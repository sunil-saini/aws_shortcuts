import sys
import socket
from services import host

about_host = host.host_data()
domain = sys.argv[1]


def search_for_type(record_type, record):
    record = record.lower()
    if record[-1] == '.':
        record = record[:-1]
    print("\nSearching in " + record_type + " for " + record)
    if record_type == 'lb':
        if record.startswith("dualstack."):
            record = record.replace("dualstack.", "")
        lb_name_file = about_host['store']+"lb_name_dns_mapping.txt"
        lines = open(lb_name_file).readlines()
        for row in lines:
            line = row.split()
            if line[1].lower() == record:
                record = line[0]

    result_found = False
    file = about_host['store']+record_type+".txt"
    records = open(file).readlines()
    for line in records:
        if record in line:
            result_found = True
            result = line
            print(record_type + " details: \n"+result)

    if record_type == 'cloudfront' and result_found and result:
        origins = result.strip().split()[2].strip().split(",")
        lbs = []
        for origin in origins:
            endpoint = origin.split("-->")[1].split("/")[0]
            if ".elb." in endpoint and endpoint.endswith(".amazonaws.com"):
                lbs.append(endpoint)
        for lb in set(lbs):
            search_for_type('lb', lb)


def check_if_ip(record):
    try:
        all_records = record.split()
        for r in all_records:
            socket.inet_aton(r)
        return True
    except:
        return False


def type_of_record(record):
    if record.endswith("rds.amazonaws.com."):
        record_type = 'rds'
    elif record.endswith("cloudfront.net."):
        record_type = 'cloudfront'
    elif 's3-website' in record and 'amazonaws.com' in record:
        record_type = 's3'
    elif ".elb." in record and record.endswith(".amazonaws.com."):
        record_type = 'lb'
    else:
        record_type = 'Unknown'
    return record_type


def get_record(record, step):
    if not record[-1] == '.':
        record = record+"."

    if step == 1:
        print("Querying for domain: "+record)
    else:
        print("\nQuerying again for domain: " + record)
    domains_file = open(about_host['store'] + "route53.txt")
    domains = domains_file.readlines()
    for line in domains:
        row = line.split()
        if row[2].startswith(record) and row[3] in ["A", "CNAME"]:
            next_target = ' '.join(row[4:])
            print("Domain pointing to --> "+next_target)
            if not check_if_ip(next_target):
                record_type = type_of_record(next_target)
                if record_type == 'Unknown':
                    get_record(next_target, step + 1)
                else:
                    search_for_type(type_of_record(next_target), next_target)


step = 1
get_record(domain, step)
