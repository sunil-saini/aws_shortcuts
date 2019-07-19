import os
import json
from os.path import expanduser
import rip_aws


def get_current_directory():
    return os.getcwd()


def get_current_user():
    return os.getlogin()


def get_home_directory():
    return expanduser("~")


def create_files_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_string_to_file(filename, string):
    fp = open(filename, 'w')
    fp.write(string)
    fp.close()


def create_alias_function(alias_name, file_path):
    alias_function = alias_name+"() {\n"+"grep \"$1\" "+"\""+file_path+"\""+"\n}\n\n"
    return alias_function


def create_get_ssm_alias_function_string(alias_name):
    cwd = get_current_directory()
    alias_function = alias_name + "() {\n" + "if [ ! -z \"$1\" ]\nthen\n" + "python "+cwd+"/get_ssm_parameter.py \"$1\"\nfi" + "\n}\n\n"
    return alias_function


def source_alias_functions(file_to_source):
    profile_file = get_home_directory()+"/.bash_profile"
    line_to_append = "\n# added by rip_aws\n"+"source "+file_to_source+"\n"

    fp = open(profile_file)
    file_content = fp.read()

    if line_to_append not in file_content:
        fp = open(profile_file, 'a+')
        fp.write(line_to_append)
        fp.close()


def service_function_mapping(s):

    mapping = {
        "ec2": rip_aws.ec2(),
        "s3": rip_aws.s3(),
        "lambdas": rip_aws.lambdas(),
        "ssm_parameters": rip_aws.ssm_parameters()
    }

    return mapping[s]


def run():

    user_home_directory = get_home_directory()
    path_to_store_ripped_files = user_home_directory + "/.rip_aws/"
    create_files_directory(path_to_store_ripped_files)

    alias_functions_string = str()

    with open('services_mapping.json') as mapping_file:
        services = json.load(mapping_file)
        mapping_file.close()
        for service in services.keys():
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

