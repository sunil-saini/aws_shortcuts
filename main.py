from crontab import CronTab
import logging.config
from common import get_current_user, get_current_directory, create_files_directory, run, start_logging, get_home_directory

logger = logging.getLogger(__name__)


def set_cron():
    start_logging()
    username = get_current_user()
    cron = CronTab(user=username)
    command = "/bin/bash " + get_current_directory() + "/cron.sh " + get_current_directory()
    job = cron.new(command=command)
    job.minute.every(5)
    cron.write()
    logger.info("cron successfully written for user: %s" % username)


create_files_directory(get_home_directory()+"/.rip_aws/logs")
run()
set_cron()
