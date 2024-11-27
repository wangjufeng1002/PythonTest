import sys
import threading
import time

from pymysql_online import UsingMysql as online
from pymysql_dev import UsingMysql as dev
import datetime
import json
from pymysql.converters import escape_string
from db_connect_pool import DEV_POOL
from db_connect_pool import ONLINE_POOL
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

replace_warehouse_code = ['WH0016',
                          'WH0019',
                          'WH0045',
                          'WH0046',
                          'WH0048',
                          'WH0058',
                          'WH0068',
                          'WH0074',
                          'WH0076',
                          'WH0079',
                          'WH0085',
                          'WH0087',
                          'WH0145',
                          'WH0165',
                          'WH0168',
                          'WH0194',
                          'WH0203',
                          'WH0205',
                          'WH0209',
                          'WH0211',
                          'WH0216',
                          'WH0237',
                          'WH0239',
                          'WH0254',
                          'WH0261',
                          'WH0262',
                          'WH0267',
                          'WH0288',
                          'WH0349',
                          'WH0360',
                          'WH0381',
                          'WH0382',
                          'WH0388',
                          'WH0390', ]

warehouse_code_sql = ','.join(repr(str(code)) for code in replace_warehouse_code)


# Imc 出库单
# def get_delivery(delivery_order_id, page_size):
#     if delivery_order_id is None:
#         sql = "SELECT * FROM erp_iom.`delivery_order` where warehouse_delivery_time >='2023-09-01' and warehouse_code in (%s)   order by delivery_order_id asc limit %d" % (warehouse_code_sql, page_size)
#     else:
#         sql = "SELECT * FROM erp_iom.`delivery_order` where delivery_order_id > '%s' and  warehouse_delivery_time >='2023-09-01' and warehouse_code in (%s)   order by delivery_order_id asc limit %d" % (
#             delivery_order_id, warehouse_code_sql, page_size)
#     print(sql)
#     with online() as um:
#         um.cursor.execute(sql)
#         return um.cursor.fetchall()

def get_delivery(delivery_order_id, page_size):
    if delivery_order_id is None:
        sql = "SELECT * FROM erp_iom.`delivery_order` where trade_time >='2023-12-01' order by delivery_order_id asc limit %d" % (
            page_size)
    else:
        sql = "SELECT * FROM erp_iom.`delivery_order` where delivery_order_id > '%s' and  trade_time >='2023-12-01' order by delivery_order_id asc limit %d" % (
            delivery_order_id, page_size)
    #print(sql)
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


# DEV imc
def insert_iom(sqls):
    with DEV_POOL.connection() as conn:
        if isinstance(sqls, list):
            for sql in sqls:
                conn.cursor().execute(sql)
        conn.cursor().close()
        conn.commit()


# 退货应收
def get_return_order(id, page_size):
    if id is None:
        sql = "SELECT * FROM erp_iom.`return_order` where create_time >='2023-12-01' order by id asc limit %d" % (
            page_size)
    else:
        sql = "SELECT * FROM erp_iom.`return_order` where id > '%s' and  create_time >='2023-12-01'  order by id asc limit %d" % (
            id, page_size)
    print(sql)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 退货应收详情
def get_return_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`return_order_detail` where return_order_id in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统退单
def get_refund_order(refund_id, page_size):
    if refund_id is None:
        sql = "SELECT * FROM oms_ops.`refund_order` where create_time >='2023-09-01' order by refund_id asc limit %d" % (
            page_size)
    else:
        sql = "SELECT * FROM oms_ops.`refund_order` where refund_id > '%s' and create_time >='2023-09-01' order by refund_id asc limit %d" % (
            refund_id, page_size)
    print(sql)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统单
def get_trade_order(order_id, page_size):
    if order_id is None:
        sql = "SELECT * FROM oms_ops.`trade_order` where trade_time >='2023-12-01' and trade_time <='2024-01-01 00:00:00' order by order_id asc limit %d" % (
            page_size)
    else:
        sql = "SELECT * FROM oms_ops.`trade_order` where order_id > '%s' and trade_time >='2023-12-01' and trade_time <='2024-01-01 00:00:00' order by order_id asc limit %d" % (
            order_id, page_size)
    #print(sql)
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


