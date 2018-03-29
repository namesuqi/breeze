# coding=utf-8
# control sdk
# author = 'zengyuetian'
# in order to make a clean test, you'd better to reboot test machines before start test

from threading import Timer
from lib.control.gateway_controller import *
from lib.holowan.holowan_const import *
from lib.holowan.create_xml import *
from lib.holowan.setting_handle import delete_path, create_path, start_path, setting_path_params, \
    setting_packet_classifier, setting_path_params_jitter, setting_path_pararms_by_peer_info
from lib.control.ue_analyze_controller import *
from lib.decorator.trace import *


@print_trace
@log_func_args
def add_route(ip, dest, mask, gw, dev):
    """
    peer add route interface
    :param ip:
    :param dest:
    :param mask:
    :param gw:
    :param dev:
    :return:
    """
    route_add_gateway(ip, dest, mask, gw, eth=dev)


@print_trace
@log_func_args
def close_icmp_redirect(ip):
    """
    icmp redirect interface
    :param ip:
    :return:
    """
    icmp_redirect(ip)


@print_trace
@log_func_args
def peer_route_init(delay_time, loss_rate, band_width):
    """
    initization include set delay_time and loss_rate and live_push_ip
    :param delay_time:
    :param loss_rate:
    :param band_width:
    :param live_push_ip:
    :return:
    """
    # setup: clean network
    delete_remote_iptables(PEER_IP)
    delete_remote_iptables(LF_IP)
    delete_remote_iptables(LIVE_PUSH_IP)

    route_delete_gateway(PEER_IP, PUSH_NET, PUSH_NET_MASK, PEER_PUSH_GW_IP, PEER_PUSH_GW_ETH)
    route_delete_gateway(PEER_IP, LF_IP, PUSH_NET_MASK, PEER_PUSH_GW_IP, PEER_PUSH_GW_ETH)
    route_delete_gateway(LF_IP, PEER_IP, PUSH_NET_MASK, PEER_PUSH_GW_IP, LF_DEV)
    route_delete_gateway(LIVE_PUSH_IP, PEER_IP, PUSH_NET_MASK, PEER_PUSH_GW_IP, LIVE_PUSH_DEV)

    # set network
    add_route(PEER_IP, PUSH_NET, PUSH_NET_MASK, gw=PEER_PUSH_GW_IP, dev=PEER_ETH)
    add_route(PEER_IP, LF_IP, PUSH_NET_MASK, gw=PEER_PUSH_GW_IP, dev=PEER_ETH)
    add_route(LF_IP, PEER_IP, PUSH_NET_MASK, gw=PEER_PUSH_GW_IP, dev=LF_DEV)
    add_route(LIVE_PUSH_IP, PEER_IP, PUSH_NET_MASK, gw=PEER_PUSH_GW_IP, dev=LIVE_PUSH_DEV)

    close_icmp_redirect(PEER_IP)
    close_icmp_redirect(LF_IP)
    close_icmp_redirect(LIVE_PUSH_IP)

    gateway_package_delay_and_loss(PEER_PUSH_GW_IP, PEER_PUSH_GW_ETH, delay_time, loss_rate, band_width, LIVE_PUSH_IP)


@print_trace
@log_func_args
def set_gateway_delay(delay_time, loss_rate):
    real_delay_time = delay_time / 2 - BASIC_DELAY_TIME
    one_way_loss_rate = loss_rate / 2.0

    if real_delay_time < 0:
        real_delay_time = 0

    # have 2 review
    peer_route_init(real_delay_time, one_way_loss_rate, ACTUAL_BAND_WIDTH)


flag = 1


@print_trace
@log_func_args
def update_holowan_para((stable_min, stable_max), (jitter_min, jitter_max), bw):
    global flag
    if flag:
        flag = 0
        return stable_min, stable_max, bw, 17
    else:
        flag = 1
        return jitter_min, jitter_max, bw, 3


is_jitter = 0


@print_trace
@log_func_args
def update_jitter_para():
    global is_jitter
    if is_jitter:
        is_jitter = 0
        return JITTER_TIME
    else:
        is_jitter = 1
        return STABLE_TIME


@print_trace
@log_func_args
def set_holowan_jitter2jitter((stable_min, stable_max), (jitter_min, jitter_max), bw):
    """
    this is a function called periodically
    to change HoloWAN configuration
    """

    delete_all_holowan_path()
    create_all_emulation_path()
    create_and_set_free_path()
    set_jitter_path((stable_min, stable_max), (jitter_min, jitter_max), bw)
    set_classifier()


def set_holowan_stable2jitter(delay, loss, bw):
    delete_all_holowan_path()
    create_all_emulation_path()
    create_and_set_free_path()
    set_stable2jitter_path(delay, loss, bw)
    set_classifier()


