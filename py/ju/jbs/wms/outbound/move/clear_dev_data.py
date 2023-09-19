from pymysql_online import UsingMysql as online
from pymysql_dev import UsingMysql as dev
import datetime
import json
from pymysql.converters import escape_string
from db_connect_pool import DEV_POOL
from db_connect_pool import ONLINE_POOL
import multiprocessing


# 退货应收
def get_return_order( page_size):
    sql = "SELECT return_order_id FROM erp_iom.`return_order` where arrive_time >='2023-08-01' and order_status in (50,60,40,70) limit  %d" % (page_size)
    with dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统退单
def get_refund_order(page_size):
    sql = "SELECT refund_id FROM oms_ops.`refund_order` where create_time >='2023-08-01'  limit %d" % page_size
    with dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 采退，采入
def get_purchase_in_refund(page_size):
    sql = "SELECT stock_order_code FROM erp_iom.`stock_order` where billing_time >='2023-08-01' and order_type in (5,6)  and status in (3,13,14) limit %d" % page_size
    with dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库
def get_no_order( page_size):
    sql = "SELECT inbound_order_code FROM erp_iom.`no_order_inbound_order` where arrive_time >='2023-08-01'  limit %d" % ( page_size)
    with dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# DEV imc
def detele_iom(sqls):
    with DEV_POOL.connection() as conn:
        if isinstance(sqls, list):
            for sql in sqls:
                conn.cursor().execute(sql)
        conn.cursor().close()
        conn.commit()


def delete_return_order(page_size):
    sqls = []
    refund_order_ids = []
    return_orders = get_return_order(page_size)
    if len(return_orders) == 0:
        return False
    for order in return_orders:
        refund_order_ids.append(order['return_order_id'])
    orderIds = ','.join(repr(str(orderId)) for orderId in refund_order_ids)
    sql = "delete from  erp_iom.`return_order` where return_order_id in (%s)" % orderIds
    sql2 = "delete from  erp_iom.`return_order_detail` where return_order_id in (%s)" % orderIds
    sqls.append(sql)
    sqls.append(sql2)
    detele_iom(sqls)
    return True


def delete_refund_order(page_size):
    sqls = []
    refund_order_ids = []
    return_orders = get_refund_order(page_size)
    if len(return_orders) == 0:
        return False
    for order in return_orders:
        refund_order_ids.append(order['refund_id'])
    orderIds = ','.join(repr(str(orderId)) for orderId in refund_order_ids)
    sql = "delete  from oms_ops.`refund_order` where refund_id in (%s)" % orderIds
    sql2 = "delete from  oms_ops.`sub_refund_order` where refund_id in (%s)" % orderIds
    sqls.append(sql)
    sqls.append(sql2)
    detele_iom(sqls)
    return True

def delete_purchase_in_refund(page_size):
    sqls = []
    refund_order_ids = []
    return_orders = get_purchase_in_refund(page_size)
    if len(return_orders) == 0:
        return False
    for order in return_orders:
        refund_order_ids.append(order['stock_order_code'])
    orderIds = ','.join(repr(str(orderId)) for orderId in refund_order_ids)
    sql = "delete from erp_iom.`stock_order` where stock_order_code in (%s)" % orderIds
    sql2 = "delete from erp_iom.`stock_order_detail` where stock_order_code in (%s)" % orderIds
    sqls.append(sql)
    sqls.append(sql2)
    detele_iom(sqls)
    return True


def delete_no_order(page_size):
    sqls = []
    refund_order_ids = []
    return_orders = get_no_order(page_size)
    if len(return_orders) == 0:
        return False
    for order in return_orders:
        refund_order_ids.append(order['inbound_order_code'])
    orderIds = ','.join(repr(str(orderId)) for orderId in refund_order_ids)
    sql = "delete from erp_iom.`no_order_inbound_order` where inbound_order_code in (%s)" % orderIds
    sql2 = "delete from erp_iom.`sub_no_order_inbound_order` where inbound_order_code in (%s)" % orderIds
    sqls.append(sql)
    sqls.append(sql2)
    detele_iom(sqls)
    return True


def delete_return_order_loop(page_size):
    for index in range(1, 100000):
        if delete_return_order(page_size) is False:
            break


def delete_purchase_order_loop(page_size):
    for index in range(1, 100000):
        if delete_purchase_in_refund(page_size) is False:
            break


def delete_refund_order_loop(page_size):
    for index in range(1, 100000):
        if delete_refund_order( page_size) is False:
            break


def delete_no_order_loop(page_size):
    for index in range(1, 100000):
        if delete_no_order(page_size) is False:
            break



if __name__ == '__main__':
    delete_return_order_loop(1000)
    multiprocessing.Process(target=delete_return_order_loop, args=(1000,), name='return_order').start()
    multiprocessing.Process(target=delete_purchase_order_loop, args=(1000,), name='purchase_order').start()
    multiprocessing.Process(target=delete_refund_order_loop, args=(1000,), name='refund_order').start()
    multiprocessing.Process(target=delete_no_order_loop, args=(1000,), name='no_order').start()
