#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import mq
import db
import schedule
import multiprocessing
import time


def arr_size(arr, size):
    s = []
    for i in range(0, int(len(arr)) + 1, size):
        c = arr[i:i + size]
        s.append(c)
    newlist = [x for x in s if x]
    return newlist


def get_queue_name(deliveryOrderId):
    #return "analyze_order_refresh_" + str(hash(deliveryOrderId) % 6)
    return "wms-stock_analyze_order_refresh_wms-stock_" +  str(hash(deliveryOrderId) & (4-1))

def test_send():
    msg_map = {}
    msg_map["deliveryOrderIds"] = ["WCK2209191571755897832783872"]
    msg_map["msgType"] = "ADD"
    mq.get_rabbitmq().producter(exchange="wms-stock_analyze_order_refresh_wms-stock_0", queue="wms-stock_analyze_order_refresh_wms-stock_0", routing_key="wms-stock_analyze_order_refresh_wms-stock_0",
                                message=json.dumps(msg_map, ensure_ascii=False))

def send_thread(k, v,msgType):
    ids_parts = arr_size(v, 50)
    for ids in ids_parts:
        msg_map = {}
        msg_map["deliveryOrderIds"] = ids
        msg_map["msgType"] = msgType
        mq.get_rabbitmq().producter(exchange=k, queue=k, routing_key=k,
                                    message=json.dumps(msg_map, ensure_ascii=False))

        print("send ids.size" + str(len(ids)) + " name" + k+" msgType:"+ msgType)


def send_msg():
    print(time.strftime("%Y%m%d-%H:%M:%S", time.localtime()) + "执行一次发送订单分析任务")
    global get

    ids_all = db.getErrorAnalyzeOrder()
    #ids_all = db.getErrorAnalyzeOrderById("f199aefa50d64c61e0da03cc848b3be8")

    queue_ids_map = {}
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_0", [])
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_1", [])
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_2", [])
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_3", [])
    for ids_map in ids_all:
        id_ = ids_map[0]
        name = get_queue_name(id_)
        get = queue_ids_map.get(name).append(id_)
    for k, v in queue_ids_map.items():
        send_thread(k, v, "SUB")
        send_thread(k, v, "ADD")
        # print(k)
        # multiprocessing.Process(target=send_thread, args=(k, v), name=k).start()

if __name__ == '__main__':
    send_msg()
    #test_send()