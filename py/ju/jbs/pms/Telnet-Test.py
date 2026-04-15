import socket
import time
from telnetlib import Telnet
from typing import Tuple
from py.ju.jbs.utils import db_sql

history_close_port = []

def check_port(host: str, port: int, timeout: int = 2) -> Tuple[int, bool]:
    """
    检查指定主机的端口是否开放

    参数:
    host (str): 目标主机名或 IP 地址
    port (int): 要检查的端口号
    timeout (int): 连接超时时间，单位为秒

    返回:
    Tuple[int, bool]: 包含端口号和是否开放的元组
    """
    try:
        with Telnet(host, port, timeout=timeout):
            return (port, True)
    except (socket.timeout, ConnectionRefusedError):
        return (port, False)
    except Exception as e:
        print(f"检查端口 {port} 时发生错误: {e}")
        return (port, False)


def range_port_test(max_port: int, min_port: int,ip:str):
    temp_port = max_port
    count = 0
    open_ports = []
    closed_ports = []
    while temp_port >= min_port:
        count = count -1
        result = check_port(ip, temp_port)
        # print("端口："+ str(result[0]) + "状态：" + str(result[1]))
        if result[1]:
            open_ports.append(temp_port)
            print(f"端口 {temp_port}: 开放")
        else:
            closed_ports.append(temp_port)
            print(f"端口 {temp_port}: 关闭")
        temp_port = temp_port - 1
    print("共计 %d 台" % count)
    print("无法连接端口：" + ','.join(repr(str(code)) for code in closed_ports))

def fixed_port_list(temp_ports, ip):
    open_ports = []
    closed_ports = []
    count = 0
    for port in temp_ports:
        count = count + 1
        result = check_port(ip, port)
        # print("端口："+ str(result[0]) + "状态：" + str(result[1]))
        if result[1]:
            open_ports.append(port)
            #print(f"端口 {port}: 开放")
        else:
            closed_ports.append(port)
            #print(f"端口 {port}: 关闭")
    print("共计 %d 台" % count)
    print("无法连接端口：" + ','.join(repr(str(code)) for code in closed_ports))


def fixed_port_segment(segment_list, ip):
    open_ports = []
    closed_ports = []
    count = 0
    for segment in segment_list:
        for port in range(segment[0], segment[1] + 1):
            count = count + 1
            result = check_port(ip, port)
            # print("端口："+ str(result[0]) + "状态：" + str(result[1]))
            if result[1]:
                open_ports.append(port)
                #print(f"端口 {port}: 开放")
            else:
                closed_ports.append(port)
                #print(f"端口 {port}: 关闭")



    print("检测时间：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print("共计 %d 台" % count)
    print("无法连接端口：" + ','.join(repr(str(code)) for code in closed_ports))
    print("新增连接失败端口：" + ','.join(repr(str(code)) for code in list(set(closed_ports) - set(history_close_port))))
    print("=============================================================================================")

    history_close_port.clear()
    history_close_port.extend(closed_ports)


def static_test():
    ip_1 = "124.115.116.142"
    ip_2 = "36.163.199.14"
    ip_3 = "61.185.16.90"
    ip_4 = "124.115.116.138"
    # 二厂段
    # segment_list = [(20001, 20015),
    #                 (20061, 20062),
    #                 (20047, 20050),
    #                 (20066, 20075),
    #                 (20038, 20040),
    #                 (20080, 20089),
    #                 (20021, 20022)]
    # segment_list = [(20001, 20094)]
    # 按端口段检测
    # fixed_port_segment(segment_list, ip_2)
    # temp_port = [20024, 20025, 20026, 20028, 20029, 20030]
    # # 按端口检测
    # fixed_port_list(temp_port, ip_1)
    # 三厂
    # segment_list = [(20034, 20081),(20088,20089),(20091,20093),(20096,20096),(20098,20099),(20101,20101),
    #                 (20001,20001),(20004,20004),(20008,20008),(20011,20012),(20015,20019),(20021,20023),(20025,20029),(20031,20032)]
    # 四厂
    # segment_list = [(20001, 20053)]
    # segment_list = [(20047, 20058)]
    #
    # fixed_port_segment(segment_list, ip_3)
    # schedule.every(1).minutes.do(fixed_port_segment, segment_list, ip_3)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    port_list = ""

def check_from_db(facotry_code):
    equipments = db_sql.get_auth_equipment(facotry_code, True)
    print(facotry_code + "设备数量" + str(len(equipments)))
    close_ports = []
    open_ports = []
    for equipment in equipments:
        result = check_port(equipment['ip'], equipment['port'])
        if result[1]:
            open_ports.append(equipment['port'])
        else:
            close_ports.append(equipment['port'])
    close_equipment_locations = list(map(lambda p: int(p) - 20000, close_ports))
    list(filter(lambda p: p >= 0, close_equipment_locations))
    print(close_equipment_locations)

if __name__ == '__main__':
    #check_from_db('GC0116')
    static_test()
