
from pymysql_online import UsingMysql as online
import time

import pandas
import xlrd
from pymysql_online import UsingMysql as online
from toollib.snowflake import snow

def getSnowflakeCode():
    guid = snow.guid()
    return time.strftime("%Y%m%d", time.localtime()) + str(guid)
def get_product():
    ## 虚拟品，赠品，无编码配件
    sql = "SELECT goods_code FROM oms_product.`product_sku` where sku_type in (4,7,10) and status = 1 "
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_warehouse():
    sql = "SELECT warehouse_code FROM oms_product.`warehouse` where warehouse_use_type = 2 and status = 1"
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


sql = 'insert into agent_settle_stock_price(stock_price_id,inbound_order_id,inbound_order_type,warehouse_code,' \
      'goods_code, stock_num,available_num,cost_price,inbound_time,relative,remark) values'
from_values = "('{}','IMPORT20230802',1,'{}',{},2147483647,2147483647,0,'2023-08-31 00:00:00',false,'初始化')"

if __name__ == '__main__':
    warehouses = get_warehouse()
    warehouse_codes =[]
    for warehouse in warehouses:
        warehouse_codes.append(warehouse["warehouse_code"])

    product_skus = get_product()
    goods_codes = []
    for product_sku in product_skus:
        goods_codes.append(product_sku["goods_code"])
    #goods_codes.append("CJ-KBZ")
    # print(len(warehouse_codes))
    # print(len(goods_codes))
    file = open("D:\\项目相关\\fms\\代发期初库存虚拟品&赠品&无编码配件.sql", "w", encoding='utf-8')
    file.write(sql)
    for warehouse_code in set(warehouse_codes):
        for goods_code in set(goods_codes):
            write_sql = from_values.format(getSnowflakeCode(), warehouse_code, repr(goods_code))
            file.write(write_sql)
            file.write(",")
            file.write("\n")
    file.flush()
    file.close()




