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

from queue import Queue


# Imc 出库单
def get_product_sku(page_from, page_size):
    sql = "SELECT * FROM oms_product.`product_sku` limit %d,%d" % (page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_supplier(page_from, page_size):
    sql = "SELECT * FROM srm_supply.`supplier` limit %d,%d" % (page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_warehouse(page_from, page_size):
    sql = "SELECT * FROM oms_product.`warehouse` where warehouse_use_type = 2  limit %d,%d" % (page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_agent_ountbound(min_id, max_id, page_size):
    sql = "SELECT * FROM fms_cost.`agent_settle_stock_outbound` where id > %d  and id <= %d  limit %d" % (
        min_id, max_id, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_agent_price(min_id, max_id, page_size):
    sql = "SELECT * FROM fms_cost.`agent_settle_stock_price` where id > %d  and id <= %d  limit %d" % (
        min_id, max_id, page_size)
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


def copy_product_sku(page_from, page_size):
    product_skus = get_product_sku(page_from, page_size)
    product_sku_insert_sql = []
    if len(product_skus) == 0:
        return False
    for purchase_price in product_skus:
        ls = [(k, v) for k, v in purchase_price.items() if (v is not None and k != 'id')]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert into oms_product.`product_sku` (" + keys + ") values (" + values + " ) on duplicate key update sku_name = " + repr(
            str(purchase_price['sku_name'])) + " ;"
        product_sku_insert_sql.append(sql)
    insert_iom(product_sku_insert_sql)
    return True


def copy_supplier(page_from, page_size):
    suppliers = get_supplier(page_from, page_size)
    supplier_sql = []
    if len(suppliers) == 0:
        return False
    for supplier in suppliers:
        ls = [(k, v) for k, v in supplier.items() if (v is not None and k != 'id')]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert into srm_supply.`supplier` (" + keys + ") values (" + values + " ) on duplicate key update supplier_name = " + repr(
            str(supplier['supplier_name'])) + " ;"
        supplier_sql.append(sql)
    insert_iom(supplier_sql)
    return True


def copy_warehouse(page_from, page_size):
    warehouses = get_warehouse(page_from, page_size)
    warehouse_sql = []
    if len(warehouses) == 0:
        return False
    for warehouse in warehouses:
        ls = [(k, v) for k, v in warehouse.items() if (v is not None and k != 'id')]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert into oms_product.`warehouse` (" + keys + ") values (" + values + " ) on duplicate key update supplier_code = " + repr(
            str(warehouse['supplier_code'])) + " ;"
        warehouse_sql.append(sql)
    print(warehouse_sql)
    # insert_iom(warehouse_sql)
    return True


def copy_product_sku_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_order_loop page:{}".format(page_num))
        if copy_product_sku((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_supplier_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_supplier_loop page:{}".format(page_num))
        if copy_supplier((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_warehouse_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_warehouse_loop page:{}".format(page_num))
        if copy_warehouse((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_agent_outbound_loop(min_id, max_id, page_size):
    executor = ThreadPoolExecutor(max_workers=20, thread_name_prefix="insert_outbound")
    all_task = []
    while True:
        agent_outbounds = get_agent_ountbound(min_id, max_id, page_size)
        sqls = []
        if len(agent_outbounds) == 0:
            break
        for outbound in agent_outbounds:
            ls = [(k, v) for k, v in outbound.items() if (v is not None)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into fms_cost.`agent_settle_stock_outbound`(" + keys + ") values (" + values + ");"
            sqls.append(sql)
        task = executor.submit(insert_iom, sqls)
        all_task.append(task)
        print(
            "%s,%s inset agent outbound size %d" % (threading.current_thread().name,
                                                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    len(agent_outbounds)))
        min_id = agent_outbounds[-1]["id"]

        if len(all_task) > 100:
            print("task num gt 100")
            while len(all_task) > 0:
                for task in all_task:
                    if task.done():
                        all_task.remove(task)
                print("suspend 5 seconds task num : %d" % len(all_task))
                time.sleep(5)
    wait(all_task, return_when=ALL_COMPLETED)


def copy_agent_price_loop(min_id, max_id, page_size):
    executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="insert_price")
    all_task = []
    while True:
        agent_prices = get_agent_price(min_id, max_id, page_size)
        sqls = []
        if len(agent_prices) == 0:
            break
        for price in agent_prices:
            ls = [(k, v) for k, v in price.items() if (v is not None)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into fms_cost.`agent_settle_stock_price`(" + keys + ") values (" + values + ");"
            sqls.append(sql)
        task = executor.submit(insert_iom, sqls)
        all_task.append(task)
        print(
            "%s,%s inset agent price size %d" % (
                threading.current_thread().name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(agent_prices)))
        min_id = agent_prices[-1]["id"]

    wait(all_task, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    # copy_product_sku_loop(1000)
    # copy_supplier_loop(100)

    # copy_agent_outbound_loop(7056971,9999999999, 1000)
    # copy_agent_outbound_loop(7056971,9999999999, 1000)

    multiprocessing.Process(target=copy_agent_outbound_loop,
                            args=(6992338, 99999999999, 3000,),
                            name="copy_agent_outbound_loop").start()

    # multiprocessing.Process(target=copy_agent_price_loop,
    #                         args=(135647, 9999999999, 1000,),
    #                         name="copy_agent_price_loop").start()

    # outbound_max = 7056971
    # price_max = 119663
    #
    # online_outbound_max = 22024164
    # online_price_max = 276611
    #
    # outbound_size = online_outbound_max - outbound_max
    # price_size = online_price_max - price_max
    #
    # outbound_part_size = outbound_size // 5
    # price_part_size = price_size // 5
    #
    # outbound_id = outbound_max
    #
    # price_id = price_max
    #
    # outbound_thread_size = 1
    # while outbound_id <= online_outbound_max:
    #     multiprocessing.Process(target=copy_agent_outbound_loop,
    #                             args=(outbound_id, outbound_id + outbound_part_size, 1000,),
    #                             name="copy_agent_outbound_loop_"+str(outbound_thread_size)).start()
    #     outbound_id = + outbound_part_size
    #     outbound_thread_size +=1
    #
    # price_thread_size = 1
    # while price_id <= online_price_max:
    #     multiprocessing.Process(target=copy_agent_price_loop,
    #                             args=(price_id, price_id + price_part_size, 1000,),
    #                             name="copy_agent_outbound_loop_"+str(price_thread_size)).start()
    #     price_id = + price_part_size
    #     price_thread_size += 1
