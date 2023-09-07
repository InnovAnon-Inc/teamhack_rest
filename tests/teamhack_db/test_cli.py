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
TEST_RECORD   = "A"
TEST_IP       = "10.10.11.215"

# TODO testing a read loop hopefully won't be more verbose than doing it in bash
# python -m teamhack_cli | tee cli.out < cli.in
# diff -q cli.out cli.exp
def test_1(): pass
  
