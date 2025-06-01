import time
from streetlevel import lookaround
from multiprocessing import Pool
from CreateDataSet import CreateImageMetaData
import os


class LookAroundImageDownloaderFromTile(CreateImageMetaData):
    def __init__(self, zoom=0, debug=False):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.zoom = zoom  # zoom (int) – The zoom level. 0 is highest, 7 is lowest. | Lowest means less detailed
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

        self.create_tile_folder_coordinate(xpos=tile_x, ypos=tile_y, foldername="heic")

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

    def download_panorama_face(self, panorama, tile_xpos, tile_ypos, zoom=None):

        panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date = self.image_metaData(panorama)

        if zoom is None:
            zoom = self.zoom

        for face in range(0, 6):
            # address = self.get_gps_directions(panorama.lat, panorama.lon).replace(' ', '_').replace(',', '')
            image_path = f"{self.heic_path}/{tile_xpos}_{tile_ypos}/{panos_ID}_{face}.heic"
            lookaround.download_panorama_face(pano=panorama, path=image_path, face=face, zoom=zoom, auth=self.auth)


def download_faces(split_panos):
    with Pool(num_processes) as pool:
        pool.map(download_func_with_downloader, split_panos)
        pool.close()
        pool.join()


def download_func_with_downloader(panorama, downloader, tile_xpos, tile_ypos):
    return downloader.download_panorama_face(panorama, tile_xpos, tile_ypos)


def split_list(panos, num_processes):
    # Prints the length of each split list
    list = [panos[i::num_processes] for i in range(num_processes)]
    # for i in range(num_processes):
    #     print(f"Length of split_panos[{i}] = {len(list[i])}")
    return list


# Exmaple usage
if __name__ == "__main__":
    tile_xpos = 69144
    tile_ypos = 40119

    downloader = LookAroundImageDownloaderFromTile(debug=False)
    panos = downloader.get_coverage_tile(tile_xpos, tile_ypos)


    print(f'Got {len(downloader.panos)*6} panoramas')

    timer = time.time()

    num_processes = os.cpu_count()

    split_panos = split_list(panos, num_processes)

    # Number of processes you want to run concurrently


    with Pool(num_processes) as pool:
        flat_panos = [item for sublist in split_panos for item in sublist]
        start_time = time.time()  # Start the timer
        pool.starmap(download_func_with_downloader,
                     [(panorama, downloader, tile_xpos, tile_ypos) for panorama in flat_panos])

        end_time = time.time()  # End the timer

    print(f"Total time for downloading: {end_time - start_time} seconds")
