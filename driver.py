import json
import threading
import logging.config
from configparser import RawConfigParser
from about_host import collect_all_required_data
import common as comm

logger = logging.getLogger(__name__)


def worker(service_for):
    logger.info("Service: %s, thread started collecting data" % service_for)
    service_data = comm.service_function_mapping(service_for)()
    services_data[service_for] = service_data
    logger.info("Service: %s, thread done collecting data" % service_for)


def validate_config_properties():
    # TO DO
    pass


comm.start_logging()
logger.info("Started driver...")
parser = RawConfigParser()
parser.read("commands.properties")
validate_config_properties()

host = collect_all_required_data()

logger.info("Collected Host Data: %s" % json.dumps(host))

services_data = {}

threads_list = []
for sec in parser.sections():

    if sec != 'project':
        thread = threading.Thread(target=worker, args=(sec,))
        threads_list.append(thread)
        thread.start()

for thread in threads_list:
    thread.join()

aliases = str()
for service in parser.sections():

    if service != 'project':
        store_file = host['store'] + service + ".txt"
        comm.write_string_to_file(store_file, services_data[service])
        list_cmd = parser[service].get('list_command')
        alias_function = comm.get_alias_function(list_cmd, store_file)
    else:
        list_cmd = parser[service].get('list_command')
        update_cmd = parser[service].get('update_command')

        list_alias = comm.set_project_alias(list_cmd)
        update_alias = comm.get_update_data_alias_function(update_cmd)

        alias_function = list_alias + update_alias

    aliases += alias_function

aliases += comm.get_ssm_alias_function(parser['ssm_parameters'].get('get_command'))
logger.info("Alias Functions: %s" % aliases)

alias_file = host['aliases']
comm.write_string_to_file(alias_file, aliases)
comm.source_alias_functions(alias_file)

logger.info('driver done')
