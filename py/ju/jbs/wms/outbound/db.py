from pymysql_comm import UsingMysql
import datetime
import json
from pymysql.converters import escape_string
from db_connect_pool import POOL

def updateDeliveryOrderExpress(startTime):

    with UsingMysql() as um:
        sql = "update delivery_order set express_code = 'wjf1996' where create_time > '{}' and express_code = ''".format(startTime)
        um.cursor.execute(sql)
        um._conn.commit()

def getDeliveryOrderIds(startTime):
    with UsingMysql() as um:
        sql = "select delivery_order_id from delivery_order  where create_time > '{}'".format(startTime)
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
    sql = "select batch_order_id from batch_order where batch_order_id >= '{}'".format(orderId)
    with UsingMysql() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()