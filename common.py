import os
import json
import logging.config
import os.path
from os.path import expanduser
import platform
import aws
from tqdm import tqdm

logger = logging.getLogger(__name__)


def start_logging(default_path="logging.json", default_level=logging.INFO):

    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as log_f:
            config = json.load(log_f)
            handler = config['handlers']
            prefix_path = get_home_directory() + "/aws_shortcuts/logs/"

            create_files_directory(prefix_path)

            log_file_handlers = ['info_file_handler', 'debug_file_handler', 'error_file_handler']

            for log_file_handler in log_file_handlers:
                handler[log_file_handler]['filename'] = prefix_path + handler[log_file_handler]['filename']

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_os():
    return platform.system()


def get_current_directory():
    return os.getcwd()


def get_current_user():
    return os.environ['USER']


def get_home_directory():
    return expanduser("~")


def get_current_shell():
    shell = os.environ['SHELL']
    return shell


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def create_files_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info("directory %s created successfully" % directory)


def write_string_to_file(filename, string):
    fp = open(filename, 'w')
    fp.write(string)
    fp.close()
    logger.info("file %s updated successfully" % filename)


def create_alias_function(alias_name, file_path):
    alias_function = alias_name+"() {\n"+"grep \"$1\" "+"\""+file_path+"\""+"\n}\n\n"
    return alias_function


def create_get_ssm_alias_function_string(alias_name):
    cwd = get_current_directory()
    alias_function = alias_name + "() {\n" + "if [ ! -z \"$1\" ]\nthen\n" + "python "+cwd+"/get_ssm_parameter.py \"$1\"\nfi" + "\n}\n\n"
    return alias_function


def source_alias_functions(file_to_source):
    os_name = get_os()
    shell = get_current_shell()

    profile_file = "." + shell.split("/")[-1] + "rc"
    profile_file_path = get_home_directory() + "/" + profile_file

    if not check_file_exists(profile_file_path):
        if os_name == "Darwin":
            profile_file_path = get_home_directory() + "/" + ".bash_profile"
        else:
            profile_file_path = get_home_directory() + "/" + ".bashrc"

    line_to_append = "\n# added by aws_shortcuts\n"+"source "+file_to_source+"\n"

    fp = open(profile_file_path)
    file_content = fp.read()

    if line_to_append not in file_content:
        fp = open(profile_file_path, 'a+')
        fp.write(line_to_append)
        fp.close()
        logger.info("file %s updated successfully" % profile_file_path)


def service_function_mapping(s):

    mapping = {
        "ec2": aws.ec2(),
        "s3": aws.s3(),
        "lambdas": aws.lambdas(),
        "ssm_parameters": aws.ssm_parameters(),
        "route53": aws.hosted_zones()
    }

    return mapping[s]


def run():
    start_logging()
    print("running...")
    logger.info("run is called, updating files...")
    user_home_directory = get_home_directory()
    path_to_store_ripped_files = user_home_directory + "/.aws_shortcuts/"
    create_files_directory(path_to_store_ripped_files)

    alias_functions_string = str()

    with open('services_mapping.json') as mapping_file:
        services = json.load(mapping_file)
        mapping_file.close()
        for service in tqdm(services.keys()):
            service_data = service_function_mapping(service)
            path_to_store_service_data = path_to_store_ripped_files + services[service]['file']
            write_string_to_file(path_to_store_service_data, service_data)

            alias_function_string = create_alias_function(services[service]['alias_function'],
                                                          path_to_store_service_data)
            alias_functions_string += alias_function_string

    alias_functions_file = path_to_store_ripped_files+".aliases"
    ssm_function_string = create_get_ssm_alias_function_string(services["ssm_parameters"]["get_param_value_alias_function"])
    write_string_to_file(alias_functions_file, alias_functions_string+ssm_function_string)
    source_alias_functions(alias_functions_file)
