from flask          import Flask, jsonify, request
#from flask_restful  import Resource, Api
#from importlib      import import_module
#from importlib.util import find_spec, LazyLoader, module_from_spec, spec_from_file_location
#from inspect        import getmembers, getmodulename, isclass
#from sys            import modules, path
#from tempfile       import NamedTemporaryFile
from teamhack_db.sql import insert

app = Flask(__name__)
#api = Api(app)
conn = None # TODO hackish

def dispatch(data, hostname_recordtype_cb, hostname_cb, ip_cb):
  if 'host' in data and 'type' in data:
    host = data['host']
    rt   = data['type']
    ret  = hostname_recordtype_cb(conn, host, rt)
    return ret
  if 'host' in data and 'type' not in data:
    host = data['host']
    ret  = hostname_cb(conn, host)
    return ret
  if 'inet' in data:
    addr = data['inet']
    ret  = ip_cb(conn, addr)
    return ret
  return '', 404

@app.route('/create')
def add():
  data = request.get_json(force=True)
  host = data['host']
  rt   = data['type']
  addr = data['inet']
  insert(conn, host, rt, addr)
  return '', 204

@app.route('/retrieve')
def retrieve():
  data = request.get_json(force=True)
  return dispatch(data, select_hostname_recordtype, select_hostname, select_ip)

@app.route('/update')
def update():
  # TODO
  return '', 404

@app.route('/delete')
def delete():
  data = request.get_json(force=True)
  return dispatch(data, drop_row_hostname_recordtype, drop_row_hostname, drop_row_ip)

def start_server(fconn):
  conn = fconn
  app.run(debug=True)
