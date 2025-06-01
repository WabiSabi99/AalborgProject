import os
import pandas as pd
import ast  # Import the ast module for literal_eval


def main():
    image_counter = 0

    for i in os.listdir("TestFolder/heic"):
        if os.path.isdir(os.path.join("TestFolder/heic", i)):
            for j in os.listdir(f"TestFolder/heic/{i}"):
                if j.endswith(".heic"):
                    image_counter += 1

    print("Total number of images downloaded from the bounding box: ", image_counter)

    load_imageMetacsv = pd.read_csv("ImageMetaData.csv")

    # Assuming load_imageMetacsv is your DataFrame
    # Convert the string representation of the tuple to an actual tuple
    load_imageMetacsv['Image tile'] = load_imageMetacsv['Image tile'].apply(ast.literal_eval)

    # Now you can count the occurrences
    counts = load_imageMetacsv['Image tile'].value_counts()

    image_count_counter = 0

    for i in os.listdir("TestFolder/heic"):
        # get the x and y coordinates from the folder name
        x = i.split("_")[0]
        y = i.split("_")[1]

        # Make sure x and y are of the same data type as in counts
        count_for_tuple = counts.get((int(x), int(y), 17), 0)
        print(
            f"The count for {x}, {y}, 17 is: {count_for_tuple} | should be: {len(os.listdir(f'TestFolder/heic/{x}_{y}'))}")
        image_count_counter += count_for_tuple

    print("Total number of images found in the bounding box: ", image_counter)
    print("Total number of images found in the csv file: ", image_count_counter)
    if image_counter == image_count_counter:
        print("The number of images found in the csv file is equal to the number of images found in the folder")
    else:
        print("The number of images found in the csv file is not equal to the number of images found in the folder")
        print("Missing images: ", image_counter - image_count_counter)


if __name__ == "__main__":
    main()
