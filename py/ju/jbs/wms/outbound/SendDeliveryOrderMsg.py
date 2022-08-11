#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import random

import snowflake.client
import time
import numpy as np
import mq
from toollib.snowflake import snow


def getSnowflakeCode():
    guid = snow.guid()
    return "WCK" + time.strftime("%Y%m%d", time.localtime()) + str(guid)


def buildOrderMap(warehouseCodes, logisticsCodes, outDeliveryOrderId):
    orderMap = {}
    orderMap.setdefault("buyerName", "fei")
    orderMap.setdefault("cartonCode", "001")
    orderMap.setdefault("expectWeight", random.uniform(1, 5))
    orderMap.setdefault("logisticsCode", logisticsCodes if logisticsCodes is not None else random.choice(logisticsCodes))
    orderMap.setdefault("logisticsMode", "DISTRIBUTION")
    orderMap.setdefault("orderType", "SALES_OUTBOUND")
    orderMap.setdefault("outDeliveryOrderId",
                        outDeliveryOrderId if outDeliveryOrderId is not None else getSnowflakeCode())
    orderMap.setdefault("ownerCode", "OW003")
    orderMap.setdefault("platCode", "TB")
    orderMap.setdefault("receiverCity", "西安市")
    orderMap.setdefault("receiverDetailAddress", "小城故事")
    orderMap.setdefault("receiverDistrict", "莲湖区")
    orderMap.setdefault("receiverMobile", "15000000000")
    orderMap.setdefault("receiverName", "fei")
    orderMap.setdefault("receiverProvince", "陕西省")
    orderMap.setdefault("senderCity", "西安市")
    orderMap.setdefault("senderDetailAddress", "鱼化寨街道")
    orderMap.setdefault("senderDistrict", "莲湖区")
    orderMap.setdefault("senderMobile", "15000000000")
    orderMap.setdefault("senderName", "jbs")
    orderMap.setdefault("senderProvince", "陕西省")
    orderMap.setdefault("shopCode", "SH001")
    orderMap.setdefault("sourceOrderId", "")
    orderMap.setdefault("tradeTime", 1659684654675)
    orderMap.setdefault("warehouseCode", warehouseCodes if warehouseCodes is not None else random.choice(warehouseCodes))
    return orderMap


def buildDetail(originGoodsCodes):
    np.random.shuffle(originGoodsCodes)
    goodsSpecies = random.randint(1, 5)
    details = []
    for code in originGoodsCodes[0:goodsSpecies]:
        detailMap = {}
        detailMap.setdefault("goodsCode", code)
        detailMap.setdefault("goodsNum", random.randint(1, 50))
        details.append(detailMap)

    return details


def send(warehouseCode,logisticsCode,detail):
    for a in range(1, random.randint(1, 100)):
        order_map = buildOrderMap(warehouseCode, logisticsCode, None)
        order_map.setdefault("orderDetails", detail)
        orderMsgJson = json.dumps(order_map, ensure_ascii=False)
        print(orderMsgJson)
        mq.get_rabbitmq().producter(exchange="delivery_order", queue="delivery_order", routing_key="delivery_order",
                                    message=orderMsgJson)


def create_same_data(warehouseCodes,logisticsCodes,goodsCodes):
    for i in range(1, 1000):
        detail = buildDetail(goodsCodes)
        warehouseCode = random.choice(warehouseCodes)
        logisticsCode = random.choice(logisticsCodes)
        send(warehouseCode, logisticsCode, detail)
        # multiprocessing.Process(target=send,args=(warehouseCode,logisticsCode,detail)).start()

def create_same_warehouse_data(warehouseCodes,logisticsCodes,goodsCodes):
    for warehouseCode in warehouseCodes:
        detail = buildDetail(goodsCodes)
        for i in range(1, 3000):
            logisticsCode = random.choice(logisticsCodes)
            send(warehouseCode, logisticsCode, detail)


# snowflake_start_server 启动 雪花算法服务
if __name__ == '__main__':

    warehouseCodes = ["WH0019", "WH0001", "WH0024", "WH0016", "WH0020", "WH0021", "WH0004",  "WH0022", "WH0003",
                      "WH0025"]
    logisticsCodes = ["LG0001", "LG0002", "LG0003", "LG0004", "LG0006", "LG0007", "LG0017", "LG0053", "LG0055",
                      "LG0060"]

    goodsCodes = ["JBS-ZNLJT-6715-GD", "JBS-ZNLJT-6715-GY", "JBS-ZNLJT-6715D-GD", "JBS-ZNLJT-7910-GY",
                  "JBS-ZNLJT-7910D-GY", "JBS-ZNLJT-809-CDK", "JBS-ZNLJT-809-DCK", "JBS-ZNLJT-810-CDK",
                  "JBS-ZNLJT-810-DCK", "JBS-ZNLJT-811-CDK", "JBS-ZNLJT-811-DCK", "JBS-ZNLJT-CFY12-GWT",
                  "JBS-ZNLJT-CFY12-OG", ]

    create_same_warehouse_data(warehouseCodes,logisticsCodes,goodsCodes)
    #create_same_data()


