import http.server
import socketserver
import fw.router
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.single_url = fw.router.SingleUrls()
        super(MyHTTPRequestHandler,self).__init__(request, client_address, server)

    def do_HEAD(self):
        pass

    def do_GET(self):
        str = ''
        str+= 'path %s' % self.path
        raw_response = self.single_url.distpach('GET', self.path)
        self.wfile.write (bytes(raw_response, 'utf-8'))

    def do_POST(self):
        pass

def _test_server():
    PORT = 8081
    httpd = socketserver.TCPServer(("", PORT), MyHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    _test_server()

