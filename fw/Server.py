import http.server
import socketserver

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        pass
    def do_GET(self):
        str = ''
        str+= 'path %s' % self.path
        self.wfile.write (bytes(str, 'utf-8'))
    def do_POST(self):
        pass

def _test_server():
    PORT = 8081
    httpd = socketserver.TCPServer(("", PORT), MyHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    _test_server()

