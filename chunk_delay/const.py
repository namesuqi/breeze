from lib.common.path import get_root_path

# file name
TCP_SERVER = 'tcpserver'
TCP_CLIENT = 'tcpclient'

SUPP_SERVER = 'suppv2server'
SUPP_CLIENT = 'suppv2dump'

# test evn info
SERVER_HOST = '192.168.8.40'
# SERVER_USER = 'admin'
# SERVER_PWD = 'yzhxc9!'
SERVER_USER = 'root'
SERVER_PWD = 'Yunshang2014'
SERVER_START_PORT = '20000'


CLIENT_HOST = '192.168.8.41'
# CLIENT_USER = 'admin'
# CLIENT_PWD = 'yzhxc9!'
CLIENT_USER = 'root'
CLIENT_PWD = 'Yunshang2014'
CLIENT_START_PORT = '10001'

REMOTE_TEST_PATH = '/home/admin/chunk_delay_test'
LOCAL_ROOT_PATH = get_root_path()
LOCAL_FILE_PATH = LOCAL_ROOT_PATH + '/misc/chunk_test'
LOCAL_RESULT_PATH = LOCAL_ROOT_PATH + '/result'

# network path
DELAY_PATH_ID = 11
DELAY_PATH_NAME = 'delay_test'
