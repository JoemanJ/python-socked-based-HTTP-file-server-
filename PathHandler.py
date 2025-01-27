import os

class PathHandler:
    _ROOT_DIRECTORY: str
    current_directory: str

    def __init__(self, root_path):

        self._ROOT_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), root_path))
        self.current_directory = self._ROOT_DIRECTORY

    def print(self):
        print('ROOT DIRECTORY:', self._ROOT_DIRECTORY)
        print('current directory:', self.current_directory)
        print('current_directory contents:', self.get_current_directory_contents())

    def get_current_directory_contents(self):
        return os.listdir(self.current_directory)
    
    def is_path_valid(self, path):
        path = self.sanitise_path(path)
        return self.path_exists(path) and self.path_is_inside_root_directory(path)
    
    def path_exists(self, path):
        return os.path.exists(os.path.join(self.current_directory, path))
    
    def path_is_inside_root_directory(self, path):
        return self._ROOT_DIRECTORY in os.path.abspath(os.path.join(self.current_directory, path))
    
    def sanitise_path(self, path):
        if path[0] == '/':
            return '.'+path
        else:
            return path
    
    def is_directory(self, path):
        path = self.sanitise_path(path)
        full_path = os.path.abspath(os.path.join(self.current_directory, path))
        return os.path.isdir(full_path)
    
    def is_file(self, path):
        path = self.sanitise_path(path)
        full_path = os.path.abspath(os.path.join(self.current_directory, path))
        return os.path.isfile(full_path)