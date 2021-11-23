#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import logging
import db
import json
import time
import datetime
import threading, time
import EsConfig
import sys, getopt
#nohup python  -u HistoryDataSync.py -a prod -s 217154450 -e 3000000000  >>nohup.log 2>&1 &
#nohup python  -u HistoryDataSync.py -a prod -s 197867883 -e 3000000000  >nohup.log 2>&1 &
#nohup python  -u HistoryDataSync.py -a dev -s 162206623 -e 225287085 >nohup.log 2>&1 &

# 取启动参数 -a 配置环境， -s 开始的ID  -e 结束的id
active = "dev"
index = "order-index"
inde_type = "order_query_key"
startId = 1000000
endId = 1000000
opts, args = getopt.getopt(sys.argv[1:], "a:s:e:")
for opt, arg in opts:
    if opt == "-a":
        active = arg
    if opt == '-s':
        startId = int(arg)
    if opt == '-e':
        endId = int(arg)
# 初始化es db
EsConfig.initEs(active)
db.initDb(active)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename="./logs/history-sync.log", level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def delNullValue(body):
    for key in list(body["doc"].keys()):
        if body["doc"][key] is None:
            del body["doc"][key]
    return body


def process(startId, endId, size, threadName):
    while True:
        orders = db.getOrdersByStartIdEndId(startId, endId, size)
        if orders is None or len(orders) == 0:
            break
        logging.info("%s 开始处理 %d <--> %d" % (threadName, orders[0].get("id"), orders[len(orders) - 1].get("id")))
        for order in orders:
            requests.get("http://10.3.253.111:8083/orderEventService/addMissValueFromOrderItems/addOrderApportAmount?orderId=" + str(order.get("orderId")))
            print(order.get("orderId"))

threading.Thread(target=process, args=(startId, endId, 20, " 线程1 "), name=" 线程1 ").start()
