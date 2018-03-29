import time

from chunk_delay.const import *
from lib.common.remoter import *


def deploy_base(host, username, password, file_name):
    # kill_cmd = 'killall {0}'.format(file_name)
    # remote_execute(host, username, password, kill_cmd)
    stop_base(host, username, password, file_name)
    makedir_cmd = 'mkdir -p {0}'.format(REMOTE_TEST_PATH)
    remote_execute(host, username, password, makedir_cmd)
    local_file = "{0}/{1}".format(LOCAL_FILE_PATH, file_name)
    remote_file = "{0}/{1}".format(REMOTE_TEST_PATH, file_name)
    copy_file_to(host, username, password, local_file, remote_file)
    chmod_cmd = "chmod +x {0}".format(remote_file)
    remote_execute(host, username, password, chmod_cmd)


def deploy_tcp_server():
    deploy_base(SERVER_HOST, SERVER_USER, SERVER_PWD, TCP_SERVER)


def deploy_tcp_client():
    deploy_base(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, TCP_CLIENT)


def deploy_supp_server():
    deploy_base(SERVER_HOST, SERVER_USER, SERVER_PWD, SUPP_SERVER)


def deploy_supp_client():
    deploy_base(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, SUPP_CLIENT)


def start_tcp_client():
    start_tcp_client_cmd = 'cd {0}; ./{1} --cst-enable --server-ip {2} --server-port {3} --client-ip {4}' \
                           ' --client-port {5} > /dev/null 2>&1'.format(REMOTE_TEST_PATH, TCP_CLIENT, SERVER_HOST,
                                                                        SERVER_START_PORT, CLIENT_HOST,
                                                                        CLIENT_START_PORT)
    remote_execute(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, start_tcp_client_cmd)


def start_tcp_server(send_rate):
    start_tcp_server_cmd = 'cd {0}; ./{1} --cst-enable --cst-rate={2} --server-ip {3} --server-port {4} ' \
                           '> /dev/null 2>&1'.format(REMOTE_TEST_PATH, TCP_SERVER, send_rate, SERVER_HOST,
                                                     SERVER_START_PORT)
    remote_execute(SERVER_HOST, SERVER_USER, SERVER_PWD, start_tcp_server_cmd)


def start_supp_client():
    start_supp_client_cmd = '{0} --server-ip {1} --server-port {2} --client-ip {3} --client-port {4} --cst-enable ' \
                            '-start_req > /dev/null 2>&1'.format(REMOTE_TEST_PATH, SUPP_CLIENT, SERVER_HOST,
                                                                 SERVER_START_PORT, CLIENT_HOST, CLIENT_START_PORT)
    remote_execute(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, start_supp_client_cmd)


def start_supp_server(send_rate, congestion_window):
    start_supp_server_cmd = 'cd {0};./{1} --server-ip {2} --server-port {3} --cst-enable --cst-rate={4} ' \
                            '--cwnd-size={5} > /dev/null 2>&1'.format(REMOTE_TEST_PATH, SUPP_SERVER, SERVER_HOST,
                                                                      SERVER_START_PORT, send_rate, congestion_window)
    remote_execute(SERVER_HOST, SERVER_USER, SERVER_PWD, start_supp_server_cmd)


def stop_base(host, username, password, file_name):
    kill_cmd = 'killall -9 {0}'.format(file_name)
    remote_execute(host, username, password, kill_cmd)


def stop_tcp_client():
    stop_base(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, TCP_CLIENT)


def stop_tcp_server():
    stop_base(SERVER_HOST, SERVER_USER, SERVER_PWD, TCP_SERVER)


def stop_supp_client():
    stop_base(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, SUPP_CLIENT)


def stop_supp_server():
    stop_base(SERVER_HOST, SERVER_USER, SERVER_PWD, SUPP_SERVER)


if __name__ == '__main__':
    start_tcp_server(1)
    time.sleep(2)
    start_tcp_client()

    time.sleep(15)

    stop_tcp_server()
    stop_tcp_client()
