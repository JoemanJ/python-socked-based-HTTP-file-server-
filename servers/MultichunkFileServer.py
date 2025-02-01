from servers.Server import Server
import socket
import threading
import os

class MultichunkFileServer(Server):
    _chunk_size: int = 1024*1000 # 1MB
    _clients: dict = {}

    def __init__(self, host, port, chunk_size):
        super().__init__(host, port)
        self._chunk_size = chunk_size
        self._clients = {}

    def start(self, connections: int = -1):
        handled_connections = 0
        print('Awaiting connection')

        while connections == -1 or handled_connections < connections:
            self.accept_connection()
            # self.close_connection()
            handled_connections += 1
        
        self.close()

    def accept_connection(self):
        connection, address = self._socket.accept()
        
        if self.is_new_client(address):
            self.register_new_client(connection, address)
        else:
            
            pass #TODO: handle chunk requests
        return

    def is_new_client(self, address: str):
        return address in self._clients
    
    def register_new_client(self, client_address: str, client_connection: socket.socket):
        thread = self.create_new_thread_for_client(client_connection)
        self._clients[client_address] = thread
        return
    
    def create_new_thread_for_client(self, client_connection: socket.socket):
        thread = ClientHandler(client_connection, self._chunk_size)
        thread.start()
        return thread


    
class ClientHandler(threading.Thread):
    _connection: socket.socket
    _chunk_size: int
    _file_path: str
    _file: any
    _number_of_chunks: int
    _uploader_threads: list[threading.Thread]
    _ready_uploaders: int

    def __init__(self, connection: socket.socket, chunk_size: int):
        self._connection = connection
        self._chunk_size = chunk_size
        super().__init__(target=self.handle_client)
        self._ready_uploaders = 0

    def handle_client(self):
        self.receive_file_path()
        if not self.request_is_valid(self._file_path):
            print(f'Requested path is invalid: {self._file_path}')
            self._connection.close()
            return
            
        self.open_file()
        self.calculate_number_of_chunks()
        self.send_number_of_chunks()
        self.create_uploader_threads()
        self.wait_until_uploaders_ready()
        self.start_uploaders()
        self.join_uploaders()
        self._connection.close()
        return

    def receive_file_path(self):
        request = self._connection.recv(1024)
        self._file_path = request.decode()
        return
        
    def request_is_valid(self):
        if not os.path.exists(self._file_path):
            return False
        if not os.path.isfile(self._file_path):
            return False
        
        return True

    def open_file(self):
        return open(self._file_path, 'rb')
    
    def calculate_number_of_chunks(self):
        self._number_of_chunks = len(self._file) / self._chunk_size
        if len(self._file) % self._chunk_size != 0:
            self._number_of_chunks += 1
        return

    def send_number_of_chunks(self):
        self._connection.send(str(self._number_of_chunks).encode())
        return
    
    def create_uploader_threads(self):
        for i in range(self._number_of_chunks):
            start_byte = 1024*i
            chunk = None

            if i != self._number_of_chunks-1: # not the last chunk
                chunk = self._file[start_byte:start_byte + self._chunk_size]
            else: # the last chunk
                chunk = self._file[start_byte:]

            thread = UploaderThread(chunk)
            self._uploader_threads.append(thread)
        return
        
    def wait_until_uploaders_ready(self): # This is busy wait, but i couldn't think of anything better
        while self._ready_uploaders < 8:
            continue
        return
    
    def start_uploaders(self):
        for thread in self._uploader_threads:
            thread.start()
        return
    
    def join_uploaders(self):
        for thread in self._uploader_threads:
            thread.join()
        return



class UploaderThread(threading.Thread):
    _connection: socket.socket = None
    _chunk: bytes
    
    def __init__(self, chunk: bytes):
        super().__init__(self.upload)

    def upload(self):
        assert self._connection != None
        self._connection.sendall(self._chunk)
        self._connection.close()