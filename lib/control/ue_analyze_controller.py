# coding=utf-8
# author = 'donghao'

from lib.dm.stats import *
from lib.control.database_controller import *


# @print_trace
# @log_func_args
# def condition_select(db_object, sdk_version, live_push_version, mode, play_duration, lf, start_time, end_time,
#                      band_width):
#     result_list = []
#     for delay_loss_tuple in DELAY_LOSS_LIST:
#         delay = delay_loss_tuple[0]
#         loss = delay_loss_tuple[-1]
#         tmp_list = select_full_condition(db_object, mode, delay, loss, sdk_version, live_push_version,
#                                          play_duration, lf, start_time, end_time, band_width)
#         if tmp_list is not None:
#             result_list.append(tmp_list)
#
#     return result_list


def condition_select_v2(db_object, **conditions):
    """
        new method for data collect. 
    """

    network_rules = list()
    delay_loss_list = list()
    results = list()
    for value in PEER_INFO.values():
        network_rules.append(value['path_rule'])
    network_rules = reduce(lambda x, y: x if y in x else x + [y], [[], ] + network_rules)

    for rule in network_rules:
        delay_loss_list.append((rule['delay']['value'] * 2, rule['loss']))
    for delay, loss in delay_loss_list:
        conditions['delay'] = delay
        conditions['loss_rate'] = loss
        tuple_result = db_object.select(MYSQL_TABLE_NAME, '*', **conditions)
        results.append(result_parser(tuple_result))
    for i in results:
        print i
    return results


def result_parser(data):
    """
        calculate data
        table structure:
|id|case_start_time|delay|loss_rate|mode|sdk_version|live_push_version|first_image_time|buffer_number|play_duration|real_play_duration|...
|band_width|p2p_percent|lf_number|queue|peer_ip|player_buffer_time|jitter|total_buffer_time|over_time_count|max_buffering_time|channel_url|...
|lf_version|is_stop|
    """
    startup_times = list()
    buffering_numbers = list()
    buffering_times = list()
    p2ps = list()
    lf_numbers = list()
    sample_number = 0
    condition_tag = str(data[0][2]) + 'ms_' + str(int(data[0][3])) + '%'
    bandwidth = data[0][11]
    channel_rate = str(int(bandwidth.replace('M', '')) / 2) + 'M'
    version = 'sdk' + data[0][5] + '/livepush' + data[0][6]
    if data is None:
        return None
    for row in data:
        if row[23] == "True":
            print 'delete', row[23]
            continue
        else:
            startup_times.append(row[7])
            buffer_num_tmp = row[9] / row[10] * row[8]
            buffering_numbers.append(buffer_num_tmp)
            p2ps.append(float(row[12]))
            lf_numbers.append(row[13])
            buffering_times.append(row[18])
            sample_number += 1
    startup_time = Stats.avg(startup_times)
    buffering_number = Stats.avg(buffering_numbers)
    buffering_time = Stats.avg(buffering_times)
    buffering_ratio = buffering_time / data[0][9]
    p2p = Stats.avg(p2ps)
    lf_number = Stats.avg(lf_numbers)
    result = [
        condition_tag,
        version,
        sample_number,
        startup_time,
        buffering_number,
        buffering_time,
        buffering_ratio,
        p2p,
        lf_number,
        channel_rate,
        bandwidth
    ]
    return result


# @print_trace
# @log_func_args
# def calculate():
#     tmp_res = db_select_result(MYSQL_TABLE_NAME, "count(DISTINCT sdk_version, 'mode')")
#     count_col = int(tmp_res[0][0])
#     return count_col


# @print_trace
# @log_func_args
# def select_specify_condition(db_object, mode, delay, loss_rate, sdk_version=SDK_VERSION,
#                              live_push_version=LIVE_PUSH_VERSION):
#     """
#     :param db_object:
#     :param mode:
#     :param delay:
#     :param loss_rate:
#     :param sdk_version:
#     :param live_push_version:
#     :return:
#     """
#     if MODE_UDP == mode:
#         records = db_select_result(db_object, MYSQL_TABLE_NAME, "*", delay=delay, loss_rate=loss_rate,
#                                    sdk_version=sdk_version, live_push_version=live_push_version)
#     else:
#         records = db_select_result(db_object, MYSQL_TABLE_NAME, "*", delay=delay, loss_rate=loss_rate, mode=mode,
#                                    live_push_version=live_push_version)
#
#     return parse_tuple_res(records, delay, loss_rate, sdk_version, live_push_version=live_push_version)
#
#
# @print_trace
# @log_func_args
# def select_full_condition(db_object, mode, delay, loss_rate, sdk_version, live_push_version, play_duration, lf,
#                           start_time, end_time, band_width):
#     """
#     :param db_object:
#     :param mode:
#     :param delay:
#     :param loss_rate:
#     :param sdk_version:
#     :param live_push_version:
#     :param play_duration:
#     :param lf:
#     :return:
#     """
#     if mode == 'udp':
#         records = db_select_result(db_object, MYSQL_TABLE_NAME, "*", delay=delay, loss_rate=loss_rate,
#                                    sdk_version=sdk_version, live_push_version=live_push_version,
#                                    play_duration=play_duration, lf_number=lf, start_time=start_time, end_time=end_time,
#                                    band_width=band_width)
#     elif mode == 'http':
#         records = db_select_result(db_object, MYSQL_TABLE_NAME, "*", delay=delay, loss_rate=loss_rate, mode=mode,
#                                    play_duration=play_duration, start_time=start_time, end_time=end_time,
#                                    band_width=band_width)
#     else:
#         print "##################################"
#         print "######   condition error    ######"
#         print "##################################"
#         exit(0)
#
#     return parse_tuple_res(records, delay, loss_rate, sdk_version, live_push_version=live_push_version)


