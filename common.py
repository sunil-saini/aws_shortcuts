import os
import json
import logging.config
import aws
from about_host import collect_all_required_data


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


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def write_string_to_file(filename, string):
    fp = open(filename, 'w')
    fp.write(string)
    fp.close()
    logger.info("file %s updated successfully" % filename)


def get_alias_function(alias_name, file_path):
    function = alias_name+"() {\n"+"grep \"$1\" "+"\""+file_path+"\""+"\n}\n\n"
    return function


def service_function_mapping(s):
    mapping = {
        "ec2": aws.ec2,
        "s3": aws.s3,
        "lambdas": aws.lambdas,
        "ssm_parameters": aws.ssm_parameters,
        "route53": aws.hosted_zones
    }

    return mapping[s]


def source_alias_functions(file_to_source):

    host = collect_all_required_data()
    profile_file = host['home'] + "/." + host['shell'].split("/")[-1] + "rc"

    if not check_file_exists(profile_file):
        if host['os'] == "darwin":
            profile_file = host['home'] + "/.bash_profile"
        else:
            profile_file = host['home'] + "/.bashrc"

    line_to_append = "\n# added by aws_shortcuts\n"+"source "+file_to_source+"\n"

    fp = open(profile_file)
    file_content = fp.read()

    if line_to_append not in file_content:
        fp = open(profile_file, 'a+')
        fp.write(line_to_append)
        fp.close()
        logger.info("file %s updated successfully" % profile_file)
