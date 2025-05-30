# -*- coding: utf-8 -*-

import json
#from toollib.snowflake import snow
from pymysql_comm import UsingOnlineOMS as online
import hashlib
from toollib.snowflake import snow
from py.ju.jbs.mes.order_plan import mq


# def getSnowflakeCode():
#     guid = snow.guid()
#     return time.strftime("%Y%m%d", time.localtime()) + str(guid)

def get_stock():
    sql = "SELECT distinct  source_order_id from `mes_order`.`produce_stock_lock` where lock_num > 0  and lock_level > 0 "
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_ww_idx(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    uuid = m2.hexdigest()
    return uuid
if __name__ == '__main__':
    stocks = get_stock()
    for stock in stocks:
        source_order_id = stock['source_order_id']
        items = []
        item = {}
        item["msgId"] = snow.guid()
        item["lockVersionId"] = source_order_id
        item["planOrderId"] = 'UN'+snow.guid()
        items.append(item)

        msg={}
        msg["unlockItems"] = items
        mq.get_rabbitmq().producter(exchange='mes-order_sales_order_stock_unlock_mes-order',
                                    queue='mes-order_sales_order_stock_unlock_mes-order',
                                    routing_key='mes-order_sales_order_stock_unlock_mes-order',
                                    message=json.dumps(msg, ensure_ascii=False))