# @print_trace
# @log_func_args
# def select_by_time(db_object, start_time, end_time):
#     """
#     :param db_object:
#     :param start_time:
#     :param end_time:
#     :return:
#     """
#     condition = 'case_start_time >= {0} and case_start_time <= {1}'.format(start_time, end_time)
#     records = db_fuzzy_select_result(db_object, MYSQL_TABLE_NAME, condition, "*")
#     # print records
#     return parse_tuple_time_res(records)


# @print_trace
# @log_func_args
# def parse_tuple_time_res(tuple_records):
#     """
#     parse tuple and return a list
#     :param tuple_records:
#     """
#     if tuple_records is None:
#         return None
# 
#     res_list = []
# 
#     for row in tuple_records:
#         index = "{0}ms_{1}%".format(row[2], row[3])
#         if row[4] == MODE_UDP:
#             version = "udp_" + row[5]
#         else:
#             version = row[4]
#         first_image_time = row[7]
#         buffer_time = row[8]
# 
#         record = [
#             index,
#             version,
#             1,
#             first_image_time,
#             buffer_time
#         ]
#         # print "record:", record
#         res_list.append(record)
# 
#     return res_list


# @print_trace
# @log_func_args
# def parse_tuple_res(tuple_records, delay, loss_rate, sdk_version, live_push_version):
#     """
#     parse tuple and return a list
#     :param tuple_records:
#     :param delay:
#     :param loss_rate:
#     :param sdk_version:
#     :param live_push_version:
#     :return: res_list
#     """
#     if tuple_records is None:
#         return None
#
#     udp_time_list = []
#     http_time_list = []
#     udp_buffer_num_list = []
#     http_buffer_num_list = []
#     udp_p2p_list = []
#     udp_total_buffering_time = []
#     http_total_buffering_time = []
#
#     udp_sample_num = 0
#     http_sample_num = 0
#
#     print tuple_records
#
#     for row in tuple_records:
#         if MODE_UDP == row[4]:
#             udp_sample_num += 1
#             udp_time_list.append(row[7])
#             buffer_num_tmp = row[9] / row[10] * row[8]
#             udp_buffer_num_list.append(buffer_num_tmp)
#             udp_total_buffering_time.append(row[18])
#             if row[12] not in ['', None]:
#                 p2p_percent = float(row[12])
#                 udp_p2p_list.append(p2p_percent)
#
#         elif MODE_HTTP == row[4]:
#             http_sample_num += 1
#             http_time_list.append(row[7])
#             buffer_num_tmp = row[9] / row[10] * row[8]
#             http_buffer_num_list.append(buffer_num_tmp)
#             http_total_buffering_time.append(row[18])
#
#     # remove_max_number_of_list(udp_time_list)
#     udp_average_time = Stats.avg(udp_time_list)
#     http_average_time = Stats.avg(http_time_list)
#     print http_time_list
#     print http_average_time
#
#     udp_buffer_num = Stats.avg(udp_buffer_num_list)
#     http_buffer_num = Stats.avg(http_buffer_num_list)
#     print http_buffer_num_list
#     print http_buffer_num
#
#     udp_average_buffering_time = Stats.avg(udp_total_buffering_time)
#     http_average_buffering_time = Stats.avg(http_total_buffering_time)
#
#     udp_p2p_percent_num = Stats.avg(udp_p2p_list)
#
#     # real_udp_buffer_num = row[10] / 60.0 *
#     index = "{0}ms_{1}%".format(delay, loss_rate)
#     udp_sdk = "sdk_" + sdk_version + '/live_push_version' + live_push_version
#
#     res_list = [
#         index,
#         udp_sdk,
#         udp_sample_num,
#         udp_average_time,
#         udp_buffer_num,
#         udp_average_buffering_time,
#         udp_p2p_percent_num,
#         MODE_HTTP,
#         http_sample_num,
#         http_average_time,
#         http_buffer_num,
#         http_average_buffering_time
#     ]
#     return res_list


# def remove_max_number_of_list(in_list):
#     in_list.remove(Stats.maximum(in_list))
#     return in_list
