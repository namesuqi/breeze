# coding=utf-8
# control leifeng
# author: zengyuetian

from lib.control.sdk_controller import *
from lib.control.stun_server import *


@print_trace
def start_deploy_lf(ip, lf_num):
    deploy_lf(ip, lf_num)


@print_trace
def start_lf(ip, lf_num, port=LF_PORT_START):
    start_lf_sdk(ip, lf_num, port)


@print_trace
def stop_lf(ip):
    stop_sdk(ip)
    deploy_lf_clean(ip)


@print_trace
def get_lf_peer_id_list(ip, lf_num, port=LF_PORT_START):
    peer_ids = list()
    count = 0
    for i in range(lf_num):
        url = "http://{0}:{1}{2}".format(ip, port + count, "/ajax/conf")
        headers = dict()
        headers["accept"] = 'application/json'
        headers["content-type"] = 'application/json'
        res = requests.get(url, headers=headers)
        peer_id = json.loads(res.content).get("peer_id", None)
        # cmd = "curl http://{0}:{1}{2}".format(ip, port + count, "/ajax/conf")
        # result = remote_execute_result(ip, ROOT_USER, ROOT_PASSWD, cmd)
        # peer_id = json.loads(result).get("peer_id", None)
        peer_ids.append(peer_id)
        count += 3
    if len(peer_ids) != lf_num:
        print "#########################################"
        print "## JOIN LF FAIL!!! EXPECT {0} ,REAL {1} ##".format(lf_num, len(peer_ids))
        print "#########################################"
        exit(0)

    return peer_ids


@print_trace
def get_lf_peer_ids(ip, lf_num):
    """
    get lf sdk peer ids from yunshang.conf
    :param ip:
    :param lf_num:
    :param port:
    :return:
    """
    ids = list()
    for i in range(lf_num):
        lf_path = LF_DEPLOY_PATH + "/lf_{0}".format(i)
        cmd = "cat {0}/yunshang/yunshang.conf".format(lf_path)
        line = remote_execute_result(ip, ADMIN_USER, ADMIN_PASSWD, cmd)
        peer_id = json.loads(line).get("peer_id", None)
        print(peer_id)
        ids.append(peer_id)
    return ids
