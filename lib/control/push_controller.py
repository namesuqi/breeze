# coding=utf-8

from lib.decorator.trace import *
from lib.control.const import *
from lib.common.remoter import *

__author__ = 'dh'


@print_trace
@log_func_args
def route_push(ip, command):
    """

    :param ip:
    :param command:
    :return:
    """
    pass


@log_func_args
@print_trace
def get_live_push_version(ip):
    cmd = "cd {0} && ./{1} -v".format(REMOTE_LIVE_PUSH_SUPP_PATH, LIVE_PUSH_FILE)
    print cmd
    version = remote_execute_stderr(ip, LIVE_PUSH_USER, LIVE_PUSH_ADMIN_PASSWD, cmd)
    # if version in LIVE_PUSH_VERSION_DICT.keys():
    #     return LIVE_PUSH_VERSION_DICT[version]
    # else:
    #     return LIVE_PUSH_VERSION
    return version.split(" ")[-1]


def deploy_upload_livepush():
    # kill previous processes
    kill_cmd = "ps aux | grep livepush | grep -v grep | awk '{print$2}' | xargs kill"
    remote_execute(LIVE_PUSH_IP, ADMIN_USER, ADMIN_PASSWD, kill_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_LIVE_PUSH_PATH)
    remote_execute(LIVE_PUSH_IP, ADMIN_USER, ADMIN_PASSWD, mkdir_cmd)

    # copy file to remote sdk dir
    loacl_upload_livepush = "{0}/web/uploads/livepush/{1}".format(ROOT_PATH, LIVE_PUSH_FILE)
    copy_file_to(LIVE_PUSH_IP, ADMIN_USER, ADMIN_PASSWD, loacl_upload_livepush, REMOTE_LIVE_PUSH)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_LIVE_PUSH)
    remote_execute(LIVE_PUSH_IP, ROOT_USER, ROOT_PASSWD, chmod_cmd)


def start_livepush():
    start_cmd = 'cd {0}; (./{1} > /dev/null 2>&1 &)'.format(REMOTE_LIVE_PUSH_PATH, LIVE_PUSH_FILE)
    remote_execute(LIVE_PUSH_IP, ADMIN_USER, ADMIN_PASSWD, start_cmd)
