import socket
import argparse
from ctypes.wintypes import tagMSG
from telnetlib import Telnet
from typing import List, Tuple


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

if __name__ == '__main__':
    max_port = 20094
    min_port = 20070
    ip_1 = "124.115.116.142"
    ip_2 = "36.163.199.14"
    ip_3 = "61.185.16.90"

    ip = ip_3

    temp_port = max_port
    open_ports = []
    closed_ports = []
    while temp_port >= min_port:
        result = check_port(ip, temp_port)
        # print("端口："+ str(result[0]) + "状态：" + str(result[1]))
        if result[1]:
            open_ports.append(temp_port)
            print(f"端口 {temp_port}: 开放")
        else:
            closed_ports.append(temp_port)
            print(f"端口 {temp_port}: 关闭")
        temp_port = temp_port -1

    print("无法连接端口：")
    for r in closed_ports:
        print(str(r))
