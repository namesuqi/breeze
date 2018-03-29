# coding=utf-8
"""
stun related api test keyword

__author__ = 'zengyuetian'

"""
import json
import threading
import requests
from lib.decorator.trace import *
from lib.control.const import *

join_failed_peer_ids = list()


@print_trace
def join_leifeng(host, port, file_id, file_url, peer_ids):

    url = "http://" + host + ":" + port + "/rrpc/join_leifeng"

    headers = dict()
    headers['content-type'] = 'application/json'
    headers['accept'] = 'application/json'

    if type(peer_ids) != list:
        peer_ids = [peer_ids]

    body_data = {
        "file_id": file_id,
        "file_url": file_url,
        "peer_ids": peer_ids
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(body_data))

    print "##############  join LF  #################"
    print "status_code: {0}".format(response.status_code)
    print "url: {0}".format(url)
    print "data: {0}".format(body_data)
    print "text: {0}".format(response.text)
    print "########################################"
    return response


@print_trace
def leave_leifeng(host, port, file_id, peer_ids):

    url = "http://" + host + ":" + port + "/leave_lf"

    headers = dict()
    headers['content-type'] = 'application/json'
    headers['accept'] = 'application/json'

    if type(peer_ids) != list:
        peer_ids = [peer_ids]

    body_data = {
        "file_id": file_id,
        "peer_ids": peer_ids
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(body_data))

    print "##############  leave LF  #################"
    print "status_code: {0}".format(response.status_code)
    print "url: {0}".format(url)
    print "data: {0}".format(body_data)
    print "text: {0}".format(response.text)
    print "########################################"
    return response

##############################################################
# 暂时不要删除，备用
# @print_trace
# def join_leifeng_one_by_one(host, port, file_id, file_url, peer_ids):
#     """
#     join leifeng one by one to improve succeed rate
#     """
#
#     for peer_id in peer_ids:
#         t = threading.Thread(target=join_leifeng_new, args=(host, port, file_id, file_url, peer_id))
#         t.start()
#     main_thread = threading.currentThread()
#     for t in threading.enumerate():
#         if t is not main_thread:
#             t.join()
#     return True if len(join_failed_peer_ids) == 0 else False
#
#
# @print_trace
# def join_leifeng_new(host, port, file_id, file_url, peer_id):
#
#     url = "http://" + host + ":" + port + "/rrpc/join_leifeng"
#
#     headers = dict()
#     headers['content_type'] = 'application/json'
#     headers['accept'] = 'application/json'
#
#     if type(peer_id) != list:
#         peer_ids = [peer_id]
#     else:
#         peer_ids = peer_id
#
#     body_data = {
#         "file_id": file_id,
#         "file_url": file_url,
#         "peer_ids": peer_ids
#     }
#
#     response = requests.post(url=url, headers=headers, data=json.dumps(body_data))
#     print response.status_code, response.content
#     if json.loads(response.text).get("error", None) is not None:
#         join_failed_peer_ids.append(peer_id)
#         print("Join leifeng {0} fail".format(peer_id))
#     else:
#         print("Join leifeng succeed")
# 暂时不要删除，备用
##############################################################


if __name__ == "__main__":
    # join_leifeng_new(STUN_THUNDER_IP, STUN_THUNDER_PORT, FILE_ID, FILE_URL, "00000009A5C84C09AAEE8F7426E71A85")
    pass