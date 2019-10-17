import time
import json
import threading
import logging.config
from services.host import host_data
from services import common as comm

logger = logging.getLogger(__name__)
comm.start_logging()
services_data = {}
host = host_data()


def validate_config_properties():
    # TODO validate resources/commands.properties
    pass


def log_and_print(log):
    print(log)
    logger.info(log)


def worker(service_for):
    log_and_print("Service: %s, thread started collecting data" % service_for)
    service_data = comm.service_function_mapping(service_for)()
    store_file = host['store'] + service_for + ".txt"
    comm.write_string_to_file(store_file, service_data)
    log_and_print("Service: %s, thread done collecting data" % service_for)


def update_services_data():
    parser = comm.properties_config_parser()
    threads_list = []
    for service in parser.sections():
        thread = threading.Thread(target=worker, args=(service,))
        threads_list.append(thread)
        thread.start()
        time.sleep(1)

    for thread in threads_list:
        thread.join()


def main():
    comm.start_logging()
    logger.info("Started driver...")

    validate_config_properties()

    logger.info("Collected Host Data: %s" % json.dumps(host))

    update_services_data()

    comm.create_alias_functions()

    comm.source_alias_functions(host['aliases'])
    comm.read_project_current_commands()

    logger.info('driver done')
