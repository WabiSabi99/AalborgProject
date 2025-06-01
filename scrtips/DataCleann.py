import json
import os
import re
from urllib.parse import unquote
import shutil

label_names = {
    "0": "Street art",
    "1": "Modern architecture",
    "2": "Historic buildings",
    "3": "Statues/Sculptures",
    "4": "Bridge",
    "5": "Ships/Boats",
    "6": "Seawater",
    "7": "Dock cleat",
    "8": "Dock",
    "9": "Park",
    "10": "Trees",
    "11": "Pond/River",
    "12": "Bush",
    "13": "Sport fields",
    "14": "Stadium",
    "15": "Playground/outdoor workout",
    "16": "Bar/Pub",
    "17": "Supermarket",
    "18": "Mall",
    "19": "Stores",
    "20": "Restaurants/Cafe",
    "21": "Pedestrian street",
    "22": "Hotel",
    "24": "Fence/Walls/hedges",
    "23": "Apartment building",
    "25": "Garden",
    "26": "House",
    "27": "Bus stop",
    "28": "Parking area",
    "29": "Urban greening",
    "30": "Transport hub",
    "31": "Hospital/police stations"
}


def extract_folder_name(data):
    data_field = data.get("data", {})
    image_path = data_field.get("image", "")

    # Decode the URL-encoded path
    decoded_path = unquote(image_path)

    # Updated pattern to match different folder name formats
    patterns = [
        r"Pictures/jpg_cut/(\d+_\d+)/\d+_\d+\.jpg",
        r"Pictures\\jpg_cut\\(\d+_\d+)\\",
        r"Pictures%5Cjpg_cut%5C(\d+_\d+)%5C"
    ]

    for pattern in patterns:
        match = re.search(pattern, decoded_path)
        if match:
            folder_name = match.group(1)
            return folder_name

    return None


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json_file(file_path, data):
    with open(f'{file_path}', 'w') as file:
        json.dump(data, file)

def total_annotations(data, label_dict_number_one, label_dict_number_two):
    total_annotations = 0

    dict_number_one = str(label_dict_number_one)
    dict_number_two = str(label_dict_number_two)

    # Iterate through each task
    for task in data:
        # Count the number of annotations for the current task
        task_annotations = len(task['annotations'])
        total_annotations += task_annotations

    label_counts = {}

    # Iterate through each task
    for task in data:
        # Iterate through each annotation in the task
        for annotation in task['annotations']:
            # Check if the annotation has a result
            if annotation['result']:
                # Get the choices from the result
                choices = annotation['result'][0]['value']['choices']
                # Iterate through each choice (label number)
                for choice in choices:
                    # Get the label name from the dictionary
                    label_name = label_names.get(choice, choice)
                    # Update the count for the current label
                    label_counts[(choice, label_name)] = label_counts.get((choice, label_name), 0) + 1

    # Print the label counts
    for (label_number, label_name), count in label_counts.items():
        print(f"Label number {label_number} ({label_name}) : appeared {count} times.")

    total_double_conditions = 0

    # Iterate through each task
    for task in data:
        # Count the number of annotations for the current task
        # Iterate through each annotation in the task
        for annotation in task['annotations']:
            # Check if the annotation has a result
            if annotation['result']:
                # Get the choices from the result
                choices = annotation['result'][0]['value']['choices']
                # Check if both custom choices are in the choices
                if dict_number_one in choices and dict_number_two in choices:
                    total_double_conditions += 1

    print(f"Total number of annotations: {total_annotations}")
    print(
        f"Total number of annotations with both {label_names[dict_number_one]} and {label_names[dict_number_two]}: {total_double_conditions}")

    # print the total number of appearances of all the labels
    total_label_appearances = sum(label_counts.values())
    print(f"Total number of appearances of all the labels: {total_label_appearances}")

    print("##############################################")

    return total_label_appearances


# We want to change the names of the json file to
# the names of the folder name and the number total images

def copy_rename():
    folder_path = os.listdir("CSV und JSON  - Jacob")

    # filter the folder_path for files ending with .json
    folder_path = [file for file in folder_path if file.endswith(".json")]

    print("folder", len(folder_path))

    for i in [file for file in folder_path if file.endswith(".json")]:

        # Load the JSON data
        path = f"CSV und JSON  - Jacob/{i}"

        print("path", path)

        with open(path, 'r') as file:
            data = json.load(file)

        # Get the first task
        task = data[0]
        folder_name = extract_folder_name(task)

        total_annotations = 0

        # Iterate through each task
        for task in data:
            # Count the number of annotations for the current task
            task_annotations = len(task['annotations'])
            total_annotations += task_annotations

        # copy the file to the new name
        new_name = f"{folder_name}_{total_annotations}.json"

        # copy the file and move to different folder

        shutil.copy(f"CSV und JSON  - Jacob/{i}", f"json_folder/{new_name}")


def remove_mistakes(file_path, new_file_path):
    data = load_json_file(file_path)

    # Iterate over each task in the data
    for task in data:
        # For each task, iterate over its annotations
        for annotation in task['annotations']:
            # If an annotation has a result, get the choices from the result
            if annotation['result']:
                choices = annotation['result'][0]['value']['choices']
                # Check if the choices contain a fence but not a house
                if "24" in choices and "26" not in choices:
                    # If so, remove the fence from the choices
                    choices.remove("24")

    total_annotation = total_annotations(data, "26", "24")

    # Save the modified data into a new JSON file
    save_json_file(new_file_path, data)

    return total_annotation


if __name__ == "__main__":
    # remove_mistakes("json_folder/69149_40127_764.json")

    # counters

    total_appearances = int(0)
    total_appearances2 = int(0)

    for i in os.listdir("json_folder"):
        print(f"Processing file: {i}")
        total_label_app = total_annotations(load_json_file(f"json_folder/{i}"), "26", "24")
        print(f"Processing file: {i}")
        total_label_app2 = total_annotations(load_json_file(f"corrected_json_files/{i}"), "26", "24")
        total_appearances += total_label_app
        total_appearances2 += total_label_app2

    print(f"Total number of appearances before mistake removal {total_appearances}")
    print(f"Total number of appearances after mistake removal: {total_appearances2}")