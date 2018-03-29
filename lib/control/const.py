# coding=utf-8
# const
# author = zengyuetian

from lib.common.path import *
from lib.decorator.log import *
from lib.const import *

SDK_VERSION = "3.16.0"

root_path = get_root_path()
ISO_TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# user and password to access remote machine
ROOT_USER = "root"
ROOT_PASSWD = "Yunshang2014"
ADMIN_USER = "admin"
ADMIN_PASSWD = "yzhxc9!"
LIVE_PUSH_USER = "admin"
LIVE_PUSH_ADMIN_PASSWD = "yzhxc9!"

SDK_FILE = "ys_service_static"
SDK_LOG_CONF = "myslog.conf"
FLV_PARSER = "flv_parse.py"
PLAYER = "main.py"

# sdk location on control machine
LOCAL_SDK = root_path + "/misc/sdk/{0}".format(SDK_FILE)
LOCAL_FLV_PARSER = root_path + "/misc/pyplayer/{0}".format(FLV_PARSER)
LOCAL_PLAYER = root_path + "/misc/pyplayer/{0}".format(PLAYER)

RESULT_PATH = root_path + "/result/"

# sdk location on peer machine
REMOTE_UE_PATH = "/root/ue"
REMOTE_SDK_PATH = REMOTE_UE_PATH + "/sdk"
REMOTE_SDK = REMOTE_SDK_PATH + "/{0}".format(SDK_FILE)
REMOTE_SDK_LOG_CONF_PATH = REMOTE_SDK_PATH + "/conf"
REMOTE_SDK_LOG_CONF = REMOTE_SDK_LOG_CONF_PATH + "/{0}".format(SDK_LOG_CONF)

# live push bin path
LIVE_PUSH_FILE = "livepush"
REMOTE_LIVE_PUSH_PATH = '/home/admin/ue_test'
REMOTE_LIVE_PUSH = REMOTE_LIVE_PUSH_PATH + '/' + LIVE_PUSH_FILE

# player on peer machine
REMOTE_PLAYER_PATH = REMOTE_UE_PATH + "/pyplayer"
REMOTE_PLAYER = REMOTE_PLAYER_PATH + "/" + PLAYER
REMOTE_FLV_PARSER = REMOTE_PLAYER_PATH + "/" + FLV_PARSER

PEER_PATH_DICT = dict()
# peer ip and path id
holowan_path_id = 2
for ip in PEER_INFO:
    PEER_PATH_DICT[ip] = holowan_path_id
    holowan_path_id += 1

#
# PEER_PATH_DICT = {
#     "192.168.8.41": 10,
#     "192.168.8.51": 11,
#     "192.168.8.52": 12,
#     "192.168.8.53": 13,
#     "192.168.8.54": 14
# }
PEER_ETH = "enp1s0"

# gateway machine info
PEER_PUSH_GW_IP = "192.168.8.42"
PEER_PUSH_GW_ETH = "enp1s0"

# gateway machine info
# PEER_PUSH_GW2_IP = "192.168.1.43"
# PEER_PUSH_GW2_ETH = "enp1s0"

# network params
BASIC_DELAY_TIME = 0

SAMPLE_NUM = 10
PLAY_DURATION = 30
LOGIN_DUATION = 3
REGULAR_TIME_PLAY_DURATION = 20
LAST_TIME_PLAY_DURATION = 300

MODE_LIST = ["first_image_time", "buffer_number"]

# NETWORK_CONGESTION_LIST = ["深队拥塞", "浅队拥塞", "突发延迟"]
# NETWORK_CONGESTION_LIST = ["deep", "shallow", "burst"]

MODE_UDP = "udp"
MODE_HTTP = "http"

UDP_LOG_NAME = "udp_stat.log"
HTTP_LOG_NAME = "http_stat.log"

MODE_FIRST_IMAGE_TIME = "first_image"
MODE_BUFFERING_NUM = "buffer_num"

RESULT_FILE = root_path + "/result/result.txt"

# csv params
CSV_HTTP_FILE = root_path + "/result/result_http_data.csv"
CSV_FILE = root_path + "/result/result_data.csv"
CSV_HEADER = [u"延迟", u"丢包", u"指标", u"播放次数", u"协议", u"平均值", u"中值", u"最大值", u"方差值",
              u"指标", u"播放时长", u"卡顿次数"]

CSV_DATABASE_HEADER = [u"延迟和丢包", u"版本", u"样本数", u"起播时间", u"卡顿次数", u"卡顿时长", u"p2p占比", u"版本", u"样本数",
                       u"起播时间", u"卡顿次数", u"卡顿时长"]
START_UP_TIME = u"启播时间"
BUFFERING_NUMBER = u"卡顿次数"

MYSQL_HOST = "192.168.1.61"
MYSQL_PORT = 3306
MYSQL_UE_USER = "ppc"
MYSQL_PASSWORD = "yunshang2014"
MYSQL_TABLE_NAME = "ue_performance"
MYSQL_DB_NAME = "user_experience"

STUN_THUNDER_IP = "192.168.8.43"
STUN_THUNDER_PORT = "8000"

LF_DEV = "enp3s0"
LF_PORT_START = 20000
LF_DEPLOY_PATH = "/home/admin/ue/lf_deploy"
LF_DEPLOY_SDK_PATH = LF_DEPLOY_PATH + "/sdk"
LF_SDK = LF_DEPLOY_PATH + "/sdk/%s" % SDK_FILE

# excel param
EXCEL_PATH = root_path + "/result/"
EXCEL_ROW0 = [u"延迟和丢包", u"版本", u"样本数", u"起播时间", u"卡顿次数", u"卡顿时长", u"卡顿率", u"p2p占比", u"lf数量", u"频道码率", u"带宽限制"]
