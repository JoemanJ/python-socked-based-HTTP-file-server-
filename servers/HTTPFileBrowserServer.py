import socket
from servers.Server import BaseServer
from servers.components.HTTPResponseBuilder import HTTPResponseBuilder
from servers.components.PathHandler import PathHandler
from servers.components.FileHandler import FileHandler

class HTTPFileBrowserServer(BaseServer):
    _response_builder: HTTPResponseBuilder
    _path_handler: PathHandler
    _file_handler: FileHandler
    _conn: socket.socket
    _client_addr: tuple

    def __init__(self, addr: str, port: int, root_path: str):
        self._response_builder = HTTPResponseBuilder()
        self._path_handler = PathHandler(root_path)
        self._file_handler = FileHandler(root_path)

        super().__init__(addr, port)

    def accept_connection(self):
        self._conn, self._client_addr = self._socket.accept()
        return

    def handle_data(self):
        raw_request = self.receive_request()
        
        if raw_request:
            # print('Received request:')
            # print(raw_request)
            
            request = self.parse_request(raw_request)

            if not self._path_handler.is_path_valid(request['path']):
                print('Invalid path requested:', request['path'])
                self.send_data(self._response_builder.build_not_found_response(request['path']))
            
            elif self._path_handler.is_directory(request['path']):
                file_list = self._path_handler.get_directory_contents(request['path'])
                self.send_data(self._response_builder.build_directory_response(request['path'], file_list))

            elif self._path_handler.is_file(request['path']):
                file_data = self._file_handler.read_file_data(self._path_handler.get_absolute_path(request['path']))
                file_size = self._file_handler.get_file_size(file_data)
                self.send_data(self._response_builder.build_zip_file_response(file_data, file_size))
                self.send_data(file_data)
                # self.send_data(file_data)

    def parse_request(self, request_data: str):
        request_lines = request_data.splitlines()

        method = request_lines[0].split(' ')[0]
        path = request_lines[0].split(' ')[1]
        protocol = request_lines[0].split(' ')[2]

        headers = request_lines[3:]

        return {'method': method,
                'path': path,
                'protocol': protocol,
                'headers': headers}

    def close_connection(self):
        self._conn.close()

    def receive_request(self):
        return self._conn.recv(1024).decode()
    
    def send_data(self, data):
        return self._conn.sendall(data)