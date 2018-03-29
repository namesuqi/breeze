# coding=utf-8

from string import Template

from holowan_const import *


def setting_path_config(modify_switch, engine_id, path_id, path_name, if_enable=2):
    """
    虚拟链路（PATH）的修改（增添、删除、启用、禁用）
    :param modify_switch: 修改方式：[1.删除，2.添加，3.启用or禁用PATH]
    :param engine_id: 指定引擎ID编号
    :param path_id: 虚拟链路ID编号
    :param path_name: 虚拟链路名称
    :param if_enable: 是否启用该PATH：[1.禁用， 2.启用] modify_switch为3时生效
    :return:
    """
    with open(XML_DIR + PATH_CONFIG_NAME + ".xml", 'r') as reader:
        config_string = reader.read()
    conf_template = Template(config_string)
    params_dict = dict()
    params_dict["modify_switch"] = modify_switch
    params_dict["engine_id"] = engine_id
    params_dict["path_id"] = path_id
    params_dict["path_name"] = path_name
    params_dict["if_enable"] = if_enable

    return_conf = conf_template.substitute(params_dict)

    print return_conf
    return return_conf


def setting_path_params_config(engine_id, path_id, path_name, path_director=3,
                               pltr_bandwidth_rate=1000, pltr_delay_co_devalue=0, pltr_loss_random_rate=0,
                               prtl_bandwidth_rate=1000, prtl_delay_co_devalue=0, prtl_loss_random_rate=0,
                               pltr_background_switch=1, pltr_background_rate=0, pltr_background_burst=0,
                               prtl_background_switch=1, prtl_background_rate=0, prtl_background_burst=0):
    """

    :param engine_id: 指定引擎ID编号
    :param path_id: 虚拟链路ID编号
    :param path_name: 虚拟链路名称
    :param path_director: 指定的虚拟链路 损伤方向，[1.仅损伤下行 ，2.仅损伤上行 ，3.损伤上下行]
    :param pltr_bandwidth_rate: （下行链路损伤参数）正常模式带宽限制值
    :param pltr_delay_co_devalue: （下行链路损伤参数）常量时延的时延值
    :param pltr_loss_random_rate: （下行链路损伤参数）普通概率丢包概率值
    :param prtl_bandwidth_rate: （上行链路损伤参数）正常模式带宽限制值
    :param prtl_delay_co_devalue: （上行链路损伤参数）常量时延的时延值
    :param prtl_loss_random_rate: （上行链路损伤参数）普通概率丢包概率值
    :param pltr_background_switch: （下行链路损伤参数）背景流量开关，[1.关闭， 2.开启]
    :param pltr_background_rate: （下行链路损伤参数）背景流量带宽抢占比例
    :param pltr_background_burst: （下行链路损伤参数）背景流量报文大小
    :param prtl_background_switch: （上行链路损伤参数）背景流量开关，[1.关闭， 2.开启]
    :param prtl_background_rate: （上行链路损伤参数）背景流量带宽抢占比例
    :param prtl_background_burst: （上行链路损伤参数）背景流量报文大小
    :return:
    """

    with open(XML_DIR + PATH_PARAMS_CONFIG_NAME + ".xml", 'r') as reader:
        config_string = reader.read()
    conf_template = Template(config_string)
    params_dict = dict()
    params_dict["engine_id"] = engine_id
    params_dict["path_id"] = path_id
    params_dict["path_name"] = path_name
    params_dict["path_director"] = path_director

    params_dict["pltr_bandwidth_rate"] = pltr_bandwidth_rate
    params_dict["pltr_delay_co_devalue"] = pltr_delay_co_devalue
    params_dict["pltr_loss_random_rate"] = pltr_loss_random_rate
    params_dict["pltr_background_switch"] = pltr_background_switch
    params_dict["pltr_background_rate"] = pltr_background_rate
    params_dict["pltr_background_burst"] = pltr_background_burst

    params_dict["prtl_bandwidth_rate"] = prtl_bandwidth_rate
    params_dict["prtl_delay_co_devalue"] = prtl_delay_co_devalue
    params_dict["prtl_loss_random_rate"] = prtl_loss_random_rate
    params_dict["prtl_background_switch"] = prtl_background_switch
    params_dict["prtl_background_rate"] = prtl_background_rate
    params_dict["prtl_background_burst"] = prtl_background_burst

    return_conf = conf_template.substitute(params_dict)

    print return_conf
    return return_conf


def setting_packet_classifier_config(src_ip, dst_ip, path_id):
    """
    目前xml文件中写死一条规则，一定会增加192.168.8.44到src_ip适应path_id的规则
    :param src_ip: 过滤规则适用src_ip
    :param dst_ip: 过滤规则适用dst_ip
    :param path_id: 遵循其规则的path id
    :return:
    """
    with open(XML_DIR + PATH_PACKET_CLASSIFIER_NAME + ".xml", 'r') as reader:
        config_string = reader.read()
    # conf_template = Template(config_string)
    # params_dict = dict()
    # if src_ip is 'any':
    #     params_dict['any_src'] = '1'
    # else:
    #     params_dict['any_src'] = ''
    #
    # if dst_ip is 'any':
    #     params_dict['any_dst'] = '1'
    # else:
    #     params_dict['any_dst'] = ''
    #
    # params_dict["source_ip"] = src_ip
    # params_dict["destination_ip"] = dst_ip
    # params_dict["path_id"] = path_id
    #
    # config_string = conf_template.substitute(params_dict)
    return config_string


def setting_one_path_packet_classifier_config(src_ip, dst_ip, path_id):

    with open(XML_DIR + ONR_PATH_PACKET_CLASSIFIER_NAME + ".xml", 'r') as reader:
        config_string = reader.read()
    conf_template = Template(config_string)
    params_dict = dict()
    params_dict["source_ip"] = src_ip
    params_dict["destination_ip"] = dst_ip
    params_dict["path_id"] = path_id
    config_string = conf_template.substitute(params_dict)
    print config_string
    return config_string


def setting_jitter_config(engine_id, path_id, path_name, min_value, max_value, bw, loss, pltr_delay):
    with open(XML_DIR + "jitter_path_param_config.xml", 'r') as reader:
        config_string = reader.read()
    conf_template = Template(config_string)
    params_dict = dict()
    params_dict["engine_id"] = engine_id
    params_dict["path_id"] = path_id
    params_dict["path_name"] = path_name
    params_dict["min"] = min_value
    params_dict["max"] = max_value
    params_dict["band_width"] = bw
    params_dict["loss"] = loss
    params_dict["pltr_delay"] = pltr_delay

    return_conf = conf_template.substitute(params_dict)

    print return_conf
    return return_conf


if __name__ == '__main__':
    # # 新建PATH
    # setting_path_config(modify_switch=2, engine_id=1, path_id=3, path_name="test_path_name")
    # # 启用
    # setting_path_config(modify_switch=3, engine_id=1, path_id=3, path_name="test_path_name", if_enable=2)
    # # 配额新建PATH的参数
    # setting_path_params_config(engine_id=1, path_id=3, path_name='test_path_name', path_director=1,
    #                            pltr_delay_co_devalue=123, pltr_loss_random_rate=10, pltr_bandwidth_rate=2,
    #                            prtl_bandwidth_rate=2, prtl_loss_random_rate=5, prtl_delay_co_devalue=321)

    # print setting_packet_classifier_config(src_ip='192.168.8.41', dst_ip='192.168.8.45', path_id=11)

    setting_jitter_config(1, 11, 'test_create_path1', 100, 500, 222)

    pass
