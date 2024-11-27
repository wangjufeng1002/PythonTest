# -*- coding: utf-8 -*-

import csv
import time

import pandas
import xlrd
#from toollib.snowflake import snow
from pymysql_comm import UsingOnline as online
import hashlib

# def getSnowflakeCode():
#     guid = snow.guid()
#     return time.strftime("%Y%m%d", time.localtime()) + str(guid)

def get_stock(goods_codes):
    goods_code_param = ','.join(repr(str(goods_code)) for goods_code in goods_codes)
    sql = "SELECT * FROM wms_work.`stock` where goods_code in (%s)" % (goods_code_param)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

sql = "update wms_work.stock_order_change set wwg_idx = '{new_wwg_idx}',goods_code='{new_goods_code}' where wwg_idx = '{old_wwg_idx}' and goods_code='{old_goods_code}';"

def get_ww_idx(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    uuid = m2.hexdigest()
    return uuid
if __name__ == '__main__':
    #读取excel
    workbook = xlrd.open_workbook("D:\\项目相关\\编码汇总.xlsx")
    sheets_ = workbook.sheets()[0]
    rows = sheets_.nrows
    count_1 = 0

    file = open("C:\\Users\\PC\Desktop\\替换\\wms库存变动记录.sql", "w",encoding='utf-8')

    insert_sql =[]
    old_goods_codes = []
    goods_codes_map = {}
    for index in range(1, rows):
        values = sheets_.row_values(rowx=index)
        old_goods_codes.append(values[0])
        goods_codes_map[values[0]] = values[3]
    stocks = get_stock(old_goods_codes)

    for stock in stocks:
        idx = stock['warehouse_code'] + stock['warehouse_location_code'] + goods_codes_map[stock['goods_code']]
        update_sql = sql.format(new_wwg_idx=get_ww_idx(idx), new_goods_code=goods_codes_map[stock['goods_code']],
                                old_wwg_idx=stock['wwg_idx'], old_goods_code=stock['goods_code'])
        file.write(update_sql+"\n")
        print(update_sql)
        #(stock)
    file.flush()
    print(len(stocks))
    print(len(old_goods_codes))

