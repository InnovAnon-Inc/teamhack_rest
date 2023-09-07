from psycopg2 import connect

def drop_table_domains(conn):
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS domains""")
    conn.commit()
def drop_table_hosts(conn):
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS hosts""")
    conn.commit()
def drop_tables(conn):
    drop_table_hosts(conn)
    drop_table_domains(conn)

def create_table_domains(conn):
    with conn.cursor() as curs:
        curs.execute("""
          CREATE TABLE IF NOT EXISTS domains (
          id          SERIAL        PRIMARY KEY,
          name        VARCHAR(255)  UNIQUE,
          value       CIDR
          )
        """)
    conn.commit()
def create_table_hosts(conn):
    with conn.cursor() as curs:
      curs.execute("""
        CREATE TABLE IF NOT EXISTS hosts (
          id          SERIAL        PRIMARY KEY,
          domain      INT           REFERENCES domains(id),
          name        VARCHAR(255)  UNIQUE,
          record_type VARCHAR(  4),
          value       INET
        )
      """)
    conn.commit()
def create_tables(conn):
    create_table_domains(conn)
    create_table_hosts  (conn)

def insert_table_domains(conn, name, cidr):
    sql = """INSERT INTO domains (name, value) VALUES (%s, %s)"""
    with conn.cursor() as curs:
        curs.execute(sql, (name, cidr))
    conn.commit()

def select_table_domains(conn):
    with conn.cursor() as curs:
        curs.execute("""SELECT name, value FROM domains""")
        return curs.fetchall()
def select_table_domains_value(conn, value):
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM domains WHERE value = %s""", (value,))
        return curs.fetchone()
def select_table_domains_name(conn, name):
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM domains WHERE name = %s""", (name,))
        return curs.fetchone()

def insert_table_hosts(conn, domain_id, hostname, record_type, ip):
    sql = """INSERT INTO hosts (domain, name, record_type, value) VALUES (%s, %s, %s, %s)"""
    with conn.cursor() as curs:
        # TODO validate that hostname suffix matches domain name
        # TODO validate that ip is within domain cidr
        curs.execute(sql, (domain_id, hostname, record_type, ip))
    conn.commit()
def insert_table_hosts_domain_name(conn, domain_name, hostname, record_type, ip):


def select_table_hosts(conn):
    domains = select_table_domains(conn)
    with conn.cursor() as curs:
        curs.execute("""SELECT domain, name, record_type, value FROM hosts""")
        rows = curs.fetchall()
    for row in rows:
        print('row: %s' % (row,))
    # TODO proper reverse mapping ?
    return list((*domains[row[0]-1], *row) for row in rows)
def select_table_hosts_value(conn, value):
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM hosts WHERE value = %s""", (value,))
        return curs.fetchone()
def select_table_hosts_name(conn, name):
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM hosts WHERE name = %s""", (name,))
        return curs.fetchone()

conn = connect("dbname='dns' user='dns' host='192.168.1.76' password='69novass'")
#conn.autocommit = True # change the behavior of commit
drop_tables(conn)
create_tables(conn)
ret = insert_table_domains(conn, ".htb", "10.10.0.0/16")
print("select_table_domains: %s" % (select_table_domains(conn),))
print("select_table_domains_value('10.10.0.0/16'): %s" % (select_table_domains_value(conn, '10.10.0.0/16'),))
domain = select_table_domains_name(conn, '.htb')
print("select_table_domains_name('.htb'): %s" % (domain,))
insert_table_hosts(conn, domain[0], "bookworm.htb", "A", "10.10.11.215")
print("select_table_hosts: %s" % (select_table_hosts(conn),))
print("select_table_hosts_value: %s" % (select_table_hosts_value(conn, '10.10.11.215'),))
print("select_table_hosts_name: %s" % (select_table_hosts_name(conn, 'bookworm.htb'),))




import socket
from dnslib import *



# Function to add a DNS record to the dictionary
def add_dns_record(name, record_type, value):
    # Load existing DNS records from the JSON file
    with open("db.json", "r") as f:
        dns_records = json.load(f)

    # Add the new record to the dictionary
    if name not in dns_records:
        dns_records[name] = {}
    dns_records[name][record_type] = value

    # Save the updated DNS records to the JSON file
    with open("db.json", "w") as f:
        json.dump(dns_records, f)

    print(f"Added DNS record: {name} {record_type} {value}")

# Function to handle DNS queries and return a response
def handle_dns_query(data):
    request = DNSRecord.parse(data)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = str(request.q.qname)
    qtype = request.q.qtype

    if qname in dns_records and qtype in dns_records[qname]:
        if qtype == QTYPE.NS:
            reply.add_answer(RR(rname=qname, rtype=qtype, rdata=NS(dns_records[qname][qtype])))
        else:
            reply.add_answer(RR(rname=qname, rtype=qtype, rdata=A(dns_records[qname][qtype])))
    else:
        reply.add_answer(RR(rname=qname, rtype=qtype, rdata=A('0.0.0.0')))

    return reply.pack()

# Function to start the DNS server and listen for requests
def start_dns_server():
    host = ''
    port = 53

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f'DNS server listening on port {port}... \n \n' )

    while True:
        data, address = server_socket.recvfrom(1024)
        response = handle_dns_query(data)
        server_socket.sendto(response, address)

start_dns_server()

## User interface to add and lookup DNS records
#while True:
#    choice = input('\n \n \n - "1" to add a DNS record, \n \n - "2" to add a name server record, \n \n - "3" to lookup a DNS record: \n \n \n')
#
#    if choice == '1':
#        name = input('Enter the name of the DNS record: \n ')
#        record_type = input('Enter the type of the DNS record (A, AAAA, MX, etc.): \n')
#        value = input('Enter the value of the DNS record: \n')
#        add_dns_record(name, record_type, value)
#        print(f'DNS record added: {name} {record_type} {value} \n')
#
#    elif choice == '2':
#        name = input('Enter the name of the domain: \n')
#        ns_value = input('Enter the name server value: \n')
#        add_dns_record(name, QTYPE.NS, ns_value)
#        print(f'NS record added for {name}: {ns_value} \n')
#
#    elif choice == '3':
#        name = input('Enter the name of the DNS record: \n')
#        record_type = input('Enter the type of the DNS record (A, AAAA, MX, NS, etc.):\n ')
#
#        if name in dns_records and record_type in dns_records[name]:
#            print(f'{name} {record_type} {dns_records[name][record_type]}')
#        else:
#            print(f'DNS record not found: {name} {record_type} \n')
#
#    else:
#        print('Invalid choice. Please enter "1", "2", or "3". \n \n try again... \n \n')
