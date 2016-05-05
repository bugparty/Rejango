from fw.router import *

@url(r"^/$")
def index(request):
    return "hello,world,123"

print("hello")