def get_purchare_refund_order(page_from, page_size):
    sql = "SELECT * FROM srm_ops.`refund_order` where delivery_time >='2023-08-01'  limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统退单子单
def get_refund_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM oms_ops.`sub_refund_order` where refund_id in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 采退，采入
def get_purchase_in_refund(page_from, page_size):
    sql = "SELECT * FROM erp_iom.`stock_order` where billing_time >='2023-08-01' and order_type in (5,6)  and status in (3,13,14) limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 采退，采入
def get_purchase_in_refund_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`stock_order_detail` where stock_order_code in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库
def get_no_order(page_from, page_size):
    sql = "SELECT * FROM erp_iom.`no_order_inbound_order` where create_time >='2023-12-01'  limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库子单
def get_no_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`sub_no_order_inbound_order` where inbound_order_code in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库
def get_purchase_price(page_from, page_size):
    sql = "SELECT * FROM srm_billing.`purchase_price`  limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 复制imc 出库单到 开发环境
def copy_delivery_order(delivery_order_id, page_size):
    delivery_order_ids = []
    delivery_orders = get_delivery(delivery_order_id, page_size)
    if len(delivery_orders) == 0:
        return False, 0
    delivery_order_insert_sql = []
    for delivery_order in delivery_orders:
        delivery_order_ids.append(delivery_order['delivery_order_id'])
        ls = [(k, v) for k, v in delivery_order.items() if (k != 'revoke_time' and v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.delivery_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    ## 查询详情
    details = get_delivery_details(delivery_order_ids)
    if len(details) == 0:
        return False, 0
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.sub_delivery_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)

    insert_iom(delivery_order_insert_sql)
    return True, delivery_order_ids[-1]


def copy_return_order(id, page_size):
    return_order_ids = []
    return_orders = get_return_order(id, page_size)
    if len(return_orders) == 0:
        return False, 0
    delivery_order_insert_sql = []
    for return_order in return_orders:
        return_order_ids.append(return_order['return_order_id'])
        ls = [(k, v) for k, v in return_order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.return_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    ## 查询详情
    details = get_return_order_detail(return_order_ids)
    if len(details) == 0:
        return False, 0
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.return_order_detail (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    insert_iom(delivery_order_insert_sql)
    return True, return_orders[-1]['id']


def copy_refund_order(refund_id, page_size):
    refund_order_ids = []
    return_orders = get_refund_order(refund_id, page_size)
    if len(return_orders) == 0:
        return False
    refund_order_insert_sql = []
    for return_order in return_orders:
        refund_order_ids.append(return_order['refund_id'])
        ls = [(k, v) for k, v in return_order.items() if (k != 'revoke_time' and v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`refund_order` (" + keys + ") values (" + values + ");"
        refund_order_insert_sql.append(sql)
    ## 查询详情
    details = get_refund_order_detail(refund_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`sub_refund_order` (" + keys + ") values (" + values + ");"
        refund_order_insert_sql.append(sql)
    insert_iom(refund_order_insert_sql)
    return True, refund_order_ids[-1]


def copy_purchase_order(page_from, page_size):
    purchase_order_ids = []
    purchase_orders = get_purchase_in_refund(page_from, page_size)
    if len(purchase_orders) == 0:
        return False
    purchase_order_insert_sql = []
    for purchase_order in purchase_orders:
        purchase_order_ids.append(purchase_order['stock_order_code'])
        ls = [(k, v) for k, v in purchase_order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into erp_iom.`stock_order` (" + keys + ") values (" + values + ");"
        purchase_order_insert_sql.append(sql)
    ## 查询详情
    details = get_purchase_in_refund_detail(purchase_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.`stock_order_detail` (" + keys + ") values (" + values + ");"
        purchase_order_insert_sql.append(sql)
    insert_iom(purchase_order_insert_sql)
    return True


def copy_no_order(page_from, page_size):
    no_order_ids = []
    no_orders = get_no_order(page_from, page_size)
    if len(no_orders) == 0:
        return False
    no_order_insert_sql = []
    for no_order in no_orders:
        no_order_ids.append(no_order['inbound_order_code'])
        ls = [(k, v) for k, v in no_order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.`no_order_inbound_order` (" + keys + ") values (" + values + ");"
        no_order_insert_sql.append(sql)
    ## 查询详情
    details = get_no_order_detail(no_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.`sub_no_order_inbound_order` (" + keys + ") values (" + values + ");"
        no_order_insert_sql.append(sql)
    insert_iom(no_order_insert_sql)
    return True


def copy_purchase_price(page_from, page_size):
    purchase_prices = get_purchase_price(page_from, page_size)
    purchase_prices_insert_sql = []
    if len(purchase_prices) == 0:
        return False
    for purchase_price in purchase_prices:
        ls = [(k, v) for k, v in purchase_price.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into srm_billing.`purchase_price` (" + keys + ") values (" + values + ");"
        purchase_prices_insert_sql.append(sql)
    insert_iom(purchase_prices_insert_sql)
    return True


def copy_purchare_refund_order(page_from, page_size):
    refund_orders = get_purchare_refund_order(page_from, page_size)
    refund_orders_insert_sql = []
    if len(refund_orders) == 0:
        return False
    for refund_order in refund_orders:
        ls = [(k, v) for k, v in refund_order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into srm_ops.`refund_order` (" + keys + ") values (" + values + ");"
        refund_orders_insert_sql.append(sql)
    insert_iom(refund_orders_insert_sql)
    return True


def copy_trade_order(order_id, page_size):
    order_ids = []
    orders = get_trade_order(order_id, page_size)
    if len(orders) == 0:
        return False
    order_insert_sql = []
    for order in orders:
        order_ids.append(order['order_id'])
        ls = [(k, v) for k, v in order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`trade_order` (" + keys + ") values (" + values + ");"
        order_insert_sql.append(sql)
    ## 查询详情
    details = get_trade_order_detail(order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`sub_trade_order` (" + keys + ") values (" + values + ");"
        order_insert_sql.append(sql)
    insert_iom(order_insert_sql)
    return True, order_ids[-1]


def copy_trade_order_mutil_thread(page_size):
    executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="trade_outbound")
    all_task = []
    page_num = 1
    order_id = "JY2312091733516770471919616"
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
        ## 查询详情
        details = get_trade_order_detail(order_ids)
        if len(details) == 0:
            continue
        for detail in details:
            ls = [(k, v) for k, v in detail.items() if (v is not None)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore  into oms_ops.`sub_trade_order` (" + keys + ") values (" + values + ");"
            order_insert_sql.append(sql)

        # print(
        #     "%s,%s trade order pageNum= %d ,last_orderId %s" % (threading.current_thread().name,
        #                                                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #                                                         page_num, order_ids[-1]))

        task = executor.submit(insert_iom, order_insert_sql)
        all_task.append(task)

        page_num += 1
        order_id = order_ids[-1]

        if len(all_task) > 100:
            print("trade order insert task num gt 100")
            while len(all_task) > 0:
                for task in all_task:
                    if task.done():
                        all_task.remove(task)
                print("trade order suspend 5 seconds task num : %d" % len(all_task))
                time.sleep(5)
        wait(all_task, return_when=ALL_COMPLETED)


def copy_trade_order_loop(page_size):
    page_num = 1
    order_id = "JY2312091733516770471919616"
    for index in range(1, 100000):
        print("copy_trade_order_loop page:{},order_id:{}".format(page_num, order_id))
        order = copy_trade_order(order_id, page_size)
        if order[0] is False:
            break
        order_id = order[-1]
        page_num += 1


def copy_purchare_refund_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_refund_loop page:{}".format(page_num))
        if copy_purchare_refund_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_delivery_order_loop(page_size):
    page_num = 1
    deliver_order_id = 'CK2312101733789571865890816'
    for index in range(1, 100000):
        print("copy_delivery_order_loop page:{},deliver_order_id:{}".format(page_num, deliver_order_id))
        order = copy_delivery_order(deliver_order_id, page_size)
        if order[0] is False:
            break
        deliver_order_id = order[-1]
        page_num += 1


def copy_delivery_order_mutil_thread(page_size):
    executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="delivery_outbound")
    all_task = []
    page_num = 1
    delivery_order_id = 'CK2312101733789571865890816'
    for index in range(1, 50000):
        print("{},{} copy_delivery_order_loop page:{},deliver_order_id:{}".format(threading.current_thread().name,
                                                                     datetime.datetime.now().strftime(
                                                                        "%Y-%m-%d %H:%M:%S"),page_num, delivery_order_id))
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
        ## 查询详情
        details = get_delivery_details(delivery_order_ids)
        if len(details) == 0:
            continue
        for detail in details:
            ls = [(k, v) for k, v in detail.items() if (v is not None)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into erp_iom.sub_delivery_order (" + keys + ") values (" + values + ");"
            delivery_order_insert_sql.append(sql)


        task = executor.submit(insert_iom, delivery_order_insert_sql)
        all_task.append(task)
        page_num += 1
        delivery_order_id = delivery_order_ids[-1]

        if len(all_task) > 100:
            print("delivery order insert task num gt 100")
            while len(all_task) > 0:
                for task in all_task:
                    if task.done():
                        all_task.remove(task)
                print("delivery order insert suspend 5 seconds task num : %d" % len(all_task))
                time.sleep(5)
        wait(all_task, return_when=ALL_COMPLETED)


def copy_return_order_loop(page_size):
    page_num = 1
    id = None
    for index in range(1, 100000):
        print("copy_return_order_loop page:{},id:{}".format(page_num, id))
        order = copy_return_order(id, page_size)
        if order[0] is False:
            break
        id = order[-1]
        page_num += 1


def copy_purchase_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_order_loop page:{}".format(page_num))
        if copy_purchase_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_refund_order_loop(page_size):
    page_num = 1
    refund_id = None
    for index in range(1, 100000):
        print("copy_refund_order_loop page:{},refund_id:{}".format(page_num, refund_id))
        order = copy_refund_order(refund_id, page_size)
        if order[0] is False:
            break
        refund_id = order[-1]
        page_num += 1


def copy_no_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_no_order_loop page:{}".format(page_num))
        if copy_no_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_purchase_price_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_price_loop page:{}".format(page_num))
        if copy_purchase_price((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


if __name__ == '__main__':
    # page_num = 1
    # page_size = 1000
    # for index in range(1, 100000):
    #     copy_delivery_order((page_num - 1) * page_size, page_size)
    #     copy_return_order((page_num - 1) * page_size, page_size)
    #     copy_purchase_order((page_num - 1) * page_size, page_size)
    #     copy_refund_order((page_num - 1) * page_size, page_size)
    #     copy_no_order((page_num - 1) * page_size, page_size)
    #     page_num += 1
    # copy_delivery_order_loop(1000)

    # multiprocessing.Process(target=copy_purchase_order_loop, args=(1000,), name='purchase_order').start()
    # multiprocessing.Process(target=copy_no_order_loop, args=(1000,), name='no_order').start()
    #
    # multiprocessing.Process(target=copy_purchare_refund_order_loop, args=(1000,), name='purchase_refund').start()

    multiprocessing.Process(target=copy_delivery_order_mutil_thread, args=(500,), name='delivery_order').start()
    # multiprocessing.Process(target=copy_return_order_loop, args=(1000,), name='return_order').start()
    multiprocessing.Process(target=copy_trade_order_mutil_thread, args=(500,), name='trade_order').start()
    # multiprocessing.Process(target=copy_no_order_loop, args=(1000,), name='no_order').start()
