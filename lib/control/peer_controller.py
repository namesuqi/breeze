# coding=utf-8
# control sdk
# author = 'zengyuetian'
# in order to make a clean test, you'd better to reboot test machines before start test

from lib.control.sdk_controller import *
from lib.control.player_controller import *
from lib.control.gateway_controller import *
from lib.control.push_controller import *
from lib.control.collect_result import *
from lib.control.ue_analyze_controller import *
from lib.decorator.trace import *
from lib.dm.stats import *


@print_trace
@log_func_args
def peer_deploy(ip):
    """
    peer peer_deploy sdk interface
    :param ip:
    :return:
    """
    deploy_sdk(ip)


@print_trace
@log_func_args
def peer_start(ip):
    """
    peer start sdk interface
    :param ip:
    :return:
    """
    start_sdk(ip)


@print_trace
@log_func_args
def peer_stop(ip):
    """
    peer start sdk interface
    :param ip:
    :return:
    """
    stop_sdk(ip)


@print_trace
@log_func_args
def peer_route(ip, dest, mask, gw):
    """
    peer add route interface
    :param ip:
    :param dest:
    :param mask:
    :param gw:
    :return:
    """
    route_add_gateway(ip, dest, mask, gw, eth=PEER_ETH)


@print_trace
@log_func_args
def peer_redirect(ip):
    """
    icmp redirect interface
    :param ip:
    :return:
    """
    icmp_redirect(ip)


@print_trace
@log_func_args
def peer_wait(sec):
    """
    wait for deploy or start ends.
    :param sec:
    :return:
    """
    time.sleep(sec)


@print_trace
@log_func_args
def deploy_files():
    """
    deploy sdk and player
    :return:
    """
    peer_deploy(PEER_IP)
    player_deploy(PEER_IP)


@print_trace
@log_func_args
def peer_route_init(delay_time, loss_rate, band_width, live_push_ip):
    """
    initization include set delay_time and loss_rate and live_push_ip
    :param delay_time:
    :param loss_rate:
    :param band_width:
    :param live_push_ip:
    :return:
    """
    # setup network
    delete_remote_iptables(PEER_IP)

    route_delete_gateway(PEER_IP, PUSH_NET, PUSH_NET_MASK, PEER_PUSH_GW_IP, PEER_PUSH_GW_ETH)

    peer_route(PEER_IP, PUSH_NET, PUSH_NET_MASK, PEER_PUSH_GW_IP)

    peer_redirect(PEER_IP)
    gateway_package_delay_and_loss(PEER_PUSH_GW_IP, PEER_PUSH_GW_ETH, delay_time, loss_rate, band_width, live_push_ip)


@print_trace
@log_func_args
def peer_play_stop():
    """
    stop player
    :return:
    """
    player_stop(PEER_IP)
    # peer_stop(PEER_IP)


@print_trace
@log_func_args
def peer_restart():
    pass


@print_trace
@log_func_args
def get_ue_result(delay_time, loss_rate):
    """
    UE get result cases entry function
    :param delay_time:
    :param loss_rate:
    :return:
    """
    db_object = MysqlDB(MYSQL_HOST, MYSQL_UE_USER, MYSQL_PASSWORD, MYSQL_DB_NAME)
    time_format = '%Y%m%d%H%M%S'
    case_time = time.strftime(time_format, time.localtime())

    peer_deploy(PEER_IP)
    player_deploy(PEER_IP)
    real_delay_time = delay_time / 2 - BASIC_DELAY_TIME
    one_way_loss_rate = loss_rate / 2.0

    if real_delay_time < 0:
        real_delay_time = 0

    # have 2 review
    peer_route_init(real_delay_time, one_way_loss_rate, ACTUAL_BAND_WIDTH, LIVE_PUSH_IP)

    cur_live_push_version = get_live_push_version(LIVE_PUSH_IP)
    peer_start(PEER_IP)
    peer_wait(LOGIN_DUATION)

    udp_log_name = "{0}/{1}_{2}_{3}_{4}".format(REMOTE_PLAYER_PATH, delay_time, loss_rate, 0, UDP_LOG_NAME)
    http_log_name = "{0}/{1}_{2}_{3}_{4}".format(REMOTE_PLAYER_PATH, delay_time, loss_rate, 0, HTTP_LOG_NAME)
    player_start(PEER_IP, BEIJING_URL, udp_log_name)

    player_wait(PLAY_DURATION)

    # stop play
    peer_play_stop()
    cur_sdk_version = get_sdk_version(PEER_IP)
    print "cur_sdk_version:{0}".format(cur_sdk_version)
    # stop sdk
    peer_stop(PEER_IP)
    back_up_sdk_log(PEER_IP, case_time)

    http_flv_player_start(PEER_IP, BEIJING_HTTP_FLV_URL, http_log_name)
    player_wait(PLAY_DURATION)
    peer_play_stop()

    udp_t = player_first_image_time(PEER_IP, udp_log_name)
    http_t = player_first_image_time(PEER_IP, http_log_name)

    udp_buffer_num = player_buffering_num(PEER_IP, udp_log_name)
    http_buffer_num = player_buffering_num(PEER_IP, http_log_name)

    udp_real_play_duration = float("%.2f" % (PLAY_DURATION - udp_t))
    http_real_play_duration = float("%.2f" % (PLAY_DURATION - http_t))

    # have to review
    # res_file_name = RESULT_PATH + "{0}ms_{1}%_.txt".format(delay_time, loss_rate)
    # write_case_result(res_file_name, udp_t, http_t, udp_buffer_num, http_buffer_num)

    # every case has to write two records into mysql
    # -1 means startup failed
    if udp_t != -1:
        db_add_result(db_object, MYSQL_TABLE_NAME, case_time, delay_time, loss_rate, MODE_UDP, PLAY_DURATION,
                      cur_sdk_version, cur_live_push_version, udp_t, udp_buffer_num, udp_real_play_duration,
                      ACTUAL_BAND_WIDTH)
    if http_t != -1:
        db_add_result(db_object, MYSQL_TABLE_NAME, case_time, delay_time, loss_rate, MODE_HTTP, PLAY_DURATION,
                      cur_sdk_version, cur_live_push_version, http_t, http_buffer_num, http_real_play_duration,
                      ACTUAL_BAND_WIDTH)


