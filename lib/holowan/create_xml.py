# coding=utf-8
# 动态创建xml文件
import xml.dom.minidom
from lib.const import *
from lib.common.path import *


def create_xml():
    free_path_id = 1
    # 在内存中创建一个空的文档
    doc = xml.dom.minidom.Document()

    # 创建一个根节点clc对象
    root = doc.createElement('clc')

    # 将根节点添加到文档对象中
    doc.appendChild(root)

    engine_id = doc.createElement('engine_id')
    engine_id.appendChild(doc.createTextNode(str(1)))

    root.appendChild(engine_id)

    # ** ** ** ** ** ** ** ** ** ** ** **
    # 添加port 1 相关内容
    # ** ** ** ** ** ** ** ** ** ** ** **
    port1 = doc.createElement('port')
    port_id_1 = doc.createElement('port_id')
    port_id_1.appendChild(doc.createTextNode(str(1)))
    port1.appendChild(port_id_1)
    # 循环 添加 ipv4段, 从SDK->LivePush
    create_paths(doc, port1, free_path_id, LIVE_PUSH_IP, True)

    # 循环 添加 ipv4段, 从SDK->LF
    create_paths(doc, port1, free_path_id, LF_IP, True)

    # 添加 FreePath
    create_free_path(doc, port1, free_path_id)

    # 添加Port1到根
    root.appendChild(port1)

    # ** ** ** ** ** ** ** ** ** ** ** **
    # 添加port 2 相关内容
    # ** ** ** ** ** ** ** ** ** ** ** **
    port2 = doc.createElement('port')
    port_id_2 = doc.createElement('port_id')
    port_id_2.appendChild(doc.createTextNode(str(2)))
    port2.appendChild(port_id_2)
    # 循环 添加 ipv4段, 从LivePush->SDK
    create_paths(doc, port2, free_path_id, LIVE_PUSH_IP, False)

    # 循环 添加 ipv4段, 从LF->SDK
    create_paths(doc, port2, free_path_id, LF_IP, False)

    # 添加 FreePath
    create_free_path(doc, port2, free_path_id)

    # 添加Port1到根
    root.appendChild(port2)

    # 开始写xml文档
    path_packet_classifier_xml = get_root_path() + "/lib/holowan/setting_xml/path_packet_classifier.xml"
    fp = open(path_packet_classifier_xml, 'w')
    # doc.writexml(fp, indent='\t', addindent='  ', newl='\n', encoding="utf-8")
    doc.writexml(fp, addindent='  ', newl='\n', encoding="utf-8")


def create_paths(doc, port, fp_id, ip, is_port1):
    for index, peer_ip in enumerate(PEER_INFO):
        ipv4 = doc.createElement('ipv4')

        if is_port1:
            src_ip = peer_ip
            dst_ip = ip
        else:
            src_ip = ip
            dst_ip = peer_ip
        src = doc.createElement('src')
        src.appendChild(doc.createTextNode(src_ip))
        ipv4.appendChild(src)

        smask = doc.createElement('smask')
        smask.appendChild(doc.createTextNode(str(32)))
        ipv4.appendChild(smask)

        dst = doc.createElement('dst')
        dst.appendChild(doc.createTextNode(dst_ip))
        ipv4.appendChild(dst)

        dmask = doc.createElement('dmask')
        dmask.appendChild(doc.createTextNode(str(32)))
        ipv4.appendChild(dmask)

        tos = doc.createElement('tos')
        tos.setAttribute('any', "1")
        ipv4.appendChild(tos)

        path_id = doc.createElement('path_id')
        path_id.appendChild(doc.createTextNode(str(fp_id + index + 1)))
        ipv4.appendChild(path_id)

        port.appendChild(ipv4)


def create_free_path(doc, port, fp_id):
    ipv4 = doc.createElement('ipv4')

    src = doc.createElement('src')
    src.setAttribute('any', "1")
    ipv4.appendChild(src)

    smask = doc.createElement('smask')
    smask.appendChild(doc.createTextNode(str(32)))
    ipv4.appendChild(smask)

    dst = doc.createElement('dst')
    dst.setAttribute('any', "1")
    ipv4.appendChild(dst)

    dmask = doc.createElement('dmask')
    dmask.appendChild(doc.createTextNode(str(32)))
    ipv4.appendChild(dmask)

    tos = doc.createElement('tos')
    tos.setAttribute('any', "1")
    ipv4.appendChild(tos)

    path_id = doc.createElement('path_id')
    path_id.appendChild(doc.createTextNode(str(fp_id)))
    ipv4.appendChild(path_id)

    port.appendChild(ipv4)


