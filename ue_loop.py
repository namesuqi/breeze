# coding=utf-8
# author: sunxiaolei
"""
run ue test with loops
"""

import optparse
import os
import time
from lib.const import *


def start_custom_play(play_time, lf_num=0):
    for mode in RUN_MODE_LIST:
        cmd = "python custom_play.py -p %s -t %d --lf %d" % (mode, play_time, lf_num)
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    parser = optparse.OptionParser("Usage: python %prog -l <loop times> -t <play duration>")
    parser.add_option('-l', dest='loop_num', type='int', help='specify ue test loop times')
    parser.add_option('-t', dest='play_duration', type='int', help='specify play time [second]')
    parser.add_option('--lf', dest='lf_num', type='int', help='specify join LF number')

    (options, args) = parser.parse_args()
    loop_num = options.loop_num
    play_duration = options.play_duration
    lf_number = options.lf_num

    start_time = time.time()
    for k in range(loop_num):
        print "++++++++++++++++++++++++++++++++++++"
        print "++++++         %d         +++++" % k
        print "++++++++++++++++++++++++++++++++++++"
        if lf_number is None:
            start_custom_play(play_duration)
        else:
            start_custom_play(play_duration, lf_number)

    print 'use time : %s' % (time.time() - start_time)
