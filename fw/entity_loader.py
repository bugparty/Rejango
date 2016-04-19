import os

def load(name):
    module = __import__(name)
    return module
