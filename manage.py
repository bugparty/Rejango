import fw.entity_loader
import config
import fw.router
import fw.dev_server
import socketserver
module = fw.entity_loader.load(config.app)
urls = fw.router.SingleUrls()
urls.printUrls()
PORT = 8081
httpd = socketserver.TCPServer(("", PORT), fw.dev_server.MyHTTPRequestHandler)
httpd.serve_forever()