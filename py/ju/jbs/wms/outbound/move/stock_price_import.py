# -*- coding: utf-8 -*-

import csv
import time

import pandas
import xlrd
from pymysql_online import UsingMysql as online
from toollib.snowflake import snow

def getSnowflakeCode():
    guid = snow.guid()
    return time.strftime("%Y%m%d", time.localtime()) + str(guid)

def get_all_warehouse():
    with online() as um:
        sql = "SELECT warehouse_code,warehouse_name FROM oms_product.`warehouse`"
        with online() as um:
            um.cursor.execute(sql)
            return um.cursor.fetchall()


# sql = "insert into agent_settle_stock_price(stock_price_id,inbound_order_id,inbound_order_type,warehouse_code,goods_code,stock_num,available_num," \
#       "cost_price,inbound_time,relative,remark) values ('{}','IMPORT20230801',1,'{}','{}','{}','{}','{}','2023-08-31 00:00:00',false,'初始化');"


sql = 'insert into agent_settle_stock_price(stock_price_id,inbound_order_id,inbound_order_type,warehouse_code,' \
      'goods_code, stock_num,available_num,cost_price,inbound_time,relative,remark) values'

from_values = "('{}','IMPORT20230801',1,'{}','{}','{}','{}','{}','2023-08-31 00:00:00',false,'初始化')"
if __name__ == '__main__':

    warehouse_map = {}
    warehouses = get_all_warehouse()
    for wh in warehouses:
        warehouse_map.setdefault(wh['warehouse_name'].replace('（禁用）',''),wh['warehouse_code'])

    #读取excel
    workbook = xlrd.open_workbook("D:\\项目相关\\fms\\8.31库存快照-合并.xlsx")
    sheets_ = workbook.sheets()[0]
    rows = sheets_.nrows
    count_1 = 0

    file = open("D:\\项目相关\\fms\\代发期初库存价格.sql", "w",encoding='utf-8')
    file.write(sql)
    insert_sql =[]
    for index in range(1, rows):
        values = sheets_.row_values(rowx=index)
        if values[5] == 0:
            continue
        write_sql = from_values.format(getSnowflakeCode(), warehouse_map.get(values[1].replace('（禁用）','')), values[0], values[5], values[5], values[7])
        file.write(write_sql)
        file.write(",")
        file.write("\n")
    file.flush()
    file.close()

