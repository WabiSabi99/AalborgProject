from PIL import Image
from pillow_heif import register_heif_opener
import os
from FolderStructure import FolderStructure
from multiprocessing import Pool


class HeicToJpgConverter(FolderStructure):
    def __init__(self):
        super().__init__()
        register_heif_opener()

        # Create a folder structure where it will store the converted images
        _FolderStructure = FolderStructure()
        _FolderStructure.create_folder_structure()
        _FolderStructure.create_heic_jpg_folders()

    def convert_heic_to_jpg(self, heic_file_path, jpg_file_path):

        # print("####################")
        # print(f"{heic_file_path}")
        # print(f"{jpg_file_path}")
        # print("####################")

        try:
            image = Image.open(heic_file_path)
            image.save(jpg_file_path)

        except Exception as e:
            print(f"An error occurred while converting {heic_file_path} to {jpg_file_path}: {e}")

    def parallel_convert_to_jpg(self, split_list, jpg_folder_path=None):

        if jpg_folder_path is None:
            jpg_folder_path = self.jpg_path

        for i in split_list:

            for k in os.listdir(f"{self.heic_path}/{i}"):
                # Here we define the jpg file path and replace the .heic extension with .jpg
                jpg_file_path = os.path.join(f'{jpg_folder_path}/{i}', k.replace(".heic", ".jpg"))

                if k.endswith(".heic"):
                    # check if the file is already converted
                    if os.path.isfile(jpg_file_path):
                        print(f"File {k} is already converted")
                        continue

                    # Here we define the heic file path
                    heic_file_path = os.path.join(self.heic_path, i, k)

                    self.convert_heic_to_jpg(heic_file_path, jpg_file_path)


# def convert_multiple_heic_to_jpg(self, jpg_folder_path=None):
#
#     if jpg_folder_path is None:
#         jpg_folder_path = self.jpg_path
#
#
#
#
#     # for i in os.listdir(self.heic_path):
#     #     if os.path.isdir(os.path.join(self.heic_path, i)):
#     #         for j in os.listdir(f"{self.heic_path}/{i}"):
#     #             if j.endswith(".heic"):
#     #
#     #                 # check if the file is already converted
#     #                 if os.path.isfile(f"{jpg_folder_path}/{i}{j.replace('.heic', '.jpg')}"):
#     #                     print(f"File {j} is already converted")
#     #                     continue
#     #
#     #                 heic_file_path = os.path.join(self.heic_path, i, j)
#     #
#     #                 jpg_file_path = os.path.join(f'{jpg_folder_path}/{i}', j.replace(".heic", ".jpg"))
#     #
#     #                 self.convert_heic_to_jpg(heic_file_path, jpg_file_path)
#     #                 convert_counter += 1
#     #                 print(f"Total number of files converted: {convert_counter}")


def split_list(list, num_processes):
    # Prints the length of each split list
    list = [list[i::num_processes] for i in range(num_processes)]
    for i in range(num_processes):
        print(f"Length of split_panos[{i}] = {len(list[i])}")
        print(f"Split_panos[{i}] = {list[i]}")
    return list


def process_split_list(split):
    converter = HeicToJpgConverter()
    converter.parallel_convert_to_jpg(split)


if __name__ == "__main__":
    converter = HeicToJpgConverter()
    heic_path = converter.heic_path

    target = split_list(os.listdir(heic_path), 8)

    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_split_list, target)