@print_trace
@log_func_args
def set_jitter_path((stable_min, stable_max), (jitter_min, jitter_max), bandwidth):
    # real task to do for this round
    (min_value, max_value, bw, timer_interval) = update_holowan_para((stable_min, stable_max), (jitter_min, jitter_max),
                                                                     bandwidth)
    for path_name in PEER_PATH_DICT:
        setting_path_params_jitter(path_id=PEER_PATH_DICT[path_name], path_name=path_name, min_value=min_value,
                                   max_value=max_value, bw=bw, loss=0, pltr_delay=25)
    # create a new timer for next task
    t = Timer(timer_interval, set_jitter_path, args=((stable_min, stable_max), (jitter_min, jitter_max), bw))
    t.setDaemon(True)
    t.start()


@print_trace
@log_func_args
def set_stable2jitter_path(delay, loss, bw):
    real_delay_time = delay / 2

    timer_interval = update_jitter_para()

    if is_jitter:
        for path_name in PEER_PATH_DICT:
            setting_path_params(path_id=PEER_PATH_DICT[path_name], path_name=path_name, path_director=PATH_DIRECTOR,
                                pltr_delay_co_devalue=real_delay_time, pltr_loss_random_rate=loss,
                                pltr_bandwidth_rate=bw, prtl_delay_co_devalue=real_delay_time,
                                prtl_loss_random_rate=loss, prtl_bandwidth_rate=bw)
    else:
        for path_name in PEER_PATH_DICT:
            setting_path_params_jitter(path_id=PEER_PATH_DICT[path_name], path_name=path_name,
                                       min_value=real_delay_time + 50, max_value=real_delay_time + 150, bw=bw,
                                       loss=loss, pltr_delay=real_delay_time)

    t = Timer(timer_interval, set_stable2jitter_path, args=(delay, loss, bw))
    t.setDaemon(True)
    t.start()


def delete_all_holowan_path():
    for path_name in PEER_PATH_DICT:
        delete_path(path_id=PEER_PATH_DICT[path_name], path_name=path_name)

    # delete_path(path_id=PATH1_ID, path_name=PATH1_NAME)
    delete_path(path_id=PATH_FREE_ID, path_name=PATH_FREE_NAME)


def create_all_emulation_path():
    for path_name in PEER_PATH_DICT:
        create_path(path_id=PEER_PATH_DICT[path_name], path_name=path_name)
        start_path(path_id=PEER_PATH_DICT[path_name], path_name=path_name)
        # create_path(path_id=PATH1_ID, path_name=PATH1_NAME)
        # start_path(path_id=PATH1_ID, path_name=PATH1_NAME)


def create_and_set_free_path():
    create_path(path_id=PATH_FREE_ID, path_name=PATH_FREE_NAME)
    start_path(path_id=PATH_FREE_ID, path_name=PATH_FREE_NAME)

    setting_path_params(path_id=PATH_FREE_ID, path_name=PATH_FREE_NAME, path_director=PATH_DIRECTOR,
                        pltr_delay_co_devalue=0, pltr_loss_random_rate=0, pltr_bandwidth_rate=1000,
                        prtl_bandwidth_rate=1000, prtl_loss_random_rate=0, prtl_delay_co_devalue=0)


def set_classifier():
    create_xml()
    setting_packet_classifier(src_ip='hard coding', dst_ip='hard coding', path_id='hard coding')


@print_trace
@log_func_args
def set_delay_by_holowan(delay_time, loss_rate, bandwidth):
    real_delay_time = delay_time / 2 - BASIC_DELAY_TIME
    # one_way_loss_rate = loss_rate / 2.0
    one_way_loss_rate = loss_rate

    if real_delay_time < 0:
        real_delay_time = 0

    # delete path
    delete_all_holowan_path()
    # create test path
    create_and_set_free_path()
    create_all_emulation_path()
    # set path params
    for path_name in PEER_PATH_DICT:
        setting_path_params(path_id=PEER_PATH_DICT[path_name], path_name=path_name, path_director=PATH_DIRECTOR,
                            pltr_delay_co_devalue=real_delay_time, pltr_loss_random_rate=one_way_loss_rate,
                            pltr_bandwidth_rate=bandwidth,
                            prtl_delay_co_devalue=real_delay_time, prtl_loss_random_rate=one_way_loss_rate,
                            prtl_bandwidth_rate=bandwidth)

    # set packet classifier, waiting improve
    set_classifier()


def set_delay_by_holowan_version2():
    """
        根据PEER_INFO配置每条不同的path
    :return: 
    """
    # delete path
    delete_all_holowan_path()
    # create test path
    create_all_emulation_path()
    # set path params
    for path_name in PEER_PATH_DICT:
        create_path_params_config(path_id=PEER_PATH_DICT[path_name], path_name=path_name,
                                  **PEER_INFO[path_name]['path_rule'])
        setting_path_pararms_by_peer_info()
    set_classifier()


if __name__ == "__main__":
    # delay = int(sys.argv[1])
    # loss = float(sys.argv[2])
    # set_gateway_delay(delay, loss)
    # set_delay_by_holowan(100, 5, 2)
    # set_holowan_jitter2jitter((10, 50), (50, 200), 2)
    set_holowan_stable2jitter(50, 5, 2)
    time.sleep(100)
