from fw.Router import *
@url(r"^/$")
def index(request):
    return "hello,world"

print("hello")