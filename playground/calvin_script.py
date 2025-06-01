import os
import io
from streetlevel import lookaround
from PIL import Image
import multiprocessing
from pillow_heif import register_heif_opener

import time
import math


class TileCoordinateConverter:
    """
    Based on The bounding box is defined by the top-left and bottom-right coordinates
    from openstreetmap we can calculate the tiles within the bounding box.
    """

    def __init__(self, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, zoom=17):
        self.zoom = zoom
        self.top_left_lat = top_left_lat
        self.top_left_lon = top_left_lon
        self.bottom_right_lat = bottom_right_lat
        self.bottom_right_lon = bottom_right_lon

    def LonLat2tile(self, lat_deg, lon_deg, zoom=None):
        """
        Convert latitude and longitude to tile coordinates
        :param lat_deg:
        :param lon_deg:
        :param zoom:
        :return:
        """
        if zoom is None:
            zoom = self.zoom

        # Convert latitude and longitude to radians
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def get_tiles_in_bbox(self, zoom=None) -> list[tuple[int, int]]:
        """
        Get all tiles within the bounding box
        :param top_left_lat:
        :param top_left_lon:
        :param bottom_right_lat:
        :param bottom_right_lon:
        :param zoom:
        :return:
        """
        if zoom is None:
            zoom = self.zoom

        top_left_tile = self.LonLat2tile(self.top_left_lat, self.top_left_lon, zoom)
        bottom_right_tile = self.LonLat2tile(self.bottom_right_lat, self.bottom_right_lon, zoom)
        #
        # print(f'top_left_tile: {top_left_tile}')
        # print(f'bottom_right_tile: {bottom_right_tile}')
        #
        # tiles = []
        # for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
        #     for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
        #         tiles.append((x, y))
        #         print(f'x: {x}, y: {y}')
        # return tiles

        # top_left_tile = self.LonLat2tile(57.0516, 9.9142, 17)
        # bottom_right_tile = self.LonLat2tile(57.0425, 9.9348, 17)

        tiles = []
        for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
            # print(f'top_left_tile[0], bottom_right_tile[0] + 1: {top_left_tile[0], bottom_right_tile[0] + 1}')
            # print(f'top_left_tile[1], bottom_right_tile[1] + 1: {top_left_tile[1], bottom_right_tile[1] + 1}')
            # print(f'x: {x}')
            for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
                tiles.append((x, y))
            # print(f'x: {x}, y: {y}')
        return tiles


class LookAroundImageDownloaderFromTile:
    def __init__(self, zoom=0, debug=False):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.zoom = 1  # zoom (int) – The zoom level. 0 is highest, 7 is lowest. | Lowest means less detailed
        self.panos = None

        self.debug = debug

        self.tile_x = None
        self.tile_y = None

        self.foldername = "jpg"

    def get_coverage_tile(self, tile_x, tile_y):
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)

        # Save the tile coordinates to the class variables
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.create_tile_folder_coordinate(xpos=tile_x, ypos=tile_y, foldername="jpg")

        return self.panos

    def create_tile_folder_coordinate(self, xpos, ypos, foldername=None):
        """
        Create a folder structure for the images
        :param xpos:
        :param ypos:
        :param foldername:
        :return:
        """

        if foldername is None:
            foldername = self.foldername

        if not os.path.exists(f"{foldername}/{xpos}_{ypos}"):
            os.makedirs(f"{foldername}/{xpos}_{ypos}")

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


            # second check if the folder exists
            if not os.path.exists(f"{self.foldername}/{tile_xpos}_{tile_ypos}"):
                os.makedirs(f"{self.foldername}/{tile_xpos}_{tile_ypos}")

            image_path = f"{self.foldername}/{tile_xpos}_{tile_ypos}/{panos_ID}_{zoom}.jpg"

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


    # creates folders :

    # create jpg folder
    if os.path.exists("jpg"):
        pass
    else:
        os.makedirs("jpg", exist_ok=True)


    folder_counter = 0
    for i in tiles.get_tiles_in_bbox():
        x = i[0]
        y = i[1]

        os.makedirs(f"jpg/{x}_{y}", exist_ok=True)
        folder_counter += 1

    print("Number of folders created: ", folder_counter)

        # create folder for each tile

    for i in tiles.get_tiles_in_bbox()[::-1]:
        x, y = i
        print(f"Downloading images for tile: {x}, {y}")
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
