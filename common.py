import os
import json
import logging.config
import aws
from configparser import RawConfigParser
from about_host import collect_all_required_data, project

logger = logging.getLogger(__name__)


def start_logging(default_path="logging.json", default_level=logging.INFO):

    host = collect_all_required_data()
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as log_f:
            config = json.load(log_f)
            handler = config['handlers']
            prefix_path = host['store'] + "logs/"

            log_file_handlers = ['info_file_handler', 'debug_file_handler', 'error_file_handler']

            for log_file_handler in log_file_handlers:
                handler[log_file_handler]['filename'] = prefix_path + handler[log_file_handler]['filename']

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def properties_config_parser():
    parser = RawConfigParser()
    parser.read("commands.properties")
    return parser


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def write_string_to_file(filename, string):
    fp = open(filename, 'w')
    fp.write(string)
    fp.close()
    logger.info("file %s updated successfully" % filename)


def service_function_mapping(s):
    mapping = {
        "ec2": aws.ec2,
        "s3": aws.s3,
        "lambdas": aws.lambdas,
        "ssm_parameters": aws.ssm_parameters,
        "route53": aws.hosted_zones,
        "lb": aws.load_balancers
    }

    return mapping[s]


def source_alias_functions(file_to_source):

    host = collect_all_required_data()

    if host['os'] == "darwin" and host['shell'] == "/bin/bash":
        profile_file = host['home'] + "/.bash_profile"
    else:
        profile_file = host['home'] + "/." + host['shell'].split("/")[-1] + "rc"

    line_to_append = "\n# added by "+project+"\nsource "+file_to_source+"\n"

    fp = open(profile_file, 'a+')
    file_content = fp.read()

    if line_to_append not in file_content:
        fp.write(line_to_append)
        fp.close()
        logger.info("file %s updated successfully" % profile_file)


def read_project_current_commands():
    host = collect_all_required_data()
    read_parser = RawConfigParser()

    properties_file = host['properties']
    read_parser.read(properties_file)

    for sec in read_parser.sections():
        for item in read_parser.items(sec):
            print("Current "+item[0]+" for "+sec+" is - "+item[1])

    print("\nTo rename commands - awss configure\n")


def configure_project_commands():
    host = collect_all_required_data()
    read_parser = RawConfigParser()
    write_parser = RawConfigParser()

    properties_file = host['properties']
    read_parser.read(properties_file)

    try:
        input_method = raw_input
    except NameError:
        input_method = input

    for sec in read_parser.sections():
        write_parser.add_section(sec)
        for item in read_parser.items(sec):
            cmd = input_method(item[0]+" for " + sec + " [ Current - " + item[1] + " ]: ")
            if cmd:
                write_parser.set(sec, item[0], cmd)
            else:
                write_parser.set(sec, item[0], item[1])

    with open(properties_file, 'w') as configfile:
        write_parser.write(configfile)


def create_alias_functions():
    parser = properties_config_parser()

    awss_vars = [project]

    for service in parser.sections():
        list_cmd = parser[service].get('list_command')
        get_cmd = parser[service].get('get_command', None)

        awss_vars.append(list_cmd)
        awss_vars.append(service)

        if get_cmd:
            awss_vars.append(get_cmd)

    cmd = "bash +x awss.sh " + ' '.join(awss_vars)
    os.system(cmd)
