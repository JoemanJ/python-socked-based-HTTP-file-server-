import socket
import os
import sys

ROOT_DIRECTORY = os.path.abspath(sys.argv[1])
ADDR = "127.0.0.1"
PORT = 25252

current_directory = ""
def build_HTML_response(directory) -> str:
    current_directory_files = os.listdir(os.path.join(ROOT_DIRECTORY, current_directory))

    response_body = ''
    response_body += f'<html><head><title>Directory listing of {directory}</title></head><body>'
    response_body += '<ul>'
    response_body += f'<li><a href="/">/</a></li>'
    response_body += f'<li><a href="{os.path.join(current_directory, os.path.pardir)}">..</a></li>'
    for file in current_directory_files:
        response_body += f'<li><a href="{os.path.join(current_directory, file)}">{file}</a></li>'
    response_body += '</ul>'
    response_body += '</body></html>'

    response = ''
    response += 'HTTP/1.1 200 OK'
    response += 'Content-Type: text/html'
    response += 'Content-Length: {}\n'.format(len(response_body.encode('utf-8')))
    response += '\n'
    response += response_body

    return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ADDR, PORT))
    s.listen()
    print(f"Server listening on {ADDR}:{PORT}")
    connection, address = s.accept()
    print(f"Connection received from {address}")
    with connection:
        while True:
            data = connection.recv(4096)
            if not data:
                print(f"Connection with client {address} closed")
                break
            print("Received data:\n", data, "\n")

            request_line = data.decode().splitlines()[0]
            requested_path = request_line.split(" ")[1]
            current_directory = requested_path[1:] if requested_path != "/" else ""
            response = build_HTML_response(current_directory)
            connection.sendall(response.encode())

print("Server closed")