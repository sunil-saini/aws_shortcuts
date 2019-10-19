import boto3


def append_ec2(response, instances_info_list, max_len):
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
                max_len = max(len(name), max_len)
                break

        instance_info = [name, instance_id, private_ip, public_ip, instance_type, current_state]
        instances_info_list.append(instance_info)

    return instances_info_list, max_len


def ec2():

    client = boto3.client('ec2')
    instances_info_list = list()

    response = client.describe_instances()
    instances_info_list, max_len = append_ec2(response, instances_info_list, 0)

    while response.get('NextToken', None):
        response = client.describe_instances(NextToken=response['NextToken'])
        instances_info_list, max_len = append_ec2(response, instances_info_list, max_len)

    all_instances_info = str()

    for ins in instances_info_list:
        all_instances_info += ins[0].ljust(max_len+5)
        for i in ins[1:]:
            all_instances_info += i.ljust(25)
        all_instances_info += "\n"

    return all_instances_info.strip()


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


def append_hosted_zones(zone_name, zone_type, rrs_response, zones_list, record_len):
    for rrs in rrs_response['ResourceRecordSets']:
        record_name = rrs['Name']
        record_len = max(len(record_name), record_len)
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

        to_append = [zone_name, zone_type, record_name, record_type] + extra
        zones_list.append(to_append)

    return zones_list, record_len


def hosted_zones():
    client = boto3.client('route53')
    response = client.list_hosted_zones()

    zones_list = list()
    zone_len = 0
    record_len = 0
    for row in response['HostedZones']:
        zone_id = row['Id']
        zone_name = row['Name']
        zone_len = max(len(zone_name), zone_len)
        zone_type = None
        if row['Config']['PrivateZone']:
            zone_type = "Private"
        else:
            zone_type = "Public"

        rrs_response = client.list_resource_record_sets(HostedZoneId=zone_id)

        zones_list, record_len = append_hosted_zones(zone_name, zone_type, rrs_response, zones_list, record_len)

        while rrs_response['IsTruncated']:
            rrs_response = client.list_resource_record_sets(HostedZoneId=zone_id,
                                                            StartRecordName=rrs_response['NextRecordName'],
                                                            StartRecordType=rrs_response['NextRecordType'])
            zones_list, record_len = append_hosted_zones(zone_name, zone_type, rrs_response, zones_list, record_len)

    all_hosted_zones = str()
    for zone in zones_list:
        all_hosted_zones += zone[0].ljust(zone_len+5)+zone[1].ljust(10)+zone[2].ljust(record_len+5)+zone[3].ljust(10)
        all_hosted_zones += ' '.join(zone[4:]) + "\n"

    return all_hosted_zones.strip()


def load_balancers():
    elb_client = boto3.client('elb')
    elbv2_client = boto3.client('elbv2')

    elb_list = elb_client.describe_load_balancers()
    elbv2_list = elbv2_client.describe_load_balancers()

    all_lb_info = str()

    for elb in elb_list['LoadBalancerDescriptions']:
        listener_descriptions = elb['ListenerDescriptions']
        instances_list = elb['Instances']
        port_mapping = []
        instances = []
        for ld in listener_descriptions:
            lb_port = str(ld['Listener']['LoadBalancerPort'])
            instance_port = str(ld['Listener']['InstancePort'])
            port_mapping.append(lb_port + "-->" + instance_port)

        for ins in instances_list:
            instances.append(ins['InstanceId'])

        lb_info = '\t'.join(['classic', elb['LoadBalancerName'], elb['Scheme'], str(port_mapping), str(instances)])
        all_lb_info += lb_info + "\n"

    for elb in elbv2_list['LoadBalancers']:
        listener_descriptions = elbv2_client.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])
        port_mapping = []
        tgs = []
        for listener in listener_descriptions['Listeners']:
            port = str(listener['Port'])
            default_action = listener['DefaultActions'][0]
            if 'TargetGroupArn' in default_action:
                tg_arn = default_action['TargetGroupArn']
                tgs.append(tg_arn)
                port_mapping.append(port + "-->" + tg_arn.split("/")[-2])
            else:
                port_mapping.append(port + "--> Rules")

        all_tgs = {}
        for tg in set(tgs):
            tg_mapping = []
            tg_response = elbv2_client.describe_target_health(TargetGroupArn=tg)
            for thd in tg_response['TargetHealthDescriptions']:
                tg_mapping.append(thd['Target']['Id'] + "-->" + str(thd['Target']['Port']))
            all_tgs[tg.split("/")[-2]] = tg_mapping

        lb_info = '\t'.join([elb['Type'], elb['LoadBalancerName'], elb['Scheme'], str(port_mapping), str(all_tgs)])
        all_lb_info += lb_info + "\n"

    return all_lb_info


def append_cloud_fronts(response, all_cfs_list, max_aliases_len):
    client = boto3.client('cloudfront')
    for item in response['DistributionList']['Items']:
        distribution = client.get_distribution(Id=item['Id'])['Distribution']
        distribution_config = distribution['DistributionConfig']
        distribution_origins = distribution_config['Origins']

        origins_id = {}

        for i in range(distribution_origins['Quantity']):
            origin_item = distribution_origins['Items'][i]
            origins_id[origin_item['Id']] = origin_item['DomainName'] + origin_item['OriginPath']

        paths = []
        default_cache_behaviour = distribution_config['DefaultCacheBehavior']
        paths.append("*" + "-->" + origins_id[default_cache_behaviour['TargetOriginId']])

        other_cache_behaviour = distribution_config['CacheBehaviors']

        for j in range(other_cache_behaviour['Quantity']):
            behaviour_item = other_cache_behaviour['Items'][j]
            path_pattern = behaviour_item['PathPattern']
            if path_pattern[0] == '/':
                routed_path = origins_id[behaviour_item['TargetOriginId']] + path_pattern
            else:
                routed_path = origins_id[behaviour_item['TargetOriginId']] + "/" + path_pattern
            paths.append(path_pattern + "-->" + routed_path)

        aliases = "-"
        if distribution.get('AliasICPRecordals', None):
            aliases = []
            for cname in distribution['AliasICPRecordals']:
                aliases.append(cname['CNAME'])

        aliases_str = ','.join(aliases)
        max_aliases_len = max(max_aliases_len, len(aliases_str))
        cfs = [distribution['DomainName'], aliases_str, ','.join(paths)]
        all_cfs_list.append(cfs)

    return all_cfs_list, max_aliases_len


def cloud_fronts():
    client = boto3.client('cloudfront')
    response = client.list_distributions()

    all_cfs_list = list()

    all_cfs_list, max_aliases_len = append_cloud_fronts(response, all_cfs_list, 0)

    while response['DistributionList'].get('IsTruncated', None):
        response = client.list_distributions(Marker=response['DistributionList']['NextMarker'])
        all_cfs_list, max_aliases_len = append_cloud_fronts(response, all_cfs_list, max_aliases_len)

    all_cfs_str = str()
    for cf in all_cfs_list:
        all_cfs_str += cf[0].ljust(40)+cf[1].ljust(max_aliases_len+5)+cf[2]+"\n"

    return all_cfs_str.strip()
