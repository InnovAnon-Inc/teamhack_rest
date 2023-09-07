from .cli  import start_cli
from .conf import config

if __name__ == '__main__':
  params = config()
  conn   = connect(**params)

  create_table(conn)
  start_cli(conn)

