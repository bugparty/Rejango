import fw.EntryLoader
import config
import fw.Router
module = fw.EntryLoader.load(config.app)
urls = fw.Router.SingleUrls()
urls.printUrls()
