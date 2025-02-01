from servers.HTTPFileBrowserServer import HTTPFileBrowserServer

def main():
    addr = "127.0.0.1"
    port = 8081


    s = HTTPFileBrowserServer(addr, port, '.')
    
    s.start(5)

if __name__ == "__main__":
    main()