from lib.common.remoter import remote_execute_result, copy_file_from
from chunk_delay.const import *


def collect_packet_jitter(mode):
    client_max_time = get_latest_packet_jitter(CLIENT_HOST)
    server_max_time = get_latest_packet_jitter(SERVER_HOST)
    client_rn = '/packet_jitter-' + client_max_time
    client_ln = '/' + mode + '_client' + '_packet_jitter-' + client_max_time
    server_rn = '/packet_jitter-' + server_max_time
    server_ln = '/' + mode + '_server' + '_packet_jitter-' + server_max_time
    client_remote_file_name = REMOTE_TEST_PATH + client_rn
    client_local_file_name = LOCAL_RESULT_PATH + client_ln
    server_remote_file_name = REMOTE_TEST_PATH + server_rn
    server_local_file_name = LOCAL_RESULT_PATH + server_ln
    copy_file_from(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, client_remote_file_name, client_local_file_name)
    copy_file_from(SERVER_HOST, SERVER_USER, SERVER_PWD, server_remote_file_name, server_local_file_name)


def get_latest_packet_jitter(hostname):
    cmd = 'ls {0} | grep packet_jitter-'.format(REMOTE_TEST_PATH)
    if hostname == CLIENT_HOST:
        result = remote_execute_result(CLIENT_HOST, CLIENT_USER, CLIENT_PWD, cmd)
    elif hostname == SERVER_HOST:
        result = remote_execute_result(SERVER_HOST, SERVER_USER, SERVER_PWD, cmd)
    else:
        print "######################################"
        print "######   PLS CHECK HOSTNAME!    ######"
        print "######################################"
        exit(0)
    time_list = result.replace('\n', '').split('packet_jitter-')
    return str(max(time_list))


if __name__ == '__main__':
    # collect_packet_jitter('tcp')
    collect_packet_jitter('rush')
