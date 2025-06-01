
# from GetTileValuesFromBoundingBox import TileCoordinateConverter
# from OpenStreetMapTilesDownload import OpenStreetMapTilesDownload
# from DownloadPanoraImage import LookAroundImageDownloaderFromTile
# from DownloadPanoraImage import download_func_with_downloader, download_faces, split_list, Pool, os, time
# from CreateDataSet import CreateImageMetaData
# import ast  # Import the ast module for literal_eval
import pyrosm_aalborg
from pyrosm_aalborg.data import sources

import os

import pandas as pd

# Bounding box coordinates
# Numbers are taken from openstreetmap where the bounding box is defined by the top-left and bottom-right coordinates
# top_left_lat = 57.0516
# top_left_lon = 9.9142
# bottom_right_lat = 57.0425
# bottom_right_lon = 9.9348


top_left_lat = 57.0537
top_left_lon = 9.9104

bottom_right_lat = 57.0393
bottom_right_lon = 9.9331


def main():
    # read the smaller dataset

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv('csv files/ImageMetaDataSet.csv', names=['Image Name', 'ID', 'Face', 'Build ID', 'Latitude', 'Longitude', 'Capture date', 'image_url', 'Has Blurs', 'tile_URL', 'Coverage Type', 'Image tile', 'Street Address'])

    print(len(df))

    counter = 0

    for i in os.listdir("TestFolder/heic"):
        # get x and y fro
        x = i.split("_")[0]
        y = i.split("_")[1]

        for j in os.listdir(f"TestFolder/heic/{x}_{y}"):
            counter += 1


    # image_counter = 0
    #
    # for i in os.listdir("TestFolder/heic"):
    #     if os.path.isdir(os.path.join("TestFolder/heic", i)):
    #         for j in os.listdir(f"TestFolder/heic/{i}"):
    #             if j.endswith(".heic"):
    #                 image_counter += 1
    #
    # print("Total number of images downloaded from the bounding box: ", image_counter)
    #
    # load_imageMetacsv = pd.read_csv("TestFolder/ImageMetaData_part_1.csv")
    #
    # # Assuming load_imageMetacsv is your DataFrame
    # # Convert the string representation of the tuple to an actual tuple
    # load_imageMetacsv['Image tile'] = load_imageMetacsv['Image tile'].apply(ast.literal_eval)
    #
    # # Now you can count the occurrences
    # counts = load_imageMetacsv['Image tile'].value_counts()
    #
    # image_count_counter = 0
    #
    # for i in os.listdir("TestFolder/heic"):
    #     # get the x and y coordinates from the folder name
    #     x = i.split("_")[0]
    #     y = i.split("_")[1]
    #
    #     # Make sure x and y are of the same data type as in counts
    #     count_for_tuple = counts.get((int(x), int(y), 17), 0)
    #     print(
    #         f"The count for {x}, {y}, 17 is: {count_for_tuple} | should be: {len(os.listdir(f'TestFolder/heic/{x}_{y}'))}")
    #     image_count_counter += count_for_tuple
    #
    # print("Total number of images found in the bounding box: ", image_counter)
    # print("Total number of images found in the csv file: ", image_count_counter)
    # if image_counter == image_count_counter:
    #     print("The number of images found in the csv file is equal to the number of images found in the folder")
    # else:
    #     print("The number of images found in the csv file is not equal to the number of images found in the folder")
    #     print("Missing images: ", image_counter - image_count_counter)




    # specify the bounding box from the osm data



if __name__ == "__main__":
    main()
