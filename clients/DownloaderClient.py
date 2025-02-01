import socket
import sys

FILE_PATH = sys.argv[1]
NUMBER_OF_CHUNKS = sys.argv[2]
request_string = f'{FILE_PATH}\n{NUMBER_OF_CHUNKS}'
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect(('127.0.0.1', 8081))

S.send(request_string.encode())
