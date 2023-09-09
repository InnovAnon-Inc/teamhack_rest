
from flask_restful import Resource

class Foo(Resource):
  def foo(self): print("foo")
class Bar(Resource):
  def bar(self): print("bar")
class Baz(Resource):
  def baz(self): print("baz")
