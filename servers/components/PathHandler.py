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

    def get_directory_contents(self, path):
        return os.listdir(self.get_absolute_path(path))
    
    def is_path_valid(self, path):
        # return self.path_exists(path) and self.path_is_inside_root_directory(path)
        return self.path_exists(path)
    
    def path_exists(self, path):
        return os.path.exists(self.get_absolute_path(path))
    
    # def path_is_inside_root_directory(self, path):
    #     return self.current_directory in self.get_absolute_path(path)
    
    def is_directory(self, path):
        full_path = self.get_absolute_path(path)
        return os.path.isdir(full_path)
    
    def is_file(self, path):
        full_path = self.get_absolute_path(path)
        return os.path.isfile(full_path)
    
    def get_absolute_path(self, relative_path: str):
        absolute_path = None
        if relative_path[0] == '/':
            relative_path = '.'+relative_path
        
        absolute_path = os.path.abspath(os.path.join(self.current_directory, relative_path))

        return absolute_path