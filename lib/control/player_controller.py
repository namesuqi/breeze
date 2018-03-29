# coding=utf-8
# control the player
# author: zengyuetian

import time
from lib.control.const import *
from lib.common.remoter import *
from lib.decorator.trace import *


@print_trace
@log_func_args
def player_deploy(ip):
    """
    deploy player interface
    :param ip:
    :return:
    """
    # kill previous processes
    kill_cmd = "killall -9 python"
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, kill_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_PLAYER_PATH)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, mkdir_cmd)

    # copy file to remote sdk dir
    copy_file_to(ip, ROOT_USER, ROOT_PASSWD, LOCAL_PLAYER, REMOTE_PLAYER)
    copy_file_to(ip, ROOT_USER, ROOT_PASSWD, LOCAL_FLV_PARSER, REMOTE_FLV_PARSER)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_PLAYER)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, chmod_cmd)


@print_trace
@log_func_args
def player_start(ip, url, log_file_name, buffer_time, is_upload=False):
    """
    start player(python) interface
    :param log_file_name: first_image_time or buffering num
    :param ip:
    :param url:
    :return:
    """

    url = "http://127.0.0.1:{0}/{1}".format(SDK_PORT, url)

    if is_upload:
        play_cmd = "cd {0} && nohup python {1} {2} {3} {4} > /dev/null 2>&1 &".format(REMOTE_PLAYER_PATH,
                                                                                      REMOTE_PLAYER,
                                                                                      url, log_file_name,
                                                                                      buffer_time)
    else:
        delete_first_tag_version = '3.16.0'
        from distutils.version import LooseVersion
        # from distutils.version import StrictVersion
        # if StrictVersion(PEER_INFO[ip]['sdk_version']) >= StrictVersion(delete_first_tag_version):
        if LooseVersion(PEER_INFO[ip]['sdk_version']) >= LooseVersion(delete_first_tag_version):
            play_cmd = "cd {0} && nohup python {1} {2} {3} {4} > /dev/null 2>&1 &".format(REMOTE_PLAYER_PATH,
                                                                                          REMOTE_PLAYER,
                                                                                          url, log_file_name,
                                                                                          buffer_time)
        else:
            play_cmd = "cd {0} && nohup python {1} {2} {3} {4} 0 > /dev/null 2>&1 &".format(REMOTE_PLAYER_PATH,
                                                                                            REMOTE_PLAYER, url,
                                                                                            log_file_name, buffer_time)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, play_cmd)


@print_trace
@log_func_args
def http_flv_player_start(ip, url, log_file_name, buffer_time):
    """
    start player(python) interface
    :param log_file_name: first_image_time or buffering num
    :param ip:
    :param url:
    :return:
    """
    play_cmd = "cd {0} && nohup python {1} {2} {3} {4} 0 > /dev/null 2>&1 &".format(REMOTE_PLAYER_PATH, REMOTE_PLAYER,
                                                                                    url, log_file_name, buffer_time)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, play_cmd)


@print_trace
@log_func_args
def player_stop(ip):
    """
    :param ip:
    :param times: retention parameter
    :return:
    """
    kill_cmd = "killall -9 python"
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, kill_cmd)


@print_trace
@log_func_args
def player_wait(sec):
    time.sleep(sec)


@print_trace
@log_func_args
def player_first_image_time(ip, log_file_name):
    """
    parse log and get firstplaytime
    :param ip:
    :param log_file_name
    :return:
    """
    cmd = "head -1000 {0}".format(log_file_name) + "|grep startup |awk -F ' ' '{print $5}'"
    # cmd = "head -5 {0}".format(REMOTE_PLAYER_LOG) + "|grep begin |awk -F ' ' '{print $1}'"
    cmd_result = remote_execute_result(ip, ROOT_USER, ROOT_PASSWD, cmd)

    if cmd_result.strip() in ['', None]:
        return 30

    try:
        first_image_time = float(cmd_result)
    except:
        first_image_time = -1

    return first_image_time


@print_trace
@log_func_args
def player_buffering_num(ip, log_file_name):
    """
    parse log and get buffering times
    :param ip:
    :param log_file_name
    :return:
    """
    cmd = "cat {0}".format(log_file_name) + "|grep buffering |wc -l"

    buffer_num = remote_execute_result(ip, ROOT_USER, ROOT_PASSWD, cmd)
    if buffer_num in ['', None]:
        return 0
    return int(buffer_num)


@print_trace
@log_func_args
def player_buffering_time(peer_ip, log_file_name, over_buffering_time):
    cmd = "cat %s | grep buffering | awk '{print $4}'" % log_file_name
    buffering_time_string = remote_execute_result(peer_ip, ROOT_USER, ROOT_PASSWD, cmd)
    if buffering_time_string in ['', None]:
        return 0, 0, 0
    time_list = buffering_time_string.split('\n')
    over_time_count = 0
    for i in xrange(len(time_list)):
        time_list[i] = float(time_list[i])
        if time_list[i] > float(over_buffering_time):
            over_time_count += 1
    total_time = sum(time_list)
    max_buffering_time = max(time_list)
    return total_time, over_time_count, max_buffering_time


@print_trace
@log_func_args
def is_play_stop(peer_ip, log_file_name, expecting_play_time):
    """
        判断是否卡死
    """
    start_cmd = "head -n 1 %s" % log_file_name
    tail_cmd = "tail -n 1 %s" % log_file_name
    head_line = remote_execute_result(peer_ip, ROOT_USER, ROOT_PASSWD, start_cmd)
    tail_line = remote_execute_result(peer_ip, ROOT_USER, ROOT_PASSWD, tail_cmd)

    import re
    re_com = re.compile("\[(.*)\]")
    start_time = re_com.search(head_line).group(1)
    end_time = re_com.search(tail_line).group(1)

    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')))
    end_time = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')))

    real_play_time = end_time - start_time

    if (expecting_play_time - real_play_time) > 60:
        return True
    else:
        return False
