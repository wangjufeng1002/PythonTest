import datetime
import json
from pymysql.converters import escape_string
from wms_online_query_con import POOL as wms_pool
from erp_online_query_con import POOL as erp_pool


def query_imc_order_page(start_time, end_time, page):
    offset = (page - 1) * 1000
    sql = "select delivery_order_id from erp_iom.delivery_order where update_time between '{}' and '{}' and order_status = 6 limit {},1000".format(
        start_time, end_time, offset)
    with erp_pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def query_wms_order(orderIds):
    sql = "select delivery_order_id from wms_stock.delivery_order where out_delivery_order_id in {} and order_status != 30".format(
        orderIds)
    with wms_pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

def query_wms_order_his(orderIds):
    sql = "select delivery_order_id from wms_stock.his_delivery_order where out_delivery_order_id in {} and order_status != 30".format(
        orderIds)
    with wms_pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

def query_wms_order_his_2022(orderIds):
    sql = "select delivery_order_id from wms_stock.his_delivery_order_2022 where out_delivery_order_id in {} and order_status != 30".format(
        orderIds)
    with wms_pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
