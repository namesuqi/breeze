# coding=utf-8
# author: Tang HuaNan
# comment: Zeng YueTian
# fake player

import flv_parse
import pycurl
import threading
import sys
import time
import datetime


BUFFER_REDUCE_TIME = 100 * 1000     # 最大缓存时间
BUFFERINT_TIME = 1000               # 播放器缓存1秒


def strtime():
    return time.strftime("[%Y-%m-%d %H:%M:%S") + ".%03d] " % ((datetime.datetime.now().microsecond / 1000))


def get_cur_ms():
    return time.time() * 1000       # 返回毫秒数为单位的时间


class BufferInfo:

    def __init__(self, log_name):
        self.logfile = open(log_name, "w")
        pass

    def start(self):
        self.bufferTime = 0
        self.lastTimeStamp = 0                  # 最后一次记录的帧相关时间
        self.update_cnt = 0                     # 貌似没用
        self.buffering = time.time()            # 是否在卡顿，还没起播:默认为卡顿中，返回当前时间的时间戳（1970纪元后经过的浮点秒数）
        self.last_real_time = get_cur_ms()      # 最后一次记录的系统时间
        self.startup_time = time.time()         # 开始播放时的系统时间
        self.startup = False                    # 是不是已经起播了
        self.last_delay_report_time = get_cur_ms()  # 最后一次记录延迟时的系统时间
        self.tag_count = 0
        self.log("begin")
        self.timer = threading.Timer(0.047, self.onTimer)  # 第一次的时间和后面的定时器时间略有不同
        self.timer.start()

    def stop(self):
        self.timer.cancel()                     # 停止计时器

    def onTimer(self):
        self.update()
        self.timer = threading.Timer(0.05, self.onTimer)  # 启动下一个定时器
        self.timer.start()

    def log(self, text):
        """
        为日志打上时间戳，立即写

        """
        log = strtime() + text + "\n"
        self.logfile.write(log)
        self.logfile.flush()

    def addTag(self, pos, timestamp, size):
        self.tag_count += 1
        # if (self.tag_count == 1 or self.tag_count == 2) and is_drop_video_head_tag:
        if self.tag_count == 1 and is_drop_video_head_tag:
            # self.lastTimeStamp = timestamp
            pass
        else:
            self.bufferTime += (timestamp - self.lastTimeStamp)
            self.lastTimeStamp = timestamp
            if self.bufferTime > BUFFER_REDUCE_TIME:  # 如果超过最大能够缓存的时间，跳过一段时间
                self.bufferTime -= 500
                self.log("skip 500ms , buffer=%.2f" % (self.bufferTime))
            if self.buffering and self.bufferTime > BUFFERINT_TIME:  # 之前在卡顿，来数据了，够消费足够的时间
                if not self.startup:    # 如果还未起播，那么记为起播时间
                    self.startup = True
                    self.log("startup time %.2f" % (time.time() - self.startup_time))
                else:                   # 以后就都记为卡顿了
                    self.log("buffering %.2f" % (time.time() - self.buffering))
                self.buffering = 0      # 重置buffing，表示现在不卡顿，准备探测下次卡顿
                self.last_real_time = get_cur_ms()

    def update(self):
        if self.buffering:          # 正在卡顿的话
            return
        else:                       # 如果现在不卡顿
            spend = (get_cur_ms() - self.last_real_time)  # 现在到上次记录之间流逝的时间
            self.bufferTime -= spend                      # 更新还能播放的缓存时间

        # 如果当前时间大于上次延迟时间5秒以上，记录一次延迟（暂时不关注延迟）
        if self.last_delay_report_time + 5000 < get_cur_ms():
            self.log("delay %.2f" % (self.bufferTime / 1000.0))
            self.last_delay_report_time = get_cur_ms()

        self.last_real_time = get_cur_ms()      # 更新
        if self.bufferTime <= 0:                # 如果buffer时间不够用
            self.bufferTime = 0                 # 更新为0
            if self.buffering == 0:             # 如果之前不卡顿
                self.buffering = time.time()    # 记为卡顿


