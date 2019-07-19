from crontab import CronTab
from main import get_current_user, get_current_directory, run


def set_cron():
    username = get_current_user()
    cron = CronTab(user=username)
    command = "/bin/bash " + get_current_directory() + "/cron.sh " + get_current_directory()
    job = cron.new(command=command)
    job.minute.every(60)
    cron.write()


run()
set_cron()
