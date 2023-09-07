import dnslib
from psycopg2         import connect

from teamhack_db.conf import config
from teamhack_db.sql  import create_table
from teamhack_db.sql  import drop_row_hostname
from teamhack_db.sql  import drop_row_id
from teamhack_db.sql  import drop_row_ip
from teamhack_db.sql  import drop_table
from teamhack_db.sql  import insert
from teamhack_db.sql  import select
from teamhack_db.sql  import select_hostname
from teamhack_db.sql  import select_ip

params = config()
conn   = connect(**params)
conn.autocommit = True # change the behavior of commit

drop_table(conn)

TEST_HOSTNAME = "bookworm.htb"
TEST_RECORD   = QTYPE.A
TEST_IP       = "10.10.11.215"

def setup(f):
  def inner(*args, **kwargs):
    create_table(conn)
    try:
      insert(conn, TEST_HOSTNAME, TEST_RECORD, TEST_IP)
      return f(*args, **kwargs)
    finally: drop_table(conn)
  return inner

@setup
def test_select():
  v = select(conn)
  assert v == [(TEST_HOSTNAME, TEST_RECORD, TEST_IP)]

@setup
def test_select_ip():
  v = select_ip(conn, TEST_IP)
  assert v == [(1, TEST_HOSTNAME, TEST_RECORD, TEST_IP)]

@setup
def test_select_hostname():
  v = select_hostname(conn, TEST_HOSTNAME)
  assert v == [(1, TEST_HOSTNAME, TEST_RECORD, TEST_IP)]

@setup
def test_drop_row_id():
  v = select_hostname(conn, TEST_HOSTNAME)[0]
  v = v[0]
  drop_row_id(conn, v)
  v = select(conn)
  assert v == []

@setup
def test_drop_row_hostname():  
  row = select_hostname(conn, TEST_HOSTNAME)
  hn  = row[0][1]
  drop_row_hostname(conn, hn)
  v = select(conn)
  assert v == []

@setup
def test_drop_row_ip():
  for ip in select_ip(conn, TEST_IP):
    drop_row_ip(conn, ip[3])
  v = select(conn)
  assert v == []

