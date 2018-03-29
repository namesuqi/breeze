# coding=utf-8
# author: sunxiaolei
"""
run live play with threads
control by UX web
"""

import optparse
import threading
from lib.database.mysqldb import MysqlDB
from lib.control.database_controller import db_add_result
from lib.control.peer_controller import get_peer_p2p
from lib.control.push_controller import deploy_upload_livepush, start_livepush
from lib.control.player_controller import *
from lib.control.sdk_controller import deploy_upload_sdk, start_sdk, stop_sdk, back_up_sdk_log, back_up_player_log, \
    confirm_login
from lib.control.set_gateway import set_delay_by_holowan_version2

# a list to hold ue results for all sdk
# results contents like [{}, {}, ...]
results = []
mutex = threading.Lock()


def custom_play_by_fake_play(play_mode_type, play_time, peer_ip, player_ip, peer_port, player_buffer_time, lf_num,
                             sdk_version=None):
    player_deploy(peer_ip)
    log_name = "{0}/{1}_{2}_{3}_buffer_count.log".format(REMOTE_PLAYER_PATH, play_mode_type, play_time,
                                                         player_buffer_time)
    live_push_version = 'fe_upload'
    p2p_percent = 0

    if play_mode_type == 'udp':
        deploy_upload_sdk(peer_ip)
        start_sdk(peer_ip, lf_prefix=PEER_INFO[peer_ip]['lf_prefix'])
        # peer start time
        time.sleep(8)
        # confirm sdk login successful
        confirm_login(peer_ip)
        # peer play
        player_start(player_ip, PEER_INFO[peer_ip]['play_url'], log_name, player_buffer_time, is_upload=True)
        # play time
        time.sleep(play_time)
        p2p_percent = get_peer_p2p(peer_ip, peer_port)
        stop_sdk(peer_ip)
        player_stop(player_ip)
        channel_url = PEER_INFO[peer_ip]['play_url']

    elif play_mode_type == 'http':
        http_flv_player_start(player_ip, BEIJING_HTTP_FLV_URL, log_name, player_buffer_time)
        sdk_version = 'null'
        time.sleep(play_time)
        player_stop(player_ip)
        channel_url = BEIJING_HTTP_FLV_URL

    else:
        print "##########################################"
        print "##### play mode type is not support! #####"
        print "##########################################"
        exit(0)

    first_image_time = player_first_image_time(player_ip, log_name)
    buffer_number = player_buffering_num(player_ip, log_name)
    total_buffering_time, over_time_count, max_buffering_time = player_buffering_time(player_ip, log_name, 10)
    is_stop = is_play_stop(player_ip, log_name, play_time)

    if PEER_INFO[peer_ip]['lf_prefix'] == WRONG_PREFIX:
        lf_num = 0

    result = {
        "first_image_time": first_image_time,
        "buffer_number": buffer_number,
        "total_buffering_time": total_buffering_time,
        "over_time_count": over_time_count,
        "max_buffering_time": max_buffering_time,
        "is_stop": is_stop,
        "sdk_version": sdk_version,
        "live_push_version": live_push_version,
        "p2p_percent": p2p_percent,
        "peer_ip": peer_ip,
        "lf_number": lf_num,
        "channel_url": channel_url,
        "delay": PEER_INFO[peer_ip]['path_rule']['delay']['value'] * 2,
        "loss": PEER_INFO[peer_ip]['path_rule']['loss'],
        "bandwidth": PEER_INFO[peer_ip]['path_rule']['bandwidth'],
        "queue_depth": PEER_INFO[peer_ip]['path_rule']['queue_limit']
    }
    if mutex.acquire(1):
        results.append(result)
        mutex.release()


def main():
    time_format = '%Y%m%d%H%M%S'
    case_time = time.strftime(time_format, time.localtime())

    parser = optparse.OptionParser("Usage: %prog -p <play mode> -t <play time> -delay <gateway delay> "
                                   "-loss <gateway loss rate> --bf <player buffer time> --lf <lf number> "
                                   "--jitter <jitter enable> --holo <true or false>")
    parser.add_option('-p', dest='play_mode_type', type='string', help='specify play mode [udp or http]')
    parser.add_option('-t', dest='play_time', type='int', help='specify play time [second]')
    parser.add_option('--lf', dest='lf', type='int', default=0, help='specify LF sdk number')
    parser.add_option('--bf', dest='player_buffer_time', type='float', default=1.0,
                      help='specify player_buffer_time [%]')
    parser.add_option('--jitter', dest='jitter', type='string', help='specify network delay jitter or not')
    parser.add_option('--deploy_livepush', dest='deploy_livepush', type='string', help='deploy upload livepush')

    (options, args) = parser.parse_args()
    play_mode_type = options.play_mode_type
    play_time = options.play_time
    player_buffer_time = options.player_buffer_time
    lf = options.lf
    jitter = options.jitter
    deploy_lp = options.deploy_livepush

    if deploy_lp:
        deploy_upload_livepush()
        start_livepush()
        exit(0)

    ################################################################
    # set WAN parameters dynamically
    ################################################################
    if jitter is None:
        set_delay_by_holowan_version2()
    else:
        pass

    for ip in PEER_INFO:
        sdk_version = "fe_upload"
        t = threading.Thread(target=custom_play_by_fake_play, args=(play_mode_type, play_time, ip, ip, SDK_PORT,
                                                                    player_buffer_time, lf, sdk_version))
        t.start()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    db_object = MysqlDB(MYSQL_HOST, MYSQL_UE_USER, MYSQL_PASSWORD, MYSQL_DB_NAME)

    for result in results:
        sdk_version = result.get("sdk_version")
        live_push_version = result.get("live_push_version")
        first_image_time = result.get("first_image_time")
        buffer_number = result.get("buffer_number")
        total_buffering_time = result.get("total_buffering_time")
        over_time_count = result.get("over_time_count")
        max_buffering_time = result.get("max_buffering_time")
        is_stop = str(result.get("is_stop"))
        p2p_percent = result.get("p2p_percent")
        peer_ip = result.get("peer_ip")
        lf_number = result.get("lf_number")
        channel_url = result.get("channel_url")
        delay_time = result.get("delay")
        loss_rate = result.get("loss")
        bandwidth = str(result.get("bandwidth")) + 'M'
        queue_depth = str(result.get("queue_depth")) + 'k'

        real_play_time = play_time - first_image_time

        if jitter is None:
            db_add_result(db_object, MYSQL_TABLE_NAME, case_time, delay_time, loss_rate, play_mode_type, play_time,
                          sdk_version, live_push_version, first_image_time, buffer_number, real_play_time,
                          bandwidth, p2p_percent, lf_number, queue_depth, peer_ip, player_buffer_time,
                          total_buffering_time, over_time_count, max_buffering_time, channel_url, LF_VERSION, is_stop)
        else:
            db_add_result(db_object, MYSQL_TABLE_NAME, case_time, delay_time, loss_rate, play_mode_type, play_time,
                          sdk_version, live_push_version, first_image_time, buffer_number, real_play_time,
                          bandwidth, p2p_percent, lf_number, queue_depth, peer_ip, player_buffer_time,
                          total_buffering_time, over_time_count, max_buffering_time, channel_url, LF_VERSION, is_stop,
                          jitter='true')


if __name__ == '__main__':
    main()
