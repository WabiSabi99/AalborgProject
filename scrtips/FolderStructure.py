import os


class FolderStructure:
    def __init__(self, folder_name=None, debug=False):

        self.debug = debug
        if folder_name is not None:
            self.folder_name = folder_name
        else:
            self.folder_name = "TestFolder"
        self.create_folder_structure()

        self.jpg_path = f'{self.folder_name}/jpg'
        self.heic_path = f'{self.folder_name}/heic'
        self.map_tiles_path = f'{self.folder_name}/map_tiles'

    def create_folder_structure(self):
        # Create a folder structure where it will store the converted images
        # first we check if the correct folder is already created from the scripts path
        # if not we create the folder structure
        self.folder_name = f'{os.path.join(os.path.dirname(__file__), self.folder_name)}'

        if not os.path.exists(f'{self.folder_name}'):
            try:
                os.makedirs(f'{self.folder_name}')
                if self.debug:
                    print(f'Folder created successfully with the name {self.folder_name}')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
        else:
            if self.debug:
                print(f'Folder already exists with the name {self.folder_name}')

    def create_heic_jpg_folders(self):
        # Create a folder structure where it will store the converted images
        if not os.path.exists(f'{self.folder_name}/heic'):
            try:
                os.makedirs(f'{self.folder_name}/heic')
                if self.debug:
                    print(f'Folder created successfully with the name {self.folder_name}/heic')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
        else:
            if self.debug:
                print(f'Folder already exists with the name {self.folder_name}/heic')

        # Create a folder structure where it will store the converted images
        if not os.path.exists(f'{self.folder_name}/jpg'):
            try:
                os.makedirs(f'{self.folder_name}/jpg')
                if self.debug:
                    print(f'Folder created successfully with the name {self.folder_name}/jpg')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")

    def create_tile_folder(self):
        # Create a folder structure where it will store the converted images
        if not os.path.exists(f'{self.folder_name}/map_tiles'):
            try:
                os.makedirs(f'{self.folder_name}/map_tiles')
                if self.debug:
                    print(f'Folder created successfully with the name {self.folder_name}/map_tiles')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")

        return f'{self.folder_name}/map_tiles'

    def create_tile_folder_coordinate(self, foldername, xpos, ypos):
        # Create a folder structure where it will store the converted images
        if not os.path.exists(f'{self.folder_name}/{foldername}/{xpos}_{ypos}'):
            try:
                os.makedirs(f'{self.folder_name}/{foldername}/{xpos}_{ypos}')
                if self.debug:
                    print(f'Folder created successfully with the name {self.folder_name}/{foldername}/{xpos}_{ypos}')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
