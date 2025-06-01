import time
from streetlevel import lookaround
from multiprocessing import Pool
from CreateDataSet import CreateImageMetaData
from GetTileValuesFromBoundingBox import TileCoordinateConverter
import os
import pandas as pd
import pandas as pd
from FolderStructure import FolderStructure
from streetlevel import lookaround
import os
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from random import choice
from time import sleep
from urllib3.exceptions import ConnectTimeoutError
from requests.exceptions import RetryError


class CreateImageMetaData(FolderStructure):
    def __init__(self, filename=None):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.panos = None

        if filename is not None:
            self.filename = filename
        else:
            self.filename = "TestImageMetaData.csv"

        self.columns = ['Image Name', 'ID', 'Face', 'Build ID', 'Latitude', 'Longitude', 'Capture date', 'image_url',
                        'Has Blurs', 'tile_URL', 'Coverage Type', 'Image tile', 'Street Address']
        self.df = pd.DataFrame(columns=self.columns)

        # Create a folder structure where it will store the converted images
        self._FolderStructure = FolderStructure()
        self._FolderStructure.create_folder_structure()
        self.folder_to_save_path = self._FolderStructure.folder_name

    def append_image_data(self, image_name, panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, image_url,
                          tile_URL, tile_coordinate, address, face_value, has_blur, coverage_type) -> None:
        """Append the data to the dataframe"""
        new_data = {
            'Image Name': image_name,
            'ID': panos_ID,
            'Face': face_value,
            'Build ID': panos_build_ID,
            'Latitude': panos_lat,
            'Longitude': panos_lon,
            'Capture date': panos_date,
            'image_url': image_url,
            'Has Blurs': has_blur,
            'tile_URL': tile_URL,
            'Coverage Type': coverage_type,  # 'CAR' or 'BACKPACK
            'Image tile': tile_coordinate,
            'Street Address': address,
        }
        new_df = pd.DataFrame([new_data])  # Create a new DataFrame with the new data
        self.df = pd.concat([self.df, new_df], ignore_index=True)  # Concatenate the new DataFrame to the existing one

        print(f"Appending data for image {image_name}")
        print(self.df.shape)
        return None

    def get_coverage_tile(self, tile_x, tile_y):
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)
        return self.panos

    def image_metaData(self, panorama) -> tuple:
        panos_ID = str(panorama.id)
        panos_build_ID = str(panorama.build_id)
        panos_lat = str(panorama.lat)
        panos_lon = str(panorama.lon)
        panos_date = str(panorama.date)
        panos_permalink = str(panorama.permalink())  # Add parentheses here
        panos_coverage_type = str(panorama.coverage_type)
        panos_has_blurs = str(panorama.has_blurs)
        panos_tile = str(panorama.tile)

        # print(f"""
        #           Got {len(self.panos)} panoramas. Here's one of them:
        #           ID: {panorama.id}\t\tBuild ID: {panorama.build_id}
        #           Latitude: {panorama.lat}\tLongitude: {panorama.lon}
        #           Capture date: {panorama.date}\tPermalink: {panos_permalink}\tCoverage Type: {panorama.coverage_type}\tHas Blurs: {panorama.has_blurs}
        #           \t Tile: {panorama.tile}
        #
        #
        #           """)

        return panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, panos_permalink, panos_coverage_type, panos_has_blurs, panos_tile

    @staticmethod
    def get_gps_directions(latitude, longitude, attempt=1, max_attempts=10):
        """Recursively get the GPS directions from the latitude and longitude. If the attempt fails, it will retry"""

        # random list of user_agents to avoid getting blocked
        user_agents = ["SemesterAgentOne", "ProjectExplorerAgent", "MED10-MASTER-THESIS-PROJECT",
                       "CodeCraftNavigator", "QuantumSemesterSurfer", "ByteBusterNavigator", "PolyglotSemesterSailor",
                       "MetaCodeAdventurer", "SyntaxSeekerExplorer", "AlgorithmicVoyagerAgent", "DataDrivenNavigator",
                       "QuantumBytePioneer"]

        try:
            # pick a random user_agent
            geolocator = Nominatim(user_agent=choice(user_agents), timeout=25)
            location = geolocator.reverse([latitude, longitude], exactly_one=True)
            return location.address if location else "No address found."
        except (ConnectTimeoutError, RetryError, GeocoderUnavailable) as e:
            if attempt < max_attempts:
                print(f"Attempt {attempt} failed. Retrying...")
                sleep(2 ** attempt)  # exponential backoff, waiting longer with each attempt
                return CreateImageMetaData.get_gps_directions(latitude, longitude, attempt=attempt + 1,
                                                              max_attempts=max_attempts)
            else:
                return "Failed to get GPS directions after multiple attempts."

    def save_to_csv(self) -> None:
        """Save the dataframe to a csv file"""
        self.df.to_csv(f'{self.folder_to_save_path}/{self.filename}', index=False)
        print("Saving data to CSV")
        # prints the row and column count of the dataframe
        print(self.df.shape)
        return None


# Define the bounding box (top left and bottom right coordinates) -> Based on the openstreet map
top_left_lat = 57.0537
top_left_lon = 9.9104

bottom_right_lat = 57.0393
bottom_right_lon = 9.9331

# Exmaple usage
if __name__ == "__main__":
    converter = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)
    downloader = CreateImageMetaData()

    list_of_tiles = converter.get_tiles_in_bbox()



    for x, y in list_of_tiles:
        panos = downloader.get_coverage_tile(x, y)

        for i in panos:
            panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, panos_permalink, panos_coverage_type, panos_has_blurs, panos_tile = downloader.image_metaData(
                i)
            address = downloader.get_gps_directions(panos_lat, panos_lon)

            image_name = f'{panos_ID}_{i}'
            tile_URL = f'https://lookaround.blob.core.windows.net/panoramas/{i.tile}.jpg'
            image_url = panos_permalink

            downloader.append_image_data(image_name, panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date,
                                         image_url, tile_URL, panos_tile, address, i, panos_has_blurs, panos_coverage_type)

    downloader.save_to_csv()
