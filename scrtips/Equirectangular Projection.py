from CreateDataSet import CreateImageMetaData
import os
import io
from streetlevel import lookaround
from PIL import Image
from GetTileValuesFromBoundingBox import TileCoordinateConverter
import multiprocessing
from pillow_heif import register_heif_opener

import time


class LookAroundImageDownloaderFromTile(CreateImageMetaData):
    def __init__(self, zoom=0, debug=False):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.zoom = 1  # zoom (int) – The zoom level. 0 is highest, 7 is lowest. | Lowest means less detailed
        self.panos = None

        self.heic_path = self._FolderStructure.heic_path
        self.debug = debug

        self.tile_x = None
        self.tile_y = None

    def get_coverage_tile(self, tile_x, tile_y):
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)

        # Save the tile coordinates to the class variables
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.create_tile_folder_coordinate(xpos=tile_x, ypos=tile_y, foldername="jpg")

        return self.panos

    def image_metaData(self, panorama) -> tuple:
        panos_ID = str(panorama.id)
        panos_build_ID = str(panorama.build_id)
        panos_lat = str(panorama.lat)
        panos_lon = str(panorama.lon)
        panos_date = str(panorama.date)

        if self.debug:
            print(f"""
               Got {len(self.panos)} panoramas. Here's one of them:
               ID: {panorama.id}\t\tBuild ID: {panorama.build_id}
               Latitude: {panorama.lat}\tLongitude: {panorama.lon}
               Capture date: {panorama.date}
               """)

        return panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date

    def download_panorama_face(self, panoramas, tile_xpos, tile_ypos, zoom=None):

        register_heif_opener()

        if zoom is None:
            zoom = self.zoom

        for panorama in panoramas:

            start_time = time.time()

            panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date = self.image_metaData(panorama)

            image_path = f"{self.jpg_path}/{tile_xpos}_{tile_ypos}/{panos_ID}_{zoom}.jpg"

            faces = []
            for face_idx in range(0, 6):
                face_heic = lookaround.get_panorama_face(panorama, face_idx, zoom, self.auth)
                face = Image.open(io.BytesIO(face_heic))
                faces.append(face)

            result = lookaround.to_equirectangular(faces, panorama.camera_metadata)
            result.save(image_path, options={"quality": 100})
            print(f"Saved  image to: {image_path} in {time.time() - start_time} seconds")


def split_list(panos, num_processes):
    # Prints the length of each split list
    list = [panos[i::num_processes] for i in range(num_processes)]
    for i in range(num_processes):
        print(f"Length of split_panos[{i}] = {len(list[i])}")
    return list


if __name__ == "__main__":

    multiprocessing.set_start_method('spawn')

    top_left_lat = 57.0537
    top_left_lon = 9.9104

    bottom_right_lat = 57.0393
    bottom_right_lon = 9.9331

    # Get title coordinates from bounding box
    tiles = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)

    # Get the total number of tiles
    total_tiles = len(tiles.get_tiles_in_bbox())
    print(f'Number of tiles in the bounding box: {total_tiles}')

    image_counter = 0
    for i in tiles.get_tiles_in_bbox():
        for j in range(0, 1):
            downloader = LookAroundImageDownloaderFromTile()
            panos = downloader.get_coverage_tile(i[0], i[1])

            image_counter += len(panos)

    print(f'Number of images to be downloaded: {image_counter}')

    downloader = LookAroundImageDownloaderFromTile()

    for i in tiles.get_tiles_in_bbox():
        x, y = i
        panos = downloader.get_coverage_tile(x, y)

        numb_process = 3

        # Split the list into 4 parts
        split_panos = split_list(panos, numb_process)  # Changed os.cpu_count() to 4

        print(f"Length of split_panos = {len(split_panos)}")

        # Create a process for each split list
        processes = []
        for i in range(numb_process):  # Changed os.cpu_count() to 4
            process = multiprocessing.Process(target=downloader.download_panorama_face, args=(split_panos[i], x, y))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()