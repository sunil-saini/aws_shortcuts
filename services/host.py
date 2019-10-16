import platform
import os
import os.path
from os.path import expanduser

project = "aws_shortcuts"


def get_os():
    return platform.system().lower()


def get_current_user():
    if os.environ['USER']:
        return os.environ['USER']
    else:
        return os.environ['LOGNAME']


def get_home_directory():
    return expanduser("~")


def get_current_shell():
    shell = os.environ['SHELL']
    return shell


def host_data():
    data = dict()
    data['os'] = get_os()
    data['user'] = get_current_user()
    data['home'] = get_home_directory()
    data['shell'] = get_current_shell()
    data['store'] = data['home'] + "/."+project+"/"
    data['aliases'] = data['store'] + ".aliases"
    data['project'] = data['store'] + project+"/"
    data['scripts'] = data['project'] + "scripts/"
    data['resources'] = data['project'] + "resources/"

    return data
