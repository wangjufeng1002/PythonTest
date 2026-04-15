import sys
import threading
import time

from ju.jbs.common.db.pymysql_comm import UsingOnlineOMS as online
from ju.jbs.common.db.pymysql_comm import UsingTest as dev
import datetime
import json
from pymysql.converters import escape_string
from ju.jbs.common.db.db_connect_pool import DEV_POOL
from ju.jbs.common.db.db_connect_pool import ONLINE_POOL
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED


# DEV imc
def insert_iom(sqls):
    with DEV_POOL.connection() as conn:
        if isinstance(sqls, list):
            for sql in sqls:
                conn.cursor().execute(sql)
        conn.cursor().close()
        conn.commit()


def get_delivery(delivery_order_id, page_size):
    if delivery_order_id is None:
        sql = "SELECT * FROM erp_iom.`delivery_order` where create_time >='2023-12-01' order by delivery_order_id asc limit %d" % (
            page_size)
    else:
        sql = "SELECT * FROM erp_iom.`delivery_order` where delivery_order_id > '%s' and  create_time >='2023-12-01' order by delivery_order_id asc limit %d" % (
            delivery_order_id, page_size)
    # print(sql)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# imc 出库单详情
def get_delivery_details(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`sub_delivery_order` where delivery_order_id in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统单
def get_trade_order(order_id, page_size):
    if order_id is None:
        sql = "SELECT * FROM oms_ops.`trade_order` where create_time >='2023-12-01' and create_time <='2024-01-01 00:00:00' order by order_id asc limit %d" % (
            page_size)
    else:
        sql = "SELECT * FROM oms_ops.`trade_order` where order_id > '%s' and create_time >='2023-12-01' and create_time <='2024-01-01 00:00:00' order by order_id asc limit %d" % (
            order_id, page_size)
    # print(sql)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统单子单
def get_trade_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM oms_ops.`sub_trade_order` where order_id in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def copy_delivery_order_mutil_thread(page_size):
    executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="delivery_outbound")
    all_task = []
    page_num = 1
    #delivery_order_id = 'CK2312171736071413006270464'
    delivery_order_id = None
    for index in range(1, 50000):
        print("{},{} copy_delivery_order_loop page:{},deliver_order_id:{}".format(threading.current_thread().name,
                                                                                  datetime.datetime.now().strftime(
                                                                                      "%Y-%m-%d %H:%M:%S"), page_num,
                                                                                  delivery_order_id))
        delivery_order_ids = []
        delivery_orders = get_delivery(delivery_order_id, page_size)
        if len(delivery_orders) == 0:
            break
        delivery_order_insert_sql = []
        for delivery_order in delivery_orders:
            delivery_order_ids.append(delivery_order['delivery_order_id'])
            ls = [(k, v) for k, v in delivery_order.items() if (k != 'revoke_time' and v is not None)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into erp_iom.delivery_order (" + keys + ") values (" + values + ");"
            delivery_order_insert_sql.append(sql)

        task = executor.submit(get_delivery_detail_and_insert, delivery_order_insert_sql, delivery_order_ids)
        all_task.append(task)

        page_num += 1
        delivery_order_id = delivery_order_ids[-1]
        if len(all_task) > 100:
            print("delivery_order insert task num gt 100")
            while len(all_task) > 0:
                for task in all_task:
                    if task.done():
                        all_task.remove(task)
                print("delivery_order insert suspend 5 seconds task num : %d" % len(all_task))
                time.sleep(5)
    wait(all_task, return_when=ALL_COMPLETED)


def get_delivery_detail_and_insert(delivery_order_insert_sql, delivery_order_ids):
    details = get_delivery_details(delivery_order_ids)
    if len(details) == 0:
        return
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.sub_delivery_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    insert_iom(delivery_order_insert_sql)
    print("%s delivery_order insert sql size: %d last_order_id: %s" % (
        threading.current_thread().name, len(delivery_order_insert_sql), delivery_order_ids[-1]))


def copy_trade_order_mutil_thread(page_size):
    executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="trade_outbound")
    all_task = []
    page_num = 1
    order_id = None
    for index in range(1, 50000):
        print("{},{} copy_trade_order_loop page:{},order_id:{}".format(threading.current_thread().name,
                                                                       datetime.datetime.now().strftime(
                                                                           "%Y-%m-%d %H:%M:%S"),
                                                                       page_num, order_id))
        order_ids = []
        orders = get_trade_order(order_id, page_size)
        if len(orders) == 0:
            break
        order_insert_sql = []
        for order in orders:
            order_ids.append(order['order_id'])
            ls = [(k, v) for k, v in order.items() if (v is not None)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore  into oms_ops.`trade_order` (" + keys + ") values (" + values + ");"
            order_insert_sql.append(sql)

        ## 查询详情并保存
        task = executor.submit(get_trade_detail_and_insert, order_insert_sql, order_ids)
        all_task.append(task)

        page_num += 1
        order_id = order_ids[-1]

        if len(all_task) > 100:
            print("trade_order insert task num gt 100")
            while len(all_task) > 0:
                for task in all_task:
                    if task.done():
                        all_task.remove(task)
                print("trade_order suspend 5 seconds task num : %d" % len(all_task))
                time.sleep(5)
    wait(all_task, return_when=ALL_COMPLETED)


def get_trade_detail_and_insert(order_insert_sql, order_ids):
    details = get_trade_order_detail(order_ids)
    if len(details) == 0:
        return
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`sub_trade_order` (" + keys + ") values (" + values + ");"
        order_insert_sql.append(sql)
    insert_iom(order_insert_sql)
    print("%s trade_order insert sql size : %d  last_order_id %s" % (
        threading.current_thread().name, len(order_insert_sql), order_ids[-1]))


if __name__ == '__main__':
    multiprocessing.Process(target=copy_delivery_order_mutil_thread, args=(2000,), name='delivery_order').start()
    multiprocessing.Process(target=copy_trade_order_mutil_thread, args=(2000,), name='trade_order').start()