# @print_trace
# @log_func_args
# def write_result_txt(file_name, mode, udp_buf_num=0, http_buf_num=0, udp_list=[], http_list=[]):
#     """
#     :param file_name:
#     :param mode:
#     :param udp_buf_num:
#     :param http_buf_num:
#     :param udp_list:
#     :param http_list:
#     :return:
#     """
#     output_file = open(file_name, "w")
#     if "first_image" == mode:
#         output_file.write(MODE_UDP)
#         for i in udp_list:
#             if type(i) == float:
#                 i = float("%.2f" % i)
#             output_file.write("," + str(i))
#         output_file.write("\n")
#         output_file.write(MODE_HTTP)
#         for i in http_list:
#             if type(i) == float:
#                 i = float("%.2f" % i)
#             output_file.write("," + str(i))
#     else:
#         output_file.write("{0},{1}\n".format(MODE_UDP, str(udp_buf_num)))
#         output_file.write("{0},{1}\n".format(MODE_HTTP, str(http_buf_num)))
#     output_file.close()


# @print_trace
# @log_func_args
# def ue_buffering_time_test(delay_time, loss_rate):
#     """
#     init UE test interface
#     obsolete temporary
#     :param delay_time:
#     :param loss_rate:
#     :return:
#     """
#     peer_deploy(PEER_IP)
#     player_deploy(PEER_IP)
#
#     real_delay_time = delay_time - BASIC_DELAY_TIME
#
#     if real_delay_time < 0:
#         real_delay_time = 0
#
#     peer_route_init(real_delay_time, loss_rate, ACTUAL_BAND_WIDTH, LIVE_PUSH_IP)
#
#     # delay_time += BASIC_DELAY_TIME
#
#     # start sdk
#     udp_log_name = "{0}/{1}_{2}_{3}_{4}_{5}".format(REMOTE_PLAYER_PATH, delay_time, loss_rate,
#                                                     "buffering_num", 0, UDP_LOG_NAME)
#     http_log_name = "{0}/{1}_{2}_{3}_{4}_{5}".format(REMOTE_PLAYER_PATH, delay_time, loss_rate,
#                                                      "buffering_num", 0, HTTP_LOG_NAME)
#     peer_start(PEER_IP)
#     peer_wait(LOGIN_DUATION)
#     player_start(PEER_IP, BEIJING_URL, udp_log_name)
#     http_flv_player_start(PEER_IP, BEIJING_HTTP_FLV_URL, http_log_name)
#     # start player
#
#     player_wait(LAST_TIME_PLAY_DURATION)
#     peer_play_stop()
#
#     udp_buffer_num = player_buffering_num(PEER_IP, udp_log_name)
#     http_buffer_num = player_buffering_num(PEER_IP, http_log_name)
#
#     print "----------------------------------------------------------------------------------------------"
#     print "{0} delay_time:{1}, loss_rate:{2}, play_time:{3}s  test: buffer num is {4}".format(
#         "udp", delay_time, loss_rate, LAST_TIME_PLAY_DURATION, udp_buffer_num)
#     print "{0} delay_time:{1}, loss_rate:{2}, play_time:{3}s  test: buffer num is {4}".format(
#         "http", delay_time, loss_rate, LAST_TIME_PLAY_DURATION, http_buffer_num)
#     print "----------------------------------------------------------------------------------------------"
#
#     res_file_name = RESULT_PATH + "{0}ms_{1}%_buffer_number.txt".format(delay_time, loss_rate)
#     write_result_txt(res_file_name, MODE_BUFFERING_NUM, udp_buffer_num, http_buffer_num, None, None)


