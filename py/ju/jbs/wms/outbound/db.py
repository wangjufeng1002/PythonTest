from ju.jbs.common.db.pymysql_comm import UsingDev as UsingMysql
import datetime
import json
from pymysql.converters import escape_string
from ju.jbs.common.db.db_connect_pool import DEV_POOL as POOL

def updateDeliveryOrderExpress(startTime):

    with UsingMysql() as um:
        sql = "update wms_stock.delivery_order set express_code = 'wjf1996' where create_time > '{}' and express_code = ''".format(startTime)
        um.cursor.execute(sql)
        um._conn.commit()

def getDeliveryOrderIds(startTime):
    with UsingMysql() as um:
        sql = "select delivery_order_id from wms_stock.delivery_order  where order_status=10 and express_code !='' and  create_time > '{}'".format(startTime)
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def inset_delivery_order(order_sql,details_sql):

    with POOL.connection() as conn:
        conn.cursor().execute(order_sql)
        for detail_sql in details_sql:
            conn.cursor().execute(detail_sql)
        conn.cursor().close()
        conn.commit()

def get_batch_order_id(orderId):
    sql = "select batch_order_id from wms_stock.batch_order where batch_order_id >= '{}'".format(orderId)
    with UsingMysql() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_product_codes(num):
    sql = "SELECT DISTINCT(goods_code) FROM oms_product.`product_sku` where status = 1 and deleted = 0 ORDER BY RAND() LIMIT {} ".format(num)
    with UsingMysql() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_warehouse_localtion(warehouse_code):
    sql = "SELECT warehouse_location_code,warehouse_location_type,special_mark, channel,warehouse_area_code FROM oms_product.`warehouse_location`" \
          " where warehouse_code = '{}' and warehouse_area_code not in ('01-BB','01-JJ','19-BB','19-JJ') order by  warehouse_location_code".format(warehouse_code)
    with UsingMysql() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def insert_stock_data(stock_sql):
    with POOL.connection() as conn:
        conn.cursor().execute(stock_sql)
        conn.cursor().close()
        conn.commit()

def getErrorAnalyzeOrder():
    sql = "select delivery_order_id from wms_stock.analyze_order_detail where analyze_order_id in (SELECT analyze_order_id from wms_stock.analyze_order where goods_code_unit like '%$')"
    with POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def getErrorAnalyzeOrderById(anlayzeOrderId):
    sql = "select delivery_order_id from wms_stock.analyze_order_detail where analyze_order_id in ('{}')".format(anlayzeOrderId)
    with POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

def get_move_stock_order():
    sql = "SELECT `move_stock_id`, `move_stock_status`, `goods_num`, `goods_species`, `warehouse_code`, `remark`, `finish_by`, `create_by`, `update_by`, `finish_time`, `create_time`, `update_time`  FROM `wms_work`.`move_stock` LIMIT 0,1000 "
    with POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
def get_move_stock_order_detail():
    sql = "SELECT * FROM `wms_work`.`move_stock_detail` LIMIT 0,1000000 "
    with POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

def insert_test(val):
    sql = "INSERT INTO `wms_stock`.`test` (`logistics_types`, `logistics_types_set`) VALUES ( '{}','{}')".format(val,val)
    with POOL.connection() as conn:
        conn.cursor().execute(sql)
        conn.cursor().close()
        conn.commit()

