# -*- coding: utf-8 -*-

import csv
import time
import json
import pandas
import xlrd
#from toollib.snowflake import snow
from pymysql_comm import UsingOnlineOMS as online
import hashlib
from toollib.snowflake import snow
from py.ju.jbs.mes import mq

# def getSnowflakeCode():
#     guid = snow.guid()
#     return time.strftime("%Y%m%d", time.localtime()) + str(guid)

def get_plan():
    sql = "select t.plan_order_id as plan_order_id from mes_aps.produce_task_order t left join mes_aps.produce_plan_order p on t.plan_order_id = p.plan_order_id" \
          " where t.task_status not in(50, 40) and p.plan_status = 50 group by t.plan_order_id"
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_ww_idx(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    uuid = m2.hexdigest()
    return uuid


if __name__ == '__main__':
    plans = get_plan()
    for plan in plans:
        msg = {}
        msg["planOrderId"] = plan['plan_order_id']


        mq.get_rabbitmq().producter(exchange='mes-aps_plan_order_status_refresh_mes-aps',
                                    queue='mes-aps_plan_order_status_refresh_mes-aps',
                                    routing_key='',
                                    message=json.dumps(msg, ensure_ascii=False))
        print("已发送"+ msg["planOrderId"])



