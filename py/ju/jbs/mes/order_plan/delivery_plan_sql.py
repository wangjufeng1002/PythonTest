# -*- coding: utf-8 -*-

import csv
import time

import pandas
import xlrd
#from toollib.snowflake import snow
from pymysql_comm import UsingOnlineOMS as online
import hashlib

# def getSnowflakeCode():
#     guid = snow.guid()
#     return time.strftime("%Y%m%d", time.localtime()) + str(guid)

def get_delivery_plan(goods_codes):
    goods_code_param = ','.join(repr(str(goods_code)) for goods_code in goods_codes)
    sql = "select delivery_plan_id, warehouse_code, owner_code, goods_code, wog_idx FROM srm_ops.delivery_plan WHERE goods_code  in (%s)" % (goods_code_param)

    print(sql)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

sql = "update srm_ops.delivery_plan  set wog_idx  = '{new_wwg_idx}',goods_code='{new_goods_code}' where delivery_plan_id  = '{delivery_plan_id}';"

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

    file = open("C:\\Users\\PC\Desktop\\替换\\交货计划.sql", "w",encoding='utf-8')

    insert_sql =[]
    old_goods_codes = []
    goods_codes_map = {}
    for index in range(1, rows):
        values = sheets_.row_values(rowx=index)
        old_goods_codes.append(values[0])
        goods_codes_map[values[0]] = values[3]
    delivery_plans = get_delivery_plan(old_goods_codes)

    for plan in delivery_plans:
        idx = plan['warehouse_code'] + plan['owner_code'] + goods_codes_map[plan['goods_code']]
        update_sql = sql.format(new_wwg_idx=get_ww_idx(idx), new_goods_code=goods_codes_map[plan['goods_code']],
                                delivery_plan_id=plan['delivery_plan_id'])
        file.write(update_sql+"\n")
        print(update_sql)

    file.flush()
    print(len(delivery_plans))
    print(len(old_goods_codes))

