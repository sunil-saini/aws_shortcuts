from crontab import CronTab
from main import get_current_user, get_current_directory, run


def set_cron():
    username = get_current_user()
    cron = CronTab(user=username)
    command = "python " + get_current_directory() + "/main.py"
    job = cron.new(command=command)
    job.minute.every(2)
    cron.write()


run()
set_cron()
