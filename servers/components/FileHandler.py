import os
import shutil
from mimetypes import guess_type

class FileHandler():
    base_directory: str

    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    def read_file_data(self, file_path: str, path_is_absolute: bool = False):
        file = open(file_path, 'rb')

        return file.read()
    
    def read_file_as_zip(self, file_path: str):
        temp_file = shutil.make_archive(os.path.basename(file_path), 'zip')
        zip_file_data = open(temp_file, 'rb').read()
        os.remove(temp_file)

        return zip_file_data
    
    def get_file_size(self, file_data: bytes):
        return len(file_data)
    
    def get_file_mime_type(self, file_path):
        return guess_type(file_path)