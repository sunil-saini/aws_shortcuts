from crontab import CronTab
import logging.config
from common import get_current_user, get_current_directory, run, start_logging

logger = logging.getLogger(__name__)


def set_cron():
    start_logging()
    username = get_current_user()
    cron = CronTab(user=username)
    command = "/bin/bash " + get_current_directory() + "/cron.sh " + get_current_directory()
    job = cron.new(command=command)
    job.hours.every(2)
    cron.write()
    logger.info("cron successfully written for user: %s" % username)


run()
set_cron()
