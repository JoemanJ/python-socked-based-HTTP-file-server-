import socket
from PathHandler import PathHandler
from HTTPResponseBuilder import HTTPResponseBuilder
    
class Server:
    addr: str
    port: int
    _socket: socket.socket
    _conn: socket.socket
    _client_addr: tuple
    _response_builder: HTTPResponseBuilder
    _path_handler: PathHandler

    def __init__(self, addr: str, port: int, root_path: str):
        self.addr = addr
        self.port = port

        self._socket = self.create_server_socket(addr, port)

        self._response_builder = HTTPResponseBuilder()
        self._path_handler = PathHandler(root_path)

        print('Server ready on', addr+':'+str(port))
    
    def create_server_socket(self, addr: str, port: int) -> socket.socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((addr, port))
        s.listen()

        return s
    
    def __del__(self):
        self._socket.close()
        print('Server closed')
        return
    
    def start(self, connections: int = -1):
        handled_connections = 0
        print('Awaiting connection')

        while connections == -1 or handled_connections <= connections:
            self.accept_connection()
            self.handle_data()
            self.close_connection()
            handled_connections += 1
        
        self.close()

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
                self.send_data(self._response_builder.build_response)
                # self.send_data(self._response_builder.build_test_response())

    def parse_request(self, request_data: str):
        request_lines = request_data.splitlines()

        method = request_lines[0].split(' ')[0]
        path = request_lines[0].split(' ')[1]
        protocol = request_lines[0].split(' ')[2]

        headers = request_lines[3:]

        return {'method': request_lines[0].split(' ')[0],
                'path': request_lines[0].split(' ')[1],
                'protocol': request_lines[0].split(' ')[2],
                'headers': request_lines[3:]}
    
    def close_connection(self):
        self._conn.close()

    def receive_request(self):
        return self._conn.recv(1024).decode()
    
    def send_data(self, data):
        return self._conn.sendall(data)

    def close(self):
        self._socket.close()
    
