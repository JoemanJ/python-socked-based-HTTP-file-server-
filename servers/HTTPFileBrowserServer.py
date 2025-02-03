import socket
import threading
import math
from servers.Server import BaseServer
from servers.components.HTTPResponseBuilder import HTTPResponseBuilder
from servers.components.PathHandler import PathHandler
from servers.components.FileHandler import FileHandler

class HTTPFileBrowserServer(BaseServer):
    _chunk_size: int
    _response_builder: HTTPResponseBuilder
    _path_handler: PathHandler
    _file_handler: FileHandler

    def __init__(self, addr: str, port: int, root_path: str, chunk_size: int = 1024*1024):
        self._response_builder = HTTPResponseBuilder()
        self._path_handler = PathHandler(root_path)
        self._file_handler = FileHandler(root_path)
        self._chunk_size = chunk_size

        super().__init__(addr, port)

    def start(self, connections: int = -1):
        handled_connections = 0
        print('Awaiting connection')

        while connections == -1 or handled_connections < connections:
            self.accept_connection()
            handled_connections += 1
        
        self.close()

    def accept_connection(self):
        connection, client_address = self._socket.accept()
        thread = threading.Thread(target=self.handle_data, args=(connection, client_address))
        thread.start()
        return

    def handle_data(self, connection: socket.socket, client_address: tuple):
        raw_request = connection.recv(1024).decode()
        
        if raw_request:
            print('Received request:')
            print(raw_request)
            
            try:
                request = self.parse_request(raw_request)
            except:
                print(f"Invalid request: {raw_request}")
                connection.sendall(self._response_builder.build_invalid_request_response())
                connection.close()

            if not self._path_handler.is_path_valid(request['path']):
                print('Invalid path requested:', request['path'])
                connection.sendall(self._response_builder.build_not_found_response(request['path']))
            
            elif self._path_handler.is_directory(request['path']):
                print(f"Directory {request['path']} requested by {client_address}")
                file_list = self._path_handler.get_directory_contents(request['path'])
                connection.sendall(self._response_builder.build_directory_response(request['path'], file_list))

            elif self._path_handler.is_file(request['path']):
                print(f"File {request['path']} requested by {client_address}")
                file_abspath = self._path_handler.get_absolute_path(request['path'])

                file_data = self._file_handler.read_file_data(file_abspath)
                file_size = self._file_handler.get_file_size(file_data)
                file_mime_type = self._file_handler.get_file_mime_type(file_abspath)

                number_of_chunks = math.ceil(file_size/self._chunk_size)

                connection.sendall(self._response_builder.build_file_response_header(file_size, file_mime_type))
                
                for i in range(number_of_chunks):
                    start = i*self._chunk_size
                    end = min(start+self._chunk_size, file_size)
                    print(f"Sending chunk {i+1} of {number_of_chunks}. Bytes {start}-{end} ({request['path']})")
                    chunk_data = file_data[start:end]
                    
                    connection.sendall(chunk_data)
                    print(f"chunk {i+1} sent")
        
        connection.close()

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