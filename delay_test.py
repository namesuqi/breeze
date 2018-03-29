import optparse

from chunk_delay.collector import collect_packet_jitter
from chunk_delay.delay_parser import delay_parser
from chunk_delay.deployer import *
from lib.holowan.setting_handle import *


def main():
    parser = optparse.OptionParser(
        "Usage: %prog -p <play mode> -t <play time> --rtt <round trip time> --loss <packet loss probability> "
        "--rate <send rate> --ratio <bandwidth ratio>"
    )
    parser.add_option('-p', dest='play_mode_type', type='string', help='specify play mode [rush or tcp]')
    parser.add_option('-t', dest='play_time', type='int', help='specify play time [second]')
    parser.add_option('--rtt', dest='rtt', type='int', help='specify rtt [Mbps]')
    parser.add_option('--loss', dest='loss', type='float', help='specify loss rate [%]')
    parser.add_option('--rate', dest='send_rate', type='int', help='specify send rate [Mbps]')
    parser.add_option('--ratio', dest='bandwidth_ratio', type='float', help='specify bandwidth_limit/send_rate')
    parser.add_option('--cwnd', dest='congestion_window', type='int', help='specify rush congestion window')

    (options, args) = parser.parse_args()
    play_mode_type = options.play_mode_type
    play_time = options.play_time
    rtt = options.rtt
    loss = options.loss
    rate = options.send_rate
    ratio = options.bandwidth_ratio
    congestion_window = options.congestion_window

    if rtt is None:
        rtt = 0
    if loss is None:
        loss = 0

    # set network
    print play_time, rtt, loss, rate * ratio
    stop_path(path_id=DELAY_PATH_ID, path_name=DELAY_PATH_NAME)
    delete_path(path_id=DELAY_PATH_ID, path_name=DELAY_PATH_NAME)
    create_path(path_id=DELAY_PATH_ID, path_name=DELAY_PATH_NAME)
    start_path(path_id=DELAY_PATH_ID, path_name=DELAY_PATH_NAME)
    setting_path_params(
        path_id=DELAY_PATH_ID, path_name=DELAY_PATH_NAME, path_director=PATH_DIRECTOR,
        pltr_delay_co_devalue=rtt / 2, pltr_loss_random_rate=loss,
        prtl_delay_co_devalue=rtt / 2, prtl_loss_random_rate=loss,
        pltr_bandwidth_rate=rate * ratio, prtl_bandwidth_rate=rate * ratio
    )
    setting_one_path_packet_classifier(CLIENT_HOST, SERVER_HOST, DELAY_PATH_ID)

    if play_mode_type == 'tcp':
        deploy_tcp_server()
        deploy_tcp_client()
        time.sleep(5)
        if rate is None:
            print "pls input send rate --rate!"
            exit(0)
        else:
            start_tcp_server(rate)
            start_tcp_client()
            print "###########################"
            print "###      start!         ###"
            print "###########################"
            time.sleep(play_time)
            stop_tcp_client()
            stop_tcp_server()
            collect_packet_jitter(play_mode_type)
            delay_parser(play_mode_type)
    elif play_mode_type == 'rush':
        deploy_supp_server()
        deploy_supp_client()
        time.sleep(5)
        if rate is None or congestion_window is None:
            print "pls input send rate or congestion window! --rate --congestion_window !!!"
            exit(0)
        else:
            start_supp_server(send_rate=rate, congestion_window=congestion_window)
            start_supp_client()
            print "###########################"
            print "###      start!         ###"
            print "###########################"
            time.sleep(play_time)
            stop_supp_client()
            stop_supp_server()
            collect_packet_jitter(play_mode_type)
            # tcp_delay_parser(play_mode_type)
            ##########################################
    else:
        print "play mode is not support!"
        exit(0)


if __name__ == '__main__':
    main()
