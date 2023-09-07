from psycopg2 import connect

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
#conn.autocommit = True # change the behavior of commit

drop_table(conn)
conn.commit()

create_table(conn)
conn.commit()

#ret = insert_table_domains(conn, ".htb", "10.10.0.0/16")
insert(conn, "bookworm.htb", "A", "10.10.11.215")
conn.commit()
print("A")
print("select: %s" % (select(conn),))
print("select_ip: %s" % (select_ip(conn, '10.10.11.215'),))
print("select_hostname: %s" % (select_hostname(conn, 'bookworm.htb'),))

drop_row_id(conn, select_hostname(conn, 'bookworm.htb')[0])
conn.commit()
print("B")
print("select: %s" % (select(conn),))

insert(conn, "bookworm.htb", "A", "10.10.11.215")
conn.commit()
row = select_hostname(conn, 'bookworm.htb')
print("C")
print("row: %s" % (row,))
hn  = row[1]
print("hn: %s" % (hn,))
drop_row_hostname(conn, hn)
conn.commit()
print("select: %s" % (select(conn),))

insert(conn, "bookworm.htb", "A", "10.10.11.215")
conn.commit()
for ip in select_ip(conn, "10.10.11.215"):
    drop_row_ip(conn, ip[3])
conn.commit()
print("D")
print("select: %s" % (select(conn),))

conn.commit()
exit(0)

