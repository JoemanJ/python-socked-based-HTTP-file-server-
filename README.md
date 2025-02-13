## Description
This is a simple file server built using only Python's 'socket' standart package.\
Server responses are formated as basic HTTP 1.1 responses, and as such the server is accessible through virtually any web browser.\
Once accessed, the server presents a simple static HTML page resembling a file brewser, with a the contents of the hosted directory. Clients can then access subdirectories and download files navigating through the static web pages.\
Clients are served through different threads so as to never block the main server process if a long opperation is being processed.\

## Technologies Used
The server was entirely written using only standart Python 3 packages, mainly 'socket', 'os', and 'threading'.\
Virtually any web browser can be used as a client.\

## Dependencies
- Python 3.5 or later

## Usage

### Quick start
Run ```python main.py ~```\
Through a web browser, access 127.0.0.1:25252\
The '/' button takes you directly to the root_directory page\
The '..' button takes you to the parent directory of the current directory\
Clicking any directory button will take you to that directory's page\
Clicking any file button will download that file, or play the corresponding media directly on your browser if that is supported.\

### Full usage
Run the server hosting a directory (named root_directory) in the main page\
```bash
python main.py [-p PORT] [--address_filter ADDRESS_FILTER] [--max_connections MAX_CONNECTIONS] root_directory
```
Where:
- PORT: The port to open the server on. Defaults to 25252.\
- address_filter: Connections from addresses other than address_filter are refused. Accept connections from any address by default.\
- max_connections: The total number of connections the server may accept before closing. Accept connections indefinitely by default.\
- root_directory: The base directory to serve files from. Only the contents of the root directory and it's subdirectories may be accessed.\

You can also run with '-h' or '--help' arguments to see all possible arguments thougth the command line

## Implementation details
The server implements a multithreaded architecture, where a main process is responsible solely for listening for incoming connections and spawning threads to serve those connections.\
If an HTTP request is sent with the address of a directory, relative to the server's root_directory, the server will respond with an HTTP 200 OK response and a webpage listing the contents of the directory in that path.\
If an HTTP request is sent with the address of a file, relatve to the browser's root_directory, the server will send that file's data to the client, from where the client's web browser will handle that data according with it's standart treatment for the file's MIME type.\
If an HTTP request is sent with an address that does not match the relative path for any directory or file relative to the server's root_directory, the server will respond with an HTTP 404 NOT FOUND response and a web page with a link back to the server's root_directory.\
If an invalid HTTP request is sent, the server will return a HTTP 400 BAD REQUEST response\
To preserve server resourses, files are sent to clients in chunks of 1MB\
Client requests are logged to the terminal where the server is running.\
