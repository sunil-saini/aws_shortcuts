import time
import json
import threading
import logging.config
from about_host import collect_all_required_data
import common as comm

logger = logging.getLogger(__name__)
services_data = {}
host = collect_all_required_data()


def validate_config_properties():
    # TO DO
    pass


def worker(service_for):
    log = "Service: %s, thread started collecting data" % service_for
    print(log)
    logger.info(log)
    service_data = comm.service_function_mapping(service_for)()
    global services_data
    services_data[service_for] = service_data
    log = "Service: %s, thread done collecting data" % service_for
    print(log)
    logger.info(log)


def start_service_threads():
    parser = comm.properties_config_parser()
    threads_list = []
    for service in parser.sections():
        thread = threading.Thread(target=worker, args=(service,))
        threads_list.append(thread)
        thread.start()
        time.sleep(1)

    for thread in threads_list:
        thread.join()


def write_service_data():
    parser = comm.properties_config_parser()
    global services_data
    global host
    for service in parser.sections():
        store_file = host['store'] + service + ".txt"
        comm.write_string_to_file(store_file, services_data[service])


def update_services_data():
    start_service_threads()
    write_service_data()


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


main()