def create_path_params_config(path_id, path_name, **damage_params):
    """
        根据规则字典创建指定path的具体规则
    :param path_id: 
    :param path_name: 
    :param damage_params: 
    :return: 
    """
    doc = xml.dom.minidom.Document()
    root = doc.createElement('pc')
    # 指定引擎编号为1
    eid = create_element_add_text_node(doc, 'eid', 1)
    # 指定虚拟链路ID编号
    pid = create_element_add_text_node(doc, 'pid', path_id)
    # 指定虚拟链路名
    pn = create_element_add_text_node(doc, 'pn', path_name)
    # 指定的虚拟链路 损伤方向为3,[1. 仅损伤下行 ，2. 仅损伤上行 ，3. 损伤上下行]
    pd = create_element_add_text_node(doc, 'pd', 3)
    # 指定虚拟链路的下行损伤参数
    pltr = create_path_params_direction_damage(doc, 'pltr', **damage_params)
    # 指定虚拟链路的上行损伤参数
    prtl = create_path_params_direction_damage(doc, 'prtl', **damage_params)

    root.appendChild(eid)
    root.appendChild(pid)
    root.appendChild(pn)
    root.appendChild(pd)
    root.appendChild(pltr)
    root.appendChild(prtl)
    doc.appendChild(root)
    path_params_config_xml = get_root_path() + "/lib/holowan/setting_xml/path_params_config_by_peer_info.xml"
    write_xml_by_document(doc, path_params_config_xml)


