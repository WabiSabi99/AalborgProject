import os
from multiprocessing import Pool
from PIL import Image
from FolderStructure import FolderStructure


class CutAndSave(FolderStructure):
    def __init__(self, folder_name=None, debug=False):
        super().__init__(folder_name, debug)
        self.target_width, self.target_height = 4352, 4352

    def extend_with_black_bars(self,split_list):


        for i in split_list:

            for j in os.listdir(f"{self.jpg_path}/{i}"):
                # Open the image
                image = Image.open(f"{self.jpg_path}/{i}/{j}")
                # Get the dimensions of the original image
                original_width, original_height = image.size

                # Calculate the dimensions of the black borders
                border_width = (self.target_width - original_width) // 2
                border_height = (self.target_height - original_height) // 2

                # Create a new blank image with the target dimensions
                extended_image = Image.new("RGB", (self.target_width, self.target_height), color="black")

                # Paste the original image onto the extended image
                offset = (border_width, border_height)
                extended_image.paste(image, offset)

                # Save the final image
                extended_image.save(f'TestFolder/jpg_cut/{i}/{j}')



def split_list(list, num_processes):
    # Prints the length of each split list
    list = [list[i::num_processes] for i in range(num_processes)]
    for i in range(num_processes):
        print(f"Length of split_panos[{i}] = {len(list[i])}")
        print(f"Split_panos[{i}] = {list[i]}")
    return list


def process_split_list(split):
    cut = CutAndSave()
    cut.extend_with_black_bars(split)

if __name__ == '__main__':
    # cut = CutAndSave()
    #
    # num_processes = os.cpu_count()
    #
    #
    # target = split_list(os.listdir(cut.jpg_path), num_processes)
    #
    # with Pool(processes=num_processes) as pool:
    #     pool.map(process_split_list, target)

    counter = 0
    for i in os.listdir("TestFolder/jpg_cut"):
        for j in os.listdir(f"TestFolder/jpg_cut/{i}"):
            counter += 1
    print(f"Total number of images in jpg_cut: {counter}")

    counter1 = 0
    for i in os.listdir("TestFolder/jpg"):
        for j in os.listdir(f"TestFolder/jpg/{i}"):
            counter1 += 1
    print(f"Total number of images in jpg: {counter}")



    # Creates the folders for the cut images
    # for i in os.listdir(cut.jpg_path):
    #     tile_xpos = int(i.split("_")[0])
    #     tile_ypos = int(i.split("_")[1])
    #     cut.create_tile_folder_coordinate(foldername="jpg_cut", xpos=tile_xpos, ypos=tile_ypos)
