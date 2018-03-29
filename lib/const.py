# coding=utf-8
# author: zengyuetian
import hashlib
import random


def get_random_item(d_list):
    item_key = random.randint(0, len(d_list) - 1)
    item_value = d_list[item_key]
    del d_list[item_key]
    return item_value


NETWORK_RULES = {
    '2M_50MS_1%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 25}, 'loss': 1},
    '2M_50MS_5%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 25}, 'loss': 5},
    '2M_50MS_10%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 25}, 'loss': 10},
    '2M_50MS_15%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 25}, 'loss': 15},
    '2M_50MS_20%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 25}, 'loss': 20},

    '2M_200MS_1%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 1},
    '2M_200MS_5%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 5},
    '2M_200MS_10%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 10},
    '2M_200MS_15%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 15},
    '2M_200MS_20%': {'bandwidth': 2, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 20},

    '1000M_200MS_1%': {'bandwidth': 1000, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 1},
    '1000M_200MS_5%': {'bandwidth': 1000, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 5},
    '1000M_200MS_10%': {'bandwidth': 1000, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 10},
    '1000M_200MS_15%': {'bandwidth': 1000, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 15},
    '1000M_200MS_20%': {'bandwidth': 1000, 'queue_limit': 128, 'delay': {'type': 1, 'value': 100}, 'loss': 20}
}

# udp==play via sdk; http==tcp
RUN_MODE_LIST = ['udp']

# player buffer time
# BUFFER_TIME = [0.1, 0.5, 1, 2]

SDK_PORT = 60000

# sdk and lf prefix
SDK_PREFIX = 8
LF_PREFIX = 9
WRONG_PREFIX = "F"

# Leifeng machine info
# LF_IP = "192.168.8.42"
LF_IP = "192.168.8.44"
LF_IPS = ["192.168.8.44"]
LF_VERSION = "3.17.27"

# PUSH server info
LIVE_PUSH_VERSION = "2.7.11"
PUSH_NET = "192.168.8.40"
PUSH_NET_MASK = "255.255.255.255"
LIVE_PUSH_IP = "192.168.8.40"
LIVE_PUSH_DEV = "enp1s0"

# channel url for udp and http
PLAY_URL = "live_flv/user/wasu?url="
# FILE_URL = "http://flv.srs.cloutropy.com/wasu/time1.flv"
BEIJING_HTTP_FLV_URL = "http://flv.srs.cloutropy.com:8080/wasu/time1.flv"

TIME1_URL = "http://pullsdk.cloutropy.com/live/time1.flv"
# TIME1_URL = "http://flv.srs.cloutropy.com/wasu/time1.flv"
# TIME1_URL = "http://flv.srs.cloutropy.com/wasu/time4.flv"
TIME4_URL = "http://pullsdk.cloutropy.com/live/time4.flv"

PLAY_TIME1_URL = PLAY_URL + TIME1_URL
PLAY_TIME4_URL = PLAY_URL + TIME4_URL

CHANNEL_INFO = [
    (TIME1_URL, hashlib.md5(TIME1_URL).hexdigest().upper()),
    (TIME4_URL, hashlib.md5(TIME4_URL).hexdigest().upper())
]

# list items number must equal with the executing machines number

RULE_LIST_LF = [
    NETWORK_RULES['2M_50MS_1%'],
    NETWORK_RULES['2M_50MS_5%'],
    NETWORK_RULES['2M_50MS_20%'],
    NETWORK_RULES['2M_50MS_20%'],
    NETWORK_RULES['2M_200MS_1%'],
    NETWORK_RULES['2M_200MS_5%'],
    NETWORK_RULES['2M_200MS_20%'],
    NETWORK_RULES['2M_200MS_20%'],
]

# RULE_LIST_LF = [
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
# ]

RULE_LIST_WITHOUT_LF = [
    NETWORK_RULES['2M_50MS_1%'],
    NETWORK_RULES['2M_50MS_5%'],
    NETWORK_RULES['2M_50MS_20%'],
    NETWORK_RULES['2M_200MS_1%'],
    NETWORK_RULES['2M_200MS_5%'],
    NETWORK_RULES['2M_200MS_20%']
]

# RULE_LIST_WITHOUT_LF = [
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_50MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
#     NETWORK_RULES['2M_200MS_20%'],
# ]

sdk_version = '3.19.6'

# peer machine info
PEER_INFO = {
    "192.168.8.41": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.51": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.52": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.53": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.54": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.61": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.55": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.56": {
        'sdk_version': sdk_version, 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_LF)
    },
    "192.168.8.57": {
        'sdk_version': sdk_version, 'lf_prefix': WRONG_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_WITHOUT_LF)
    },
    "192.168.8.58": {
        'sdk_version': sdk_version, 'lf_prefix': WRONG_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_WITHOUT_LF)
    },
    "192.168.8.59": {
        'sdk_version': sdk_version, 'lf_prefix': WRONG_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_WITHOUT_LF)
    },
    "192.168.8.62": {
        'sdk_version': sdk_version, 'lf_prefix': WRONG_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_WITHOUT_LF)
    },
    "192.168.8.71": {
        'sdk_version': sdk_version, 'lf_prefix': WRONG_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_WITHOUT_LF)
    },
    "192.168.8.72": {
        'sdk_version': sdk_version, 'lf_prefix': WRONG_PREFIX, 'play_url': PLAY_TIME1_URL,
        'path_rule': get_random_item(RULE_LIST_WITHOUT_LF)
    },
    # "192.168.8.73": {
    #     'sdk_version': '3.18.31', 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
    #     'path_rule': get_random_item(RULE_LIST_LF)
    # },
    # "192.168.8.74": {
    #     'sdk_version': '3.18.31', 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
    #     'path_rule': get_random_item(RULE_LIST_LF)
    # },
    # "192.168.8.75": {
    #     'sdk_version': '3.18.12', 'lf_prefix': LF_PREFIX, 'play_url': PLAY_TIME1_URL,
    #     'path_rule': get_random_item(RULE_LIST_LF)
    # },
}
