import time
import json
import threading
import logging.config
from about_host import collect_all_required_data
import common as comm

logger = logging.getLogger(__name__)


def validate_config_properties():
    # TO DO
    pass


def worker(service_for):
    log = "Service: %s, thread started collecting data" % service_for
    print(log)
    logger.info(log)
    service_data = comm.service_function_mapping(service_for)()
    services_data[service_for] = service_data
    log = "Service: %s, thread done collecting data" % service_for
    print(log)
    logger.info(log)


def start_service_threads():
    parser = comm.properties_config_parser()
    threads_list = []
    for service in parser.sections():
        if service != 'project':
            thread = threading.Thread(target=worker, args=(service,))
            threads_list.append(thread)
            thread.start()
            time.sleep(1)

    for thread in threads_list:
        thread.join()


def write_service_data():
    parser = comm.properties_config_parser()
    for service in parser.sections():
        if service != 'project':
            store_file = host['store'] + service + ".txt"
            comm.write_string_to_file(store_file, services_data[service])


services_data = {}
comm.start_logging()
logger.info("Started driver...")

validate_config_properties()

host = collect_all_required_data()
logger.info("Collected Host Data: %s" % json.dumps(host))

start_service_threads()
write_service_data()
comm.create_alias_functions()

print("-"*25+"Commands"+"-"*25)
comm.read_project_current_commands()
logger.info('driver done')
