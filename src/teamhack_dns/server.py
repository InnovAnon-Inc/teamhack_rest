import socket
from dnslib import *

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

