from .sql import insert, select_hostname_recordtype

def start_cli():
  while True: # User interface to add and lookup DNS records
    choice = input('\n \n \n - "1" to add a DNS record, \n \n - "2" to add a name server record, \n \n - "3" to lookup a DNS record: \n \n \n')

    if choice == '1':
        name        = input('Enter the name of the DNS record: \n ')
        record_type = input('Enter the type of the DNS record (A, AAAA, MX, etc.): \n')
        value       = input('Enter the value of the DNS record: \n')
        insert(conn, name, record_type, value)
        conn.commit()
        print(f'DNS record added: {name} {record_type} {value} \n')

    elif choice == '2':
        name     = input('Enter the name of the domain: \n')
        ns_value = input('Enter the name server value: \n')
        insert(conn, name, 'NS', ns_value)
        conn.commit()
        print(f'NS record added for {name}: {ns_value} \n')

    elif choice == '3':
        name        = input('Enter the name of the DNS record: \n')
        record_type = input('Enter the type of the DNS record (A, AAAA, MX, NS, etc.):\n ')

        ip          = select_hostname_recordtype(conn, name, record_type)
        #if name in dns_records and record_type in dns_records[name]:
        print(f'{name} {record_type} {ip}')
        #else:
        #    print(f'DNS record not found: {name} {record_type} \n')

    else:
        print('Invalid choice. Please enter "1", "2", or "3". \n \n try again... \n \n')

