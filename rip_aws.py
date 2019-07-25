import boto3


def ec2():

    client = boto3.client('ec2')
    response = client.describe_instances()
    all_instances_info = str()

    for reservation in response['Reservations']:
        row = reservation['Instances'][0]
        tags = row['Tags']
        state = row['State']
        instance_id = row.get('InstanceId', "NA")
        private_ip = row.get('PrivateIpAddress', "NA")
        public_ip = row.get('PublicIpAddress', "NA")
        instance_type = row.get('InstanceType', "NA")
        current_state = state.get('Name', "NA")

        name = "NA"
        for tag in tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
                break

        instance_info = '\t'.join([name, instance_id, private_ip, public_ip, instance_type, current_state])
        all_instances_info += instance_info+"\n"

    return all_instances_info


def s3():
    client = boto3.client('s3')
    response = client.list_buckets()

    all_buckets = str()

    for row in response['Buckets']:
        bucket_name = row['Name']
        all_buckets += bucket_name+"\n"

    return all_buckets


def lambdas():
    client = boto3.client('lambda')
    response = client.list_functions()

    marker = response.get('NextMarker', None)
    all_lambdas = str()

    while True:
        for row in response['Functions']:
            lambda_name = row['FunctionName']
            all_lambdas += lambda_name + "\n"

        if not marker:
            break

        response = client.list_functions(Marker=marker)
        marker = response.get('NextMarker', None)

    return all_lambdas


def ssm_parameters():
    client = boto3.client('ssm')
    response = client.describe_parameters(MaxResults=50)
    next_token = response.get('NextToken', None)

    all_ssm_parameters = str()

    for row in response['Parameters']:
        parameter_name = row['Name']
        all_ssm_parameters += parameter_name+"\n"

    while True:

        if not next_token:
            break

        response = client.describe_parameters(NextToken=next_token, MaxResults=10)
        next_token = response.get('NextToken', None)

        for row in response['Parameters']:
            parameter_name = row['Name']
            all_ssm_parameters += parameter_name + "\n"
    return all_ssm_parameters


def get_ssm_parameter_value(parameter=None):

    if not parameter:
        return
    client = boto3.client('ssm')
    response = client.get_parameters(Names=[parameter], WithDecryption=True)
    row = response['Parameters'][0]
    print(row['Value'])


def hosted_zones():
    client = boto3.client('route53')
    response = client.list_hosted_zones()

    all_hosted_zones = str()

    for row in response['HostedZones']:
        zone_id = row['Id']
        zone_name = row['Name']
        zone_type = None
        if row['Config']['PrivateZone']:
            zone_type = "Private"
        else:
            zone_type = "Public"

        rrs_response = client.list_resource_record_sets(HostedZoneId=zone_id)

        for rrs in rrs_response['ResourceRecordSets']:
            record_name = rrs['Name']
            record_type = rrs['Type']

            extra = []
            if rrs.get('ResourceRecords', None):
                for record in rrs['ResourceRecords']:
                    if record_type == "MX":
                        extra.append(record['Value'].split()[-1])
                    else:
                        extra.append(record['Value'].split()[0])

            if rrs.get('AliasTarget', None):
                extra.append(rrs['AliasTarget']['DNSName'])

            to_append = [zone_name, zone_type, record_name, record_type]+extra
            all_hosted_zones += '\t'.join(to_append)+"\n"

    return all_hosted_zones
