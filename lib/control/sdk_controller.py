# coding=utf-8
# author = zengyuetian

from lib.control.player_controller import *
import requests
import json


@log_func_args
def deploy_sdk(ip):
    # kill previous processes
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, kill_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, mkdir_cmd)

    # copy file to remote sdk dir
    local_peer_sdk = "{0}/sdk_peer/{1}/{2}".format(MISC_PATH, ip, SDK_FILE)
    copy_file_to(ip, ROOT_USER, ROOT_PASSWD, local_peer_sdk, REMOTE_SDK)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_SDK)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, chmod_cmd)


@log_func_args
def deploy_upload_sdk(peer_ip):
    # kill previous processes
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(peer_ip, ROOT_USER, ROOT_PASSWD, kill_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH)
    remote_execute(peer_ip, ROOT_USER, ROOT_PASSWD, mkdir_cmd)

    # copy file to remote sdk dir
    upload_peer_sdk = "{0}/web/uploads/peer/{1}".format(ROOT_PATH, SDK_FILE)
    copy_file_to(peer_ip, ROOT_USER, ROOT_PASSWD, upload_peer_sdk, REMOTE_SDK)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_SDK)
    remote_execute(peer_ip, ROOT_USER, ROOT_PASSWD, chmod_cmd)


@log_func_args
def deploy_log_conf(peer_ip):
    # create sdk conf dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_LOG_CONF_PATH)
    remote_execute(peer_ip, ROOT_USER, ROOT_PASSWD, mkdir_cmd)

    # copy file to remote sdk dir
    local_conf_file = "{0}/config/{1}".format(MISC_PATH, SDK_LOG_CONF)
    copy_file_to(peer_ip, ROOT_USER, ROOT_PASSWD, local_conf_file, REMOTE_SDK_LOG_CONF)


@log_func_args
def start_sdk(ip, port=SDK_PORT, lf_prefix=LF_PREFIX):
    """
    start peer sdk with prefix, and use specified leifeng prifix
    :param ip:
    :param port:
    :return:
    """
    p2pclient = "ulimit -c unlimited && cd {0} && nohup ./{1}".format(REMOTE_SDK_PATH, SDK_FILE)
    cmd = "{0} -p {1} -u {2} -x 0000000{3}  > /dev/null 2>&1 &".format(p2pclient, port, SDK_PREFIX, lf_prefix)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, cmd)


@log_func_args
def stop_sdk(ip):
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, kill_cmd)


@log_func_args
def get_sdk_version(ip, port=SDK_PORT):
    # try:
    #     url = "http://{0}:{1}{2}".format(ip, port, "/ajax/version")
    #     headers = dict()
    #     headers["accept"] = 'application/json'
    #     print url
    #
    #     res = requests.get(url, headers=headers, timeout=10)
    #     return json.loads(res.content).get("core", None)
    # except:
    #     return 0

    cmd = "curl http://{0}:{1}{2}".format(ip, port, "/ajax/version")
    result = remote_execute_result(ip, ROOT_USER, ROOT_PASSWD, cmd)
    return json.loads(result).get("core", None)


@log_func_args
def back_up_sdk_log(ip, time_stamp):
    mk_cmd = "mkdir /root/ue/sdk_log"
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, mk_cmd)
    cmd = "cp /root/ue/sdk/yunshang/yunshang.log /root/ue/sdk_log/yunshang_%s.log" % time_stamp
    remote_execute(ip, ROOT_USER, ROOT_PASSWD, cmd)


@log_func_args
def back_up_player_log(player_ip, log_name, time_stamp):
    mk_cmd = "mkdir /root/ue/player_log"
    remote_execute(player_ip, ROOT_USER, ROOT_PASSWD, mk_cmd)
    cmd = "cp /root/ue/pyplayer/%s /root/ue/player_log/%s_%s.log" % (log_name, log_name, time_stamp)
    remote_execute(player_ip, ROOT_USER, ROOT_PASSWD, cmd)


@log_func_args
def remove_logs(player_ip):
    rm_log_cmd = "rm -f /root/ue/player_log/*; rm -f /root/ue/sdk_log/*"
    remote_execute(player_ip, ROOT_USER, ROOT_PASSWD, rm_log_cmd)


