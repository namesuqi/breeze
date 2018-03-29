from lib.common.path import *

root_path = get_root_path()

# file params

XML_DIR = root_path + '/lib/holowan/setting_xml/'

PATH_CONFIG_NAME = 'path_config'
PATH_PARAMS_CONFIG_NAME = 'path_params_config'
PATH_PACKET_CLASSIFIER_NAME = 'path_packet_classifier'
ONR_PATH_PACKET_CLASSIFIER_NAME = 'one_path_packet_classifier'


# network interface params
URL_PREFIX = "http://192.168.8.199:8080"
HEADERS = {
        "X-HoloWAN-API": "OI_API",
        "Accept": "*/*",
        "Content-type": "text/xml"
}


# path params
ENGINE_ID = 1
PATH_DIRECTOR = 3
# PATH1_NAME = 'test_path1'
# PATH1_ID = 10

PATH_FREE_NAME = 'free_path'
PATH_FREE_ID = 1

STABLE_TIME = 10
JITTER_TIME = 3

QUEUE_DEPTH = '128k'
