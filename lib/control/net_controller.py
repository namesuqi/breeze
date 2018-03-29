# coding=utf-8
# control gateway network: tc ...
# author: zengyuetian

from lib.control.const import *
from lib.common.remoter import *


def package_delay(remote_ip, eth, delay, loss_rate, band_width, live_push_ip):
    """
    setup package delay via tc
    :param remote_ip:
    :param eth:
    :param delay:
    :param loss_rate:
    :param band_width:
    :param live_push_ip:
    :return:
    """
    cmd_list = [
        "tc qdisc del dev {0} root >/dev/null".format(eth),
        "tc qdisc add dev {0} root handle 1: cbq bandwidth 100Mbit avpkt 1000".format(eth),
        "tc class add dev {0} parent 1:0 classid 1:1 cbq bandwidth 100Mbit rate 100Mbit avpkt 1000 bounded".format(eth),
        "tc class add dev {0} parent 1:0 classid 1:2 cbq bandwidth 5Mbit rate 3Mbit avpkt 1000 bounded".format(eth),
        "tc class add dev {0} parent 1:0 classid 1:3 cbq bandwidth 5Mbit rate 3Mbit avpkt 1000 bounded".format(eth),

        "tc qdisc add dev {0} parent 1:2 handle 20: tbf rate {1}bit burst 100Kbit limit 30000".format(eth, band_width),
        "tc qdisc add dev {0} parent 20:1 netem delay {1}ms loss {2}%".format(eth, delay, loss_rate),

        "tc qdisc add dev {0} parent 1:3 handle 30: tbf rate {1}bit burst 100Kbit limit 30000".format(eth, band_width),
        "tc qdisc add dev {0} parent 30:1 netem delay {1}ms loss {2}%".format(eth, delay, loss_rate),

        "tc filter add dev {0} parent 1:0 protocol ip prio 16 u32 match ip dst {1} flowid 1:2".format(eth, PEER_IP),
        "tc filter add dev {0} parent 1:0 protocol ip prio 16 u32 match ip dst {1} flowid 1:3".format(eth, LF_IP),
        "tc filter add dev {0} parent 1:0 protocol ip prio 16 u32 match ip dst {1} flowid 1:3".format(eth, live_push_ip)
    ]
    for cmd in cmd_list:
        remote_execute(remote_ip, ROOT_USER, ROOT_PASSWD, cmd)


def speed_limit(remote_ip, src, dest, param):
    pass


def route_add_gateway(remote_ip, dest, mask, gw, eth):
    """
    add route(net) to specified machine
    :param remote_ip:
    :param dest:
    :param mask:
    :param gw:
    :param eth:
    :return:
    """
    cmd = "route add -net {0} netmask {1} gw {2} dev {3}".format(dest, mask, gw, eth)
    remote_execute(remote_ip, ROOT_USER, ROOT_PASSWD, cmd)


def route_delete_gateway(remote_ip, dest, mask, gw, eth):
    """
    delete route(net) in specified machine
    :param remote_ip:
    :param dest:
    :param mask:
    :param gw:
    :param eth:
    :return:
    """
    cmd = "route del -net {0} netmask {1} gw {2} dev {3}".format(dest, mask, gw, eth)
    remote_execute(remote_ip, ROOT_USER, ROOT_PASSWD, cmd)


def delete_remote_iptables(remote_ip):
    """
    clear remote machine's iptables
    :param remote_ip:
    :return:
    """
    cmd = "iptables -F"
    remote_execute(remote_ip, ROOT_USER, ROOT_PASSWD, cmd)


def icmp_redirect(remote_ip):
    cmd = "iptables -A INPUT -p icmp --icmp-type redirect -j DROP && " \
          "iptables -A FORWARD -p icmp --icmp-type redirect -j DROP && " \
            "iptables -A OUTPUT -p icmp --icmp-type redirect -j DROP"
    remote_execute(remote_ip, ROOT_USER, ROOT_PASSWD, cmd)

if __name__ == "__main__":
    icmp_redirect("")
