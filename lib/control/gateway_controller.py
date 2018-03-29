# coding=utf-8
# control gateway
# author: zengyuetian

from lib.control.net_controller import *


def gateway_package_delay_and_loss(remote_ip, eth, delay, loss_rate, band_width, live_push_ip):
    """
    setup gateway package delay interface
    :param remote_ip:
    :param eth:
    :param delay:
    :return:
    """
    package_delay(remote_ip, eth, delay, loss_rate, band_width, live_push_ip)

