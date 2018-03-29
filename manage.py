# coding=utf-8
# author: zengyuetian
# Tool to stop sdk on multi-machine

import sys
import threading
import time
import requests
import json
from lib.const import *
from lib.control.const import PEER_PATH_DICT
from lib.control.peer_controller import stop_sdk
from lib.control.player_controller import player_stop
from lib.control.sdk_controller import remove_logs, deploy_log_conf
from lib.holowan.setting_handle import delete_path, stop_path


def send_request(host_ip, host_port, url):
    url = "http://{0}:{1}{2}".format(host_ip, host_port, url)
    headers = dict()
    headers["accept"] = 'application/json'
    resp = requests.get(url, headers=headers, timeout=5)
    return resp


def get_sdk_data(host_ip, host_port):
    global mutex
    ip_list.append(host_ip)
    try:
        res = send_request(host_ip, host_port, "/ajax/report")
        p2p_percent = json.loads(res.content).get("p2p_percent", None)
        seed_num = json.loads(res.content).get("seed_num", None)
        stream_num = json.loads(res.content).get("stream_num", None)
        download_rate = json.loads(res.content).get("download_rate", None)

        if mutex.acquire(1):
            p2p_list.append(p2p_percent)
            seed_num_list.append(seed_num)
            stream_num_list.append(stream_num)
            download_rate_list.append(download_rate)
            mutex.release()
    except Exception as e:
        if mutex.acquire(1):
            p2p_list.append(0)
            seed_num_list.append(0)
            stream_num_list.append(0)
            download_rate_list.append(0)
            mutex.release()


class Tester(object):
    """
    test helper class
    """
    @staticmethod
    def print_help():
        print "Please use type: [stop_peer] or [stop_lf] or [p2p] or [clean_holowan] or [clean_log] or [change_conf]"
        exit(1)

    @staticmethod
    def stop_sdk(ips):
        for ip in ips:
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}".format(ip)
            t = threading.Thread(target=stop_sdk, args=(ip,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(0.1)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()
        print("All SDK stopped")

    @staticmethod
    def stop_play(ips):
        for ip in ips:
            print "---------------------------------------------------------------------------------------------------"
            print "Start for host {0}".format(ip)
            t = threading.Thread(target=player_stop, args=(ip,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(0.1)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()
        print("All player stopped")

    @staticmethod
    def collect_p2p():
        log_file = open("manage.log", 'w')
        while True:
            try:
                t1 = time.time()
                # print dash_board_port_list

                global p2p_list, seed_num_list, stream_num_list, download_rate_list, ip_list
                p2p_list = []
                bad_p2p_list = []
                seed_num_list = []
                stream_num_list = []
                bad_stream_list = []
                download_rate_list = []
                ip_list = []

                for ip in PEER_INFO:
                    t = threading.Thread(target=get_sdk_data, args=(ip, SDK_PORT))
                    t.start()

                main_thread = threading.currentThread()
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()

                t2 = time.time()
                zero_list = [x for x in p2p_list if x == 0]
                non_zero_list = [x for x in p2p_list if x != 0]
                current = time.localtime()
                time_str = time.strftime("%Y/%m/%d %H:%M:%S", current)
                bad_p2p_list.sort()
                bad_stream_list.sort()

                print "================================================================"
                print "{0} cost {1} seconds to get result".format(time_str, t2 - t1)
                print "IP number is: ", len(PEER_INFO), PEER_INFO.keys()
                print "SDK number is: {0}".format(len(p2p_list))
                print "------------------------------------------"
                print "          All sdk average p2p is: {0}%".format(sum(p2p_list) / len(p2p_list))
                print "          Alive sdk average p2p is: {0}%".format(sum(non_zero_list) / len(non_zero_list))
                print "          Max p2p is {0}%, Min p2p is {1}%".format(max(non_zero_list), min(non_zero_list))
                print "          {0} SDKs with p2p >= 80%".format(len([i for i in non_zero_list if i >= 80]))
                print "          {1}{0} SDKs with p2p 0%{1}".format(len(zero_list), " @@@@@@@@@@@@ " if len(zero_list) > 0 else "")
                print "          P2P 0 sdk info: ", bad_p2p_list
                print "------------------------------------------"
                print "          {0} SDKs with seed < 32".format(len([i for i in seed_num_list if i < 32]))
                print "------------------------------------------"
                print "          {0} SDKs with stream >= 32".format(len([i for i in stream_num_list if i >= 32]))
                print "          {0} SDKs with stream < 32".format(len([i for i in stream_num_list if i < 32]))
                print "------------------------------------------"
                # print "Download List", download_rate_list
                print "All sdk average download rate {0}".format(sum(download_rate_list) / len(download_rate_list))
                print "Alive sdk average download rate {0}".format(sum(download_rate_list) / len(non_zero_list))
                print "================================================================"
                print "Peer IP Address", ip_list
                print "SeedNum List", seed_num_list
                print "All sdk average seed number {0}".format(sum(seed_num_list) / len(seed_num_list))
                print "StreamNum List", stream_num_list
                print "All sdk average stream number {0}".format(sum(stream_num_list) / len(stream_num_list))

                # write log at once
                log_file.write(time_str + "\n")
                ip_text = "ip list:  " + str(ip_list) + "\n"
                log_file.write(ip_text)
                p2p_text = "p2p_text:  " + str(p2p_list) + "\n"
                log_file.write(p2p_text)
                seed_text = "seed_text:  " + str(seed_num_list) + "\n"
                log_file.write(seed_text)
                stream_text = "stream_text:  " + str(stream_num_list) + "\n"
                log_file.write(stream_text)
                log_file.flush()


            except Exception as e:
                # print e
                pass

            time.sleep(60)

    @staticmethod
    def clean_holowan():
        for path_name, path_id in PEER_PATH_DICT.items():
            stop_path(path_id=path_id, path_name=path_name)
            delete_path(path_id=path_id, path_name=path_name)
        stop_path(path_id=1, path_name='free_path')
        delete_path(path_id=1, path_name='free_path')

    @staticmethod
    def clean_log():
        for peer_ip in PEER_INFO:
            remove_logs(peer_ip)

    @staticmethod
    def change_log_conf():
        for peer_id in PEER_INFO:
            deploy_log_conf(peer_id)


if __name__ == "__main__":

    time1 = time.time()
    mutex = threading.Lock()
    p2p_list = []
    seed_num_list = []
    stream_num_list = []
    download_rate_list = []
    ip_list = []

    tester = Tester()
    if len(sys.argv) != 2:
        tester.print_help()
    else:
        if sys.argv[1] == "stop_peer":
            tester.stop_sdk(PEER_INFO.keys())
            tester.stop_play(PEER_INFO.keys())
        elif sys.argv[1] == "stop_lf":
            tester.stop_sdk(LF_IPS)
        elif sys.argv[1] == "p2p":
            tester.collect_p2p()
        elif sys.argv[1] == "clean_holowan":
            tester.clean_holowan()
        elif sys.argv[1] == "clean_log":
            tester.clean_log()
        elif sys.argv[1] == "change_conf":
            tester.change_log_conf()
        else:
            tester.print_help()

    time2 = time.time()
    print "********** Cost {0} seconds **********".format(time2 - time1)
