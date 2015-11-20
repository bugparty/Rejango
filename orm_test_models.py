from orm import *

class User(Model):
    username = StringField()
    age = IntField()
    birthday = DateField()


class Foo(Model):
    bar = StringField()