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