# coding=utf-8
# author: zengyuetian
# start and join lf

from lib.control.leifeng_controller import *


def print_help():
    print()
    print "please use following format"
    print "******************************************************"
    print "python leifeng.py [start | stop | join | leave ] [num]"
    print "******************************************************"
    print()
    exit(1)


####################################
# 如果一次start_join操作不成功
# 可以直接运行join
####################################
if __name__ == "__main__":
    time1 = time.time()
    action_list = ["start", "stop", "join", "leave"]
    # 判断输入
    if len(sys.argv) != 3:
        print_help()
    else:
        action = sys.argv[1]
        if action not in action_list:
            print_help()

        lf_num = int(sys.argv[2])

        # 开始执行启动雷锋的步骤
        if action == "start":
            # stop lf
            print("Stop Leifeng")
            stop_sdk(LF_IP)

            # deploy lf
            start_deploy_lf(LF_IP, lf_num)

            # start lf
            print("Start Leifeng")
            start_lf(LF_IP, lf_num)

        # 开始执行停止雷锋的步骤
        if action == "stop":
            # stop lf
            print("Stop ALL Leifeng !!!")
            stop_sdk(LF_IP)

        # 开始执行拉入雷锋的步骤
        if action == "join":
            # get peer_ids
            ids = get_lf_peer_ids(LF_IP, lf_num)

            while True:
                current = time.localtime()
                time_str = time.strftime("%Y/%m/%d %H:%M:%S", current)

                print "Timestamp {0}".format(time_str)
                # join leifeng
                for file_url, file_id in CHANNEL_INFO:
                    join_leifeng(STUN_THUNDER_IP, STUN_THUNDER_PORT, file_id, file_url, ids)
                    time.sleep(5)

                # sleep
                time.sleep(60)

        # 开始执行清退雷锋的步骤
        if action == "leave":
            # get peer_ids
            ids = get_lf_peer_ids(LF_IP, lf_num)

            while True:
                current = time.localtime()
                time_str = time.strftime("%Y/%m/%d %H:%M:%S", current)

                print "Timestamp {0}".format(time_str)
                # join leifeng
                for file_url, file_id in CHANNEL_INFO:
                    leave_leifeng(STUN_THUNDER_IP, STUN_THUNDER_PORT, file_id, ids)
                    time.sleep(5)

                # sleep
                time.sleep(60)

        # 计时
        time2 = time.time()
        print "Cost {0} seconds to {1}".format(time2 - time1, action)
