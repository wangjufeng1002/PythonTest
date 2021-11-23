#!
import db
import json
import time
import datetime
import threading, time
import EsConfig
import requests
import schedule
from LoggerEntity import Logger
import os
index="order-index"
inde_type="order_query_key"
logUtils = Logger(filename='./logs/dateCompensation.log', level='info')
httpUtl="http://10.5.25.80:10001/syncOrder?orderId=%d"
def process(startDate,endDate):
    body = '''
    {   
        "from":%d,
        "size": 10000,
        "query": {
        "bool": {
          "filter": [
            {
              "range": {
                "orderCreationDate": {
                  "from": "%s",
                  "to": "%s",
                  "include_lower": true,
                  "include_upper": true,
                  "boost": 1
                }
              }
            }
          ]
        }
      }
    }'''

    orderIds=set()
    sql_group_count = db.getOrderId(startDate,endDate)
    offset =0
    while True:
        es_search = EsConfig.es.search(index=index, doc_type=inde_type, body=body % (offset,startDate, endDate))
        if es_search['hits']['hits'] is None or len(es_search['hits']['hits']) == 0:
            break
        for hit in es_search['hits']['hits']:
           orderIds.add(int(hit["_id"]))
        offset+=10000
    #丢了的数据
    loseOrderIds = []
    for result in sql_group_count:
       if result.get("order_id") not  in orderIds:
           loseOrderIds.append(result.get("order_id"))
    logUtils.logger.info("%s <-> %s  %d"%(startDate,endDate,len(loseOrderIds)))
    for orderId in loseOrderIds:
        os.system("curl "+httpUtl%(int(orderId)))
    #print(es_search)




#nohup python DataCompensation.py  >> logs/nohup-dataCompensation.log 2>&1 &
if __name__ == '__main__':
    EsConfig.initEs("prod")
    db.initDb("test")
    #
    startHour = datetime.datetime.now() + datetime.timedelta(hours=-2280)
    start_date = startHour.strftime("%Y-%m-%d %H")+":00:00"
    #end_date = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H") + " 00:00:00"
    end_date = startHour.strftime("%Y-%m-%d %H") + ":59:59"
    while True:
        process(start_date,end_date)
        startHour = startHour + datetime.timedelta(hours=-1)
        start_date = startHour.strftime("%Y-%m-%d %H") + ":00:00"
        end_date = startHour.strftime("%Y-%m-%d %H") + ":59:59"





