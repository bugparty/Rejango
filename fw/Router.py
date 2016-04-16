import re
class Request(object):
    pass
class NoUrlMatch(Exception):
    def __init__(self, url):
        self.url = url


class SingleUrls(object):
    _urls = []
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(SingleUrls, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def add_url(self, url, fn):
        SingleUrls._urls.append((url, fn))

    def printUrls(self):
        print(self._urls)

    def distpach(self,method, url):
        for compiled_path,method, fn in self._urls:
            result = compiled_path.match(url)
            if result:
                request = Request()
                return fn(request)
        raise NoUrlMatch()



def url(path, method="GET"):
   def real_decorator(fn):
       urls = SingleUrls()
       compiled_path = re.compile(path)
       urls.add_url(compiled_path, method,  fn)

   return real_decorator