# @print_trace
# @log_func_args
# def ue_first_image_test(delay_time, loss_rate):
#     """
#     init UE test interface
#     :param delay_time:
#     :param loss_rate:
#     :return:
#     """
#     peer_deploy(PEER_IP)
#     player_deploy(PEER_IP)
#     real_delay_time = delay_time - BASIC_DELAY_TIME
#
#     if real_delay_time < 0:
#         real_delay_time = 0
#
#     peer_route_init(real_delay_time, loss_rate, ACTUAL_BAND_WIDTH, LIVE_PUSH_IP)
#
#     udp_time_list = []
#     http_time_list = []
#
#     for i in range(SAMPLE_NUM):
#             # start sdk
#         peer_start(PEER_IP)
#         peer_wait(LOGIN_DUATION)
#
#         udp_log_name = "{0}/{1}_{2}_{3}_{4}_{5}".format(REMOTE_PLAYER_PATH, delay_time, loss_rate,
#                                                         "first_image_time", i+1, UDP_LOG_NAME)
#         http_log_name = "{0}/{1}_{2}_{3}_{4}_{5}".format(REMOTE_PLAYER_PATH, delay_time, loss_rate,
#                                                          "first_image_time", i+1, HTTP_LOG_NAME)
#         player_start(PEER_IP, BEIJING_URL, udp_log_name)
#         http_flv_player_start(PEER_IP, BEIJING_HTTP_FLV_URL, http_log_name)
#         # start player
#
#         player_wait(REGULAR_TIME_PLAY_DURATION)
#
#         # validate first image time
#         udp_t = player_first_image_time(PEER_IP, udp_log_name)
#         udp_time_list.append(udp_t)
#
#         http_t = player_first_image_time(PEER_IP, http_log_name)
#         http_time_list.append(http_t)
#
#         print "----------------------------------------------------------------------------------------------"
#         print "{0} delay_time:{1}, loss_rate:{2}  test{3}: First play time is {4}".format(
#             "udp", delay_time, loss_rate, i+1, udp_t)
#         print "{0} delay_time:{1}, loss_rate:{2}  test{3}: First play time is {4}".format(
#             "http", delay_time, loss_rate, i+1, http_t)
#         print "----------------------------------------------------------------------------------------------"
#
#         # stop sdk and remove log
#         peer_play_stop()
#
#     udp_result_list = []
#     udp_average_time = Stats.avg(udp_time_list)
#     udp_median_time = Stats.median(udp_time_list)
#     udp_max_time = Stats.maximum(udp_time_list)
#     udp_variance_time = Stats.variance2(udp_time_list)
#
#     udp_result_list.append(udp_average_time)
#     udp_result_list.append(udp_median_time)
#     udp_result_list.append(udp_max_time)
#     udp_result_list.append(udp_variance_time)
#
#     http_result_list = []
#     http_average_time = Stats.avg(http_time_list)
#     http_median_time = Stats.median(http_time_list)
#     http_max_time = Stats.maximum(http_time_list)
#     http_variance_time = Stats.variance2(http_time_list)
#
#     http_result_list.append(http_average_time)
#     http_result_list.append(http_median_time)
#     http_result_list.append(http_max_time)
#     http_result_list.append(http_variance_time)
#
#     print ""
#     print "First image time list udp:", udp_time_list
#     print "First image time list http:", http_time_list
#     print "Sampler Number is: {0}, delay time is: {1}, loss_rate is: {2}".format(SAMPLE_NUM, delay_time, loss_rate)
#     print "**********************************************************************************************"
#     print "{0}-First Play Time: average: {1}s, median: {2}s, max: {3}s".format("udp", udp_average_time,
#                                                                             udp_median_time, udp_max_time)
#     print "{0}-First Play Time: average: {1}s, median: {2}s, max: {3}s".format("http", http_average_time,
#                                                                             http_median_time, http_max_time)
#     print "**********************************************************************************************"
#     print ""
#
#     res_file_name = RESULT_PATH + "{0}ms_{1}%_first_image_time.txt".format(delay_time, loss_rate)
#     write_result_txt(res_file_name, MODE_FIRST_IMAGE_TIME, 0, 0, udp_result_list, http_result_list)


@print_trace
@log_func_args
def get_peer_p2p(ip, port):
    url = "http://{0}:{1}{2}".format(ip, port, "/ajax/report")
    headers = dict()
    headers["accept"] = 'application/json'
    # print url
    res = requests.get(url, headers=headers)
    return json.loads(res.content).get("p2p_percent", None)


if __name__ == "__main__":

    time_format = '%Y%m%d%H%M%S'
    case_start_time = time.strftime(time_format, time.localtime())

    if len(sys.argv) == 1:
        print "default parameter:"
        for delay in DELAY_TIME_LIST:
            for loss in LOSS_RATE_LIST:
                print "delay:{0}ms, loss_rate:{1}%".format(delay, loss)
                get_ue_result(delay, loss)
    elif len(sys.argv) == 3:
        print "please make sure cmd like: python peer_controller delay loss"
        print "Parameter delay:{0}ms and loss_rate:{1}%".format(sys.argv[1], sys.argv[2])
        get_ue_result(int(sys.argv[1]), float(sys.argv[2]))

    # case_stop_time = time.strftime(time_format, time.localtime())
    tmp_csv_name = root_path + "/result/" + case_start_time + ".csv"
    get_database_res_from_time(case_start_time, tmp_csv_name)
