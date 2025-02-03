import argparse
from servers.HTTPFileBrowserServer import HTTPFileBrowserServer

def main(args):
    # addr = "127.0.0.1"
    # port = 25252


    s = HTTPFileBrowserServer(args.address_filter,
                              int(args.port),
                              args.root_directory,
                              )
    
    s.start(int(args.max_connections))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='python main.py',
        description = 'This program is a simple socket-based web server that\
            lists and serves files over the network.\n\
            The server generates a simple HTML webpage on the given port with a\
            file browsing system.\n\
            Default port: 25252',
        epilog=''
    )

    parser.add_argument("root_directory", 
                        help='Root directory of the file server.')
    
    parser.add_argument('-p', '--port', 
                        help='Port to listen on. Defaults to 25252', 
                        default='25252')
    
    parser.add_argument('--address_filter',
                        help='Server will only accept connections from this address. \
                              If not specified, server will listen for connections from any address.',
                        default='')
    
    parser.add_argument('--max_connections',
                        help="Maximum number of connections the server should listen for.\n\
                              After the maximum number is reached, the server closes.\n\
                              Leave blank or '-1' for unlimited connections",
                        default='-1')
                        

    args = parser.parse_args()

    main(args)