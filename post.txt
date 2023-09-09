from flask_restful import Resource

class ShitPiss(Resource):
  def get (self): return "shit"
  def post(self): return "piss"

class Foo(Resource):
  def get (self): return "foo"
  def post(self): return "foo"

class Bar(Resource):
  def get (self): return "bar"
  def post(self): return "bar"

class Baz(Resource):
  def get (self): return "baz"
  def post(self): return "baz"

