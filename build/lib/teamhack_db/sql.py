from psycopg2 import connect

def drop_type_record(conn):
    with conn.cursor() as curs:
        curs.execute("""DROP TYPE IF EXISTS record_type""")
def drop_table(conn):
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS hosts""")
    drop_type_record(conn)

def create_type_record(conn):
    with conn.cursor() as curs:
        curs.execute("""CREATE TYPE record_type AS ENUM ('A', 'AAAA', 'MX')""")
def create_table(conn):
    create_type_record(conn)
    with conn.cursor() as curs:
      curs.execute("""
        CREATE TABLE IF NOT EXISTS hosts (
          id       SERIAL        PRIMARY KEY,
          hostname VARCHAR(255)  UNIQUE,
          record   VARCHAR(  4),
          ip       INET
        )
      """)

def insert(conn, hostname, record, ip):
    sql = """INSERT INTO hosts (hostname, record, ip) VALUES (%s, %s, %s)"""
    with conn.cursor() as curs:
        curs.execute(sql, (hostname, record, ip,))

def select(conn):
    with conn.cursor() as curs:
        curs.execute("""SELECT hostname, record, ip FROM hosts""")
        return curs.fetchall()

def select_ip(conn, ip):
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM hosts WHERE ip = %s""", (ip,))
        return curs.fetchall()
def select_hostname(conn, hostname):
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM hosts WHERE hostname = %s""", (hostname,))
        return curs.fetchone()

def drop_row_id(conn, row_id):
    with conn.cursor() as curs:
        curs.execute("""DELETE FROM hosts WHERE id = %s""", (row_id,))
def drop_row_hostname(conn, hostname):
    with conn.cursor() as curs:
        curs.execute("""DELETE FROM hosts WHERE hostname = %s""", (hostname,))
def drop_row_ip(conn, ip):
    with conn.cursor() as curs:
        curs.execute("""DELETE FROM hosts WHERE ip = %s""", (ip,))

conn = connect("dbname='dns' user='dns' host='192.168.1.76' password='69novass'")
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

