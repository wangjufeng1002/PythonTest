#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
import setting
from sshtunnel import SSHTunnelForwarder
import sys
#from dbConnectPool import  POOL

order_basic = None
order_package = None


def initDb(active):
    global server, order_basic, order_package
    if "test" in active:
        server = SSHTunnelForwarder(
            ("10.4.12.122", 22),  # ssh IP和port
            ssh_password="checkos",  # ssh 密码
            ssh_username="checkos",
            remote_bind_addresses=(("myordersbasicdb.idc4", 3306), ("mymt_order_package.db", 3306)))  # 数据库所在的IP和端口
        server.start()
        # order_baisc连接
        order_basic = pymysql.connect(host="127.0.0.1", port=server.local_bind_ports[0], user=setting.ob_use,
                                      password=setting.ob_password, database="orders_basic",
                                      charset="utf8")
        # order-package 连接
        order_package = pymysql.connect(host="127.0.0.1", port=server.local_bind_ports[1], user=setting.op_use,
                                        password=setting.op_password, database="mt_order_package",
                                        charset="utf8")
    elif "prod" in active:
        # order_baisc连接
        order_basic = pymysql.connect(host=setting.ob_host, port=setting.ob_port, user=setting.ob_use,
                                      password=setting.ob_password, database="orders_basic",
                                      charset="utf8", autocommit=True)
        # order-package 连接
        order_package = pymysql.connect(host=setting.op_host, port=setting.op_port, user=setting.op_use,
                                        password=setting.op_password, database="mt_order_package",
                                        charset="utf8", autocommit=True)
    elif "history" in active:
        # order_baisc连接
        order_basic = pymysql.connect(host=setting.ob_host, port=setting.ob_port, user=setting.ob_use,
                                      password=setting.ob_password, database="orders_basic",
                                      charset="utf8", autocommit=True)
        # order-package 连接
        order_package = pymysql.connect(host=setting.op_host, port=setting.op_port, user=setting.op_use,
                                        password=setting.op_password, database="mt_order_package",
                                        charset="utf8", autocommit=True)

    else:
        # order_baisc连接
        order_basic = pymysql.connect(host=setting.op_host_his, port=setting.op_port_his, user=setting.op_use_his,
                                      password=setting.op_password_his, database="orders_basic_history",
                                      charset="utf8")
        # order-package 连接
        order_package = pymysql.connect(host=setting.op_host_dev, port=setting.op_port_dev, user=setting.op_use_dev,
                                        password=setting.op_password_dev, database="mt_order_package",
                                        charset="utf8")

def getOrderCustDetailByCustId(custId):
    sql = "select order_id, as custId,nick_name as custNickName from order_invoice where shop_id =  "
    executeSql = sql % custId
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    result = cursor.fetchall()
    custs = []
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        cust = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            cust[columns[j]] = row[j]
        custs.append(cust)
    cursor.close()
    return custs

def getNullShopIdInvoice(offset,limit):
    return None