def create_path_params_direction_damage(doc, direction, **damage_params):
    p_direction = doc.createElement(direction)

    # 设置带宽限制, s为带宽限制类型 1正常模式 2抖动模式，r为带宽限制值，t带宽限制单位 3 Mbps
    bd = doc.createElement('bd')
    s = create_element_add_text_node(doc, 's', 1)
    r = create_element_add_text_node(doc, 'r', damage_params['bandwidth'])
    t = create_element_add_text_node(doc, 't', 3)
    bd.appendChild(s)
    bd.appendChild(r)
    bd.appendChild(t)

    # 设置背景流量, s背景流量开关 1 关闭 2开启，lu 背景流量带宽抢占比例，bs 背景流量报文大小
    bg = doc.createElement('bg')
    s = create_element_add_text_node(doc, 's', 1)
    lu = create_element_add_text_node(doc, 'lu', 0)
    bs = create_element_add_text_node(doc, 'bs', 0)
    bg.appendChild(s)
    bg.appendChild(lu)
    bg.appendChild(bs)

    # 队列深度配置，qd 队列深度值大小，qdt队列深度类型 1 报文个数 2 内存大小 3 时间ms
    ql = doc.createElement('ql')
    qd = create_element_add_text_node(doc, 'qd', damage_params['queue_limit'])
    qdt = create_element_add_text_node(doc, 'qdt', 2)
    ql.appendChild(qd)
    ql.appendChild(qdt)

    # 修改报文配置，cs 修改报文开关 0 关闭s
    md = doc.createElement('md')
    cs = create_element_add_text_node(doc, 'cs', 0)
    md.appendChild(cs)

    # MTU限制配置，s MTU限制开关，n MTU限制值
    m = doc.createElement('m')
    s = create_element_add_text_node(doc, 's', 1)
    n = create_element_add_text_node(doc, 'n', 1500)
    m.appendChild(s)
    m.appendChild(n)

    # 以太网帧间隙占用配置, t 帧间隙占用类型 1 默认以太网24 2 最小4 3自定义值， r 帧间隙大小值
    fo = doc.createElement('fo')
    t = create_element_add_text_node(doc, 't', 1)
    r = create_element_add_text_node(doc, 'r', 24)
    fo.appendChild(t)
    fo.appendChild(r)

    # 时延配置， s 时延类型 1 常量时延 2 平均分布时延 3 正态分布时延，
    d = doc.createElement('d')
    s = create_element_add_text_node(doc, 's', damage_params['delay']['type'])
    d.appendChild(s)
    if damage_params['delay']['type'] == 1:
        # de 时延值
        co = doc.createElement('co')
        de = create_element_add_text_node(doc, 'de', damage_params['delay']['value'])
        co.appendChild(de)
        d.appendChild(co)
    elif damage_params['delay']['type'] == 2:
        # dmi 平均分布的最小值，dma 平均分布的最大值，是否允许时延乱序 0关闭 1打开， shake平均时延抖动配置
        un = doc.createElement('un')
        dmi = create_element_add_text_node(doc, 'dmi', damage_params['delay']['min_value'])
        dma = create_element_add_text_node(doc, 'dma', damage_params['delay']['max_value'])
        reo = create_element_add_text_node(doc, 'reo', 0)
        shake = create_element_add_attribute(doc, 'shake', 'type_id', 0)
        un.appendChild(dmi)
        un.appendChild(dma)
        un.appendChild(reo)
        un.appendChild(shake)
        d.appendChild(un)
    else:
        pass

    # 丢包配置, s 丢包类型
    l = doc.createElement('l')
    s = create_element_add_text_node(doc, 's', 1)
    ra = doc.createElement('ra')
    r = create_element_add_text_node(doc, 'r', damage_params['loss'])
    ra.appendChild(r)
    l.appendChild(s)
    l.appendChild(ra)

    # BER配置， ber BER值， beri BER指数值
    cor = doc.createElement('cor')
    ber = create_element_add_text_node(doc, 'ber', 0)
    beri = create_element_add_text_node(doc, 'beri', 14)
    cor.appendChild(ber)
    cor.appendChild(beri)

    # 报文乱序配置, s 报文乱序类型 1默认类型 2抖动类型, p 报文乱序概率，dmi 报文乱序延时最小值，dma 报文乱序延时最大值
    reo = doc.createElement('reo')
    s = create_element_add_text_node(doc, 's', 1)
    p = create_element_add_text_node(doc, 'p', '0.000')
    dmi = create_element_add_text_node(doc, 'dmi', '0.1')
    dma = create_element_add_text_node(doc, 'dma', '0.5')
    reo.appendChild(s)
    reo.appendChild(p)
    reo.appendChild(dmi)
    reo.appendChild(dma)

    # 重复报文配置
    du = doc.createElement('du')
    s = create_element_add_text_node(doc, 's', 1)
    p = create_element_add_text_node(doc, 'p', '0.000')
    du.appendChild(s)
    du.appendChild(p)

    p_direction.appendChild(bd)
    p_direction.appendChild(bg)
    p_direction.appendChild(ql)
    p_direction.appendChild(md)
    p_direction.appendChild(m)
    p_direction.appendChild(fo)
    p_direction.appendChild(d)
    p_direction.appendChild(l)
    p_direction.appendChild(cor)
    p_direction.appendChild(reo)
    p_direction.appendChild(du)

    return p_direction


def create_element_add_text_node(doc, element_name, text):
    element = doc.createElement(element_name)
    element.appendChild(doc.createTextNode(str(text)))
    return element


def create_element_add_attribute(doc, element_name, attribute_name, attribute_value):
    element = doc.createElement(element_name)
    element.setAttribute(attribute_name, attribute_value)
    return element


def write_xml_by_document(doc, file_path):
    fp = open(file_path, 'w')
    doc.writexml(fp, addindent='  ', newl='\n', encoding="utf-8")
    fp.close()


if __name__ == "__main__":
    create_xml()
    # damage_params = {
    #     'bandwidth': 10,
    #     'queue_limit': 128,
    #     'delay': {'type': 1, 'value': 100},
    #     # 'delay': {'type': 2, 'max_value': 100, 'min_value': 50}
    #     'loss': 5
    # }
    # create_path_params_config('11', 'auto_test_path', **damage_params)

    # import requests
    # url = 'http://192.168.2.199:8080/emulator_config'
    # HEADERS = {
    #     "X-HoloWAN-API": "OI_API",
    #     "Accept": "*/*",
    #     "Content-type": "text/xml"
    # }
    # path_params_config_xml = get_root_path() + "/lib/holowan/setting_xml/test.xml"
    # with open(path_params_config_xml, 'r') as reader:
    #     config_string = reader.read()
    # print config_string
    # response = requests.post(url=url, headers=HEADERS, data=config_string)
    # print response.status_code
    # print response.text
