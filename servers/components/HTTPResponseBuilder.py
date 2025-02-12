import os

class HTTPResponseBuilder:
    def __init__(self):
        pass

    def build_test_response(self):
        response = ''
        response += 'HTTP/1.1 200 OK\r\n'
        response += '\r\n'
        response += ''
        response += '<html>'
        response += '<head><title>Hello World</title></head>'
        response += '<body>Hello World</body>'
        response += '</html>'

        return response.encode()
    
    def build_not_found_response(self, path: str):
        response = ''
        response += 'HTTP/1.1 404 NOT FOUND\r\n'
        response += '\r\n'
        response += ''
        response += '<html>'
        response += '<head><title>Not Found</title></head>'
        response += '<body>'
        response += '<h1>404 Not Found</h1>'
        response += f'<p>Could not find the following resourse: {path}</p>'
        response += '<p>Click <a href="/">here</a> to return to the root directory</p>'
        response += '</body>'
        response += '</html>'

        return response.encode()
    
    def build_directory_response(self, path: str, file_list: list):
        response = ''
        response += 'HTTP/1.1 200 OK\r\n'
        response += '\r\n'
        response += ''
        response += '<html>'
        response += f'<head><title>{path}</title></head>'
        response += '''
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 0;
            }

            h1 {
                background-color: #007bff;
                color: white;
                padding: 20px;
                margin: 0;
                text-align: center;
            }

            ul {
                list-style-type: none;
                padding: 0;
                margin: 20px;
            }

            li {
                background-color: #fff;
                margin: 5px 0;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }

            a {
                text-decoration: none;
                color: #007bff;
            }

            a:hover {
                color: #0056b3;
            }

            li a {
                display: block;
                padding: 5px 10px;
            }
        </style>
        '''
        response += '<body>'
        response += f'<h1>{path}</h1>'
        response += '<ul>'
        response += f'<li><a href="/">/</a></li>'
        if path != '/':
            response += f'<li><a href="{os.path.join(path, os.path.pardir)}">..</a></li>'
        if file_list:
            for file in file_list:
                response += f'<li><a href="{os.path.join(path, file)}">{file}</a></li>'
        response += '</ul>'
        response += '</body>'
        response += '</html>'

        return response.encode()
    
    def build_file_response_header(self, file_size: int, content_type: str):
        response = ''
        response += 'HTTP/2 200 OK\r\n'
        response += f'Content-Length: {file_size}'
        response += 'content-disposition: attachment; filename=sample-1.zip'
        response += '\r\n'
        response += f'Content-Type: {content_type}'
        response += '\r\n'
        response += '\r\n'

        return response.encode()
        
    def build_invalid_request_response(self):
        response = ''
        response += 'HTTP/2 400 Bad Request\r\n'