@log_func_args
def deploy_lf(ip, lf_num):
    # kill previous processes
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, kill_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(LF_DEPLOY_SDK_PATH)
    remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, mkdir_cmd)

    local_lf_sdk = "{0}/sdk_lf/{1}".format(MISC_PATH, SDK_FILE)
    copy_file_to(ip, ADMIN_USER, ADMIN_PASSWD, local_lf_sdk, LF_SDK)

    chmod_cmd = "chmod +x {0}".format(LF_SDK)
    remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, chmod_cmd)

    for i in range(lf_num):
        cmd = "cp -R {0} {1}/lf_{2}".format(LF_DEPLOY_SDK_PATH, LF_DEPLOY_PATH, i)
        remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, cmd)


@log_func_args
def deploy_lf_clean(ip):
    cmd1 = "rm -rf {0}/*".format(LF_DEPLOY_SDK_PATH)
    remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, cmd1)

    remove_lf_cmd = "rm -rf {0}/lf_*".format(LF_DEPLOY_PATH)
    remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, remove_lf_cmd)


def start_lf_sdk(ip, lf_num, port):
    """
    start lf sdk with prefix
    :param ip:
    :param lf_num:
    :param port:
    :return:
    """
    count = 0
    for i in range(lf_num):
        lf_path = LF_DEPLOY_PATH + "/lf_{0}".format(i)
        p2p_client = "ulimit -c 2000000 && cd {0} && nohup ./{1}".format(lf_path, SDK_FILE)
        cmd = "{0} -p {1} -u {2} > /dev/null 2>&1 &".format(p2p_client, port + count, LF_PREFIX)
        remote_execute(ip, ADMIN_USER, ADMIN_PASSWD, cmd)
        count += 3


def prepare_sdk():
    """
    copy specified version sdk to sdk_peer dir
    copy specified version sdk to sdk_lf dir
    :return: Succeed:True, Fail: False
    """
    ret = False

    # check if all version exist
    peer_versions = []
    for ip in PEER_INFO:
        peer_versions.append(PEER_INFO[ip]['sdk_version'])

    version_set = set(peer_versions)
    version_set.add(LF_VERSION)
    for v in version_set:
        version_sdk = "{0}/sdk/{1}/{2}".format(MISC_PATH, v, SDK_FILE)
        if not os.path.exists(version_sdk):
            return ret

    # clean sdk_peer and sdk_lf dir
    sdk_peer_path = MISC_PATH + "/sdk_peer"
    sdk_lf_path = MISC_PATH + "/sdk_lf"
    cmd = "rm -rf {0}/*".format(sdk_peer_path)
    os.system(cmd)
    cmd = "rm -rf {0}/*".format(sdk_lf_path)
    os.system(cmd)

    # cp specified version sdk to sdk_peer
    for ip in PEER_INFO:
        sdk_ip_path = "{0}/{1}".format(sdk_peer_path, ip)
        cmd = "mkdir -p {0}".format(sdk_ip_path)
        os.system(cmd)
        sdk_version = PEER_INFO[ip]['sdk_version']
        sdk_file = "{0}/sdk/{1}/{2}".format(MISC_PATH, sdk_version, SDK_FILE)
        cmd = "cp {0} {1}".format(sdk_file, sdk_ip_path)
        os.system(cmd)
    print("PEER SDK copied to each ip dir")
    # cp sdk to sdk_lf
    sdk_file = "{0}/sdk/{1}/{2}".format(MISC_PATH, LF_VERSION, SDK_FILE)
    cmd = "cp {0} {1}".format(sdk_file, sdk_lf_path)
    os.system(cmd)
    print("Leifeng SDK copied to Leifeng sdk dir")
    return True


@log_func_args
def confirm_login(peer_ip):
    cmd = "curl http://{0}:{1}{2}".format(peer_ip, SDK_PORT, "/ajax/login")
    retry_times = 5
    while True:
        result = remote_execute_result(peer_ip, ROOT_USER, ROOT_PASSWD, cmd)
        try:
            data = json.loads(result).get("status", None)
            if data == 'E_OK':
                break
            else:
                time.sleep(5)
        except:
            retry_times -= 1
            if retry_times > 0:
                print 'retry {0} times confirm login'.format(retry_times)
            else:
                raise Exception('sdk login fail!')