class ProcessData:

    def __init__(self, log_name):
        self.buffer_info = BufferInfo(log_name)

    def OpenClientReq(self):
        self.start()

    def CloseClientReq(self):
        self.stop()

    def start(self):
        self.parser = flv_parse.FLVParse()
        self.last_timestamp = 0      # 最后一帧时间戳
        self.frame_time_total = 0    # 所有帧的总时间
        self.frame_count = 0         # 总帧数
        self.buffer_info.start()     # 开始处理并记录日志
        self.video_tag_count = 0

    def stop(self):
        self.last_timestamp = 0
        self.buffer_info.stop()      # 停止处理

    def body_callback(self, buf):
        self.parser.parse(buf, self.tag_callback)

    def timestamp_verify(self, delta):
        if self.frame_count > 0:
            avg = self.frame_time_total / self.frame_count       # 平均每帧的时间
            diff = avg - delta
            if diff < 0:            # 计算偏差
                diff = -diff
            if diff > 10:           # 如果和平均每帧之间的时间大于10(ms?), 丢弃之
                self.buffer_info.log("Frame timestamp error avg=%d cur=%d" % (avg, delta))
        if delta > 0:             # 累加总时间和帧数
            self.frame_time_total += delta
            self.frame_count += 1

    def tag_callback(self, pos, timestamp, vtype, size):      # 每一个新tag处理一次
        if vtype == 9:      # 9 代表视频
            self.video_tag_count += 1
            # if (self.video_tag_count == 1 or self.video_tag_count == 2) and is_drop_video_head_tag:
            if self.video_tag_count == 1 and is_drop_video_head_tag:
                # update last timestamp and do nothing
                # self.last_timestamp = timestamp
                pass
            else:
                delta = timestamp - self.last_timestamp       # 帧之间的变动时间
                self.timestamp_verify(delta)     # 验证下timestamp，丢掉错误的，累加正确的
                self.last_timestamp = timestamp  # 更新
                self.buffer_info.addTag(pos, timestamp, size)  # 记录卡顿，延迟
        if vtype == 18:   # 18 代表脚本
            pass


def bytes_coming(buf):
    process_data.body_callback(buf)


def cur_thread(url):
    print strtime() + " curl thread...." + url
    cur = pycurl.Curl()
    cur.setopt(cur.URL, url)
    cur.setopt(cur.WRITEFUNCTION, bytes_coming)
    process_data.OpenClientReq()
    cur.perform()
    print cur.getinfo(cur.HTTP_CODE)
    cur.close()
    print strtime() + " curl exit " + url
    process_data.CloseClientReq()


# -----------------------------------
# How to call this script
# python main.py url log buffer_time
# -----------------------------------
if __name__ == '__main__':
    url = "http://127.0.0.1:32717/live_flv/user/wasu?url=http://flv.srs.cloutropy.com/wasu/time1.flv"
    log_file_name = None
    # if is_drop_video_head_tag = 1, pass the flv body first video tag, don't do anything
    is_drop_video_head_tag = 1
    if len(sys.argv) == 5:
        url = sys.argv[1]
        log_file_name = sys.argv[2]
        buffer_time = float(sys.argv[3])
        BUFFERINT_TIME = buffer_time * 1000
        is_drop_video_head_tag = int(sys.argv[4])
    elif len(sys.argv) == 4:
        url = sys.argv[1]
        log_file_name = sys.argv[2]
        buffer_time = float(sys.argv[3])
        BUFFERINT_TIME = buffer_time * 1000
    elif len(sys.argv) == 3:
        url = sys.argv[1]
        log_file_name = sys.argv[2]
    elif len(sys.argv) == 2:
        log_file_name = sys.argv[1]

    print("----------------------------------------")
    print("URL: ", url)
    print("LOG: ", log_file_name)
    print("BUFFERINT_TIME: ", BUFFERINT_TIME)
    print("----------------------------------------")

    global process_data
    process_data = ProcessData(log_file_name)

    if url:
        t = threading.Thread(target=cur_thread, args=(url,))
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
