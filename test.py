#! /usr/bin/env python3

from flask_restful import Resource

from importlib      import import_module
#from imp            import new_module
from importlib.util import find_spec, LazyLoader, module_from_spec, spec_from_file_location
from inspect        import getmembers, getmodulename, isclass
from sys            import modules
from tempfile       import NamedTemporaryFile

def gensym(length=32, prefix="gensym_"):
  """
  generates a fairly unique symbol, used to make a module name,
  used as a helper function for load_module

  :return: generated symbol
  """
  alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
  symbol = "".join([secrets.choice(alphabet) for i in range(length)])

  return prefix + symbol

def load_module(source, module_name=None, lazy=True):
  """
  reads file source and loads it as a module

  :param source: file to load
  :param module_name: name of module to register in sys.modules
  :return: loaded module
  """

  if module_name is None: module_name = gensym()

  spec = spec_from_file_location(module_name, source)
  if lazy: spec.loader = LazyLoader(spec.loader)
  module               = module_from_spec(spec)
  modules[module_name] = module
  spec.loader.exec_module(module)

  return module, module_name

def upload_file(file):
  path = NamedTemporaryFile(delete=False, dir="uploads", suffix='.py')
  path.write(file.encode())
  return path.name


def add(code):
  path              = upload_file(code)
  name              = getmodulename(path)
  assert name is not None
  module, name      = load_module(path, name, False)
  assert name is not None
  mems = getmembers(module, isclass)
  assert mems != []
  mems = [cls for _, cls in mems if issubclass(cls, Resource)]
  assert mems != []
  return name, mems

name, mems = add("""
from flask_restful import Resource

class Foo(Resource):
  def foo(self): print("foo")
class Bar(Resource):
  def bar(self): print("bar")
class Baz(Resource):
  def baz(self): print("baz")
""")

print(f'name: {name}')
print(f'mems: {mems}')

