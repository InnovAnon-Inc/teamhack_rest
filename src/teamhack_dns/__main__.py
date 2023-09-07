from psycopg2           import connect
from teamhack_db.conf   import config
from            .server import start_dns_server

if __name__ == '__main__':
  params = config()
  conn   = connect(**params)

  create_table(conn)
  start_dns_server(conn)

