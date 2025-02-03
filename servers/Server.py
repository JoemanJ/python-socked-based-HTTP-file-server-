import socket

class BaseServer:
    addr: str
    port: int
    _socket: socket.socket

    def __init__(self, addr: str, port: int):
        self.addr = addr
        self.port = port

        self._socket = self.create_server_socket(addr, port)

        print('Server ready on', addr+':'+str(port))
    
    def create_server_socket(self, addr: str, port: int) -> socket.socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((addr, port))
        except OSError as e:
            print(f'Error: Port {port} already in use')
            quit()
        
        s.listen()

        return s
    
    def __del__(self):
        self._socket.close()
        print('Server closed')
        return
    
    def start(self, connections: int = -1):
        handled_connections = 0
        print('Awaiting connection')

        while connections == -1 or handled_connections < connections:
            self.accept_connection()
            self.handle_data()
            self.close_connection()
            handled_connections += 1
        
        self.close()

    def accept_connection(self):
        pass

    def handle_data(self):
        pass
    
    def send_data(self, data):
        pass

    def close(self):
        self._socket.close()

    def close_connection(self):
        pass
    
