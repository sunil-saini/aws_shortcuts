from crontab import CronTab
import logging.config
from common import start_logging
from about_host import collect_all_required_data

logger = logging.getLogger(__name__)


def set_user_cron():
    start_logging()
    host = collect_all_required_data()
    cron = CronTab(user=host['user'])
    command = "/bin/bash " + host['project'] + "/cron.sh " + host['project']
    job = cron.new(command=command)
    job.every(2).hours()
    cron.write()
    logger.info("cron successfully written for user: %s" % host['user'])


set_user_cron()
