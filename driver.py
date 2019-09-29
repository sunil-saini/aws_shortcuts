import json
import threading
import logging.config
from configparser import RawConfigParser
from about_host import collect_all_required_data
from common import write_string_to_file, get_alias_function, get_ssm_alias_function, service_function_mapping, source_alias_functions, start_logging

logger = logging.getLogger(__name__)


def worker(service_for):
    logger.info("Service: %s, thread started collecting data" % service_for)
    service_data = service_function_mapping(service_for)()
    services_data[service_for] = service_data
    logger.info("Service: %s, thread done collecting data" % service_for)


def validate_config_properties():
    # TO DO
    pass


start_logging()
logger.info("Started driver...")
parser = RawConfigParser()
parser.read("commands.properties")
validate_config_properties()

host = collect_all_required_data()

logger.info("Collected Host Data: %s" % json.dumps(host))

services_data = {}

threads_list = []
for sec in parser.sections():
    thread = threading.Thread(target=worker, args=(sec,))
    threads_list.append(thread)
    thread.start()

for thread in threads_list:
    thread.join()

aliases = str()
for service in parser.sections():
    store_file = host['store'] + service + ".txt"
    write_string_to_file(store_file, services_data[service])
    function_name = parser[service].get('list_command')
    alias_function = get_alias_function(function_name, store_file)
    aliases += alias_function

aliases += get_ssm_alias_function(parser['ssm_parameters'].get('get_command'))
logger.info("Alias Functions: %s" % aliases)

alias_file = host['aliases']
write_string_to_file(alias_file, aliases)
source_alias_functions(alias_file)

logger.info('driver done')
