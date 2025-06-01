import os
from multiprocessing import Pool
from PIL import Image

# folder path : E:\Label studio\Data\Pictures\jpg_cut



folder_path = "E:\\Label studio\\Data\\Pictures\\jpg_cut"
output_path = "Pictures/New size"



def create_folder(folder_path) -> None:
    # create folder
    os.mkdir(folder_path)


def resize_image(split_list) -> None:

    # PIL resize

    width = 512
    height = 512

    image_counter = 0

    for i in split_list:
        for j in os.listdir(f"{folder_path}/{i}"):
            image_path = f"{folder_path}/{i}/{j}"
            output = f"{output_path}/{i}/{j}"
            im = Image.open(image_path)
            im_resized = im.resize(size=(width, height))
            im_resized.save(output)
            image_counter += 1

    print(f"Number of images resized: {image_counter}")


def split_list(list, num_processes):
    # Prints the length of each split list
    list = [list[i::num_processes] for i in range(num_processes)]
    for i in range(num_processes):
        print(f"Length of split_panos[{i}] = {len(list[i])}")
        print(f"Split_panos[{i}] = {list[i]}")
    return list

def main():

    # # create folder
    # create_folder(output_path)

    num_processes = os.cpu_count()
    target = split_list(os.listdir(folder_path), num_processes)

    with Pool(processes=num_processes) as pool:
        pool.map(resize_image, target)

if __name__ == "__main__":
    main()
