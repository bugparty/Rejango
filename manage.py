import fw.EntryLoader
import config
import fw.Router
import fw.Server
import socketserver
module = fw.EntryLoader.load(config.app)
urls = fw.Router.SingleUrls()
urls.printUrls()
PORT = 8081
httpd = socketserver.TCPServer(("", PORT), fw.Server.MyHTTPRequestHandler)
httpd.serve_forever()