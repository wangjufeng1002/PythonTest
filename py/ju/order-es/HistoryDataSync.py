#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
        bodys = []
        for order in orders:
            orderId = order.get("orderId")
            # 获取 orderLabel
            orderLables = db.getOrderLabel(orderId)
            orderPackage = db.getPackage(orderId)
            orderProducts = db.getProduts(orderId)
            orderCustDetail = db.getOrderCustDetailByCustId(order.get("custId"))
            refundAudits = db.getRefundAudits(orderId)
            orderShareAmounts = db.getOrderShareAmouns(orderId)

            if orderLables is None or len(orderLables) == 0:
                orderLable = None
                orderLableComment = None
            else:
                orderLable = orderLables[0].get("orderLable")
                orderLableComment = orderLables[0].get("orderLableComment")

            if orderCustDetail is None or len(orderCustDetail) == 0:
                cust_detail_ = None
            else:
                cust_detail_ = orderCustDetail[0]

            try:
                body = {
                    "_index": index,
                    "_type": inde_type,
                    "_op_type": 'update',
                    "_id": orderId,
                    "doc_as_upsert": True,
                    "doc": {
                        "shopId": order.get("shopId"),
                        "orderId": order.get("orderId"),
                        "status": order.get("status"),
                        "syncStatus":order.get("syncStatus"),
                        "shippingMethodType": order.get("shippingMethodType"),
                        "orderMode": order.get("orderMode"),
                        "orderType": order.get("orderType"),
                        "fromPlatForm": order.get("fromPlatForm"),
                        "externalOrderId": order.get("externalOrderId"),
                        "receiverName": order.get("receiverName"),
                        "receiverMobileTel": order.get("receiverMobileTel"),
                        "isPresale": order.get("isPresale"),
                        "sendDate": None if order.get("sendDate") is None else datetime.datetime.strftime(
                            order.get("sendDate"),
                            "%Y-%m-%d %H:%M:%S"),
                        "orderInnerType": order.get("orderInnerType"),
                        "payDate": None if order.get("payDate") is None else datetime.datetime.strftime(
                            order.get("payDate"),
                            "%Y-%m-%d %H:%M:%S"),
                        "orderCreationDate": None if order.get(
                            "orderCreationDate") is None else datetime.datetime.strftime(
                            order.get("orderCreationDate"), "%Y-%m-%d %H:%M:%S"),
                        "lastChangeDate": None if order.get(
                            "lastChangeDate") is None else datetime.datetime.strftime(
                            order.get("lastChangeDate"), "%Y-%m-%d %H:%M:%S"),
                        "orderCancelDate": None if order.get("orderCancelDate") is None else datetime.datetime.strftime(
                            order.get("orderCancelDate"), "%Y-%m-%d %H:%M:%S"),
                        "waitDistributionDate": None if order.get(
                            "waitDistributionDate") is None else datetime.datetime.strftime(
                            order.get("waitDistributionDate"), "%Y-%m-%d %H:%M:%S"),
                        "waitShippingResultDate": None if order.get(
                            "waitShippingResultDate") is None else datetime.datetime.strftime(
                            order.get("waitShippingResultDate"),
                            "%Y-%m-%d %H:%M:%S"),
                        "shippingLastEventDate": None if order.get(
                            "shippingLastEventDate") is None else datetime.datetime.strftime(
                            order.get("shippingLastEventDate"), "%Y-%m-%d %H:%M:%S", ),
                        "waitPickGoodsDate": None if order.get(
                            "waitPickGoodsDate") is None else datetime.datetime.strftime(
                            order.get("waitPickGoodsDate"), "%Y-%m-%d %H:%M:%S"),
                        "orderLabel": orderLable,
                        "paymentMethodType": order.get("paymentMethodType"),
                        "orderLabelComment": orderLableComment,
                        "shippingFeeAmount" : order.get("shippingFeeAmount"),
                        "realPaidAmount": order.get("realPaidAmount"),
                        "totalAmount": order.get("totalAmount"),
                        "payableAmount": order.get("payableAmount"),
                        "custInfo": cust_detail_,
                        "externalProductId": order.get("externalProductId"),
                        "products": None if orderProducts is None or len(orderProducts) == 0 else orderProducts,
                        "expresses": None if orderPackage is None or len(orderPackage) == 0 else orderPackage,
                        "refundAudits": None if refundAudits is None or len(refundAudits) == 0 else refundAudits,
                        "orderShareAmounts": None if orderShareAmounts is None or len(orderShareAmounts) == 0 else orderShareAmounts
                    }
                }
            except Exception as e:
                logging.error("同步订单 %d 异常" % orderId)
                logging.info("错误的id=%d", order.get("id"))
                raise e
            bodys.append(delNullValue(body))
        try:
            helpers_bulk = helpers.bulk(client=EsConfig.es, actions=bodys, index=index,
                                        doc_type=inde_type,
                                        chunk_size=len(bodys), raise_on_error=True)
            print(helpers_bulk)
            startId = orders[len(orders) - 1].get("id")
            if startId == endId:
                break
        except Exception as e:
            raise e


threading.Thread(target=process, args=(startId, endId, 20, " 线程1 "), name=" 线程1 ").start()
