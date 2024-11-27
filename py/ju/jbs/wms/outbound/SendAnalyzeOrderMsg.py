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


def send_thread(k, v):
    ids_parts = arr_size(v, 50)
    for ids in ids_parts:
        msg_map = {}
        msg_map["deliveryOrderIds"] = ids
        msg_map["msgType"] = "ADD"
        mq.get_rabbitmq().producter(exchange=k, queue=k, routing_key=k,
                                    message=json.dumps(msg_map, ensure_ascii=False))
        print("send ids.size" + str(len(ids)) + " name" + k)


def send_msg():
    print(time.strftime("%Y%m%d-%H:%M:%S", time.localtime()) + "执行一次发送订单分析任务")
    global get
    # db.updateDeliveryOrderExpress("2022-09-01 16:20:00")
    start_time = "2024-01-17 00:00:00"
    ids_all = db.getDeliveryOrderIds(start_time)
    print(len(ids_all))
    queue_ids_map = {}
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_0", [])
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_1", [])
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_2", [])
    queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_3", [])
    # queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_4", [])
    # queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_5", [])
    # queue_ids_map.setdefault("wms-stock_analyze_order_refresh_wms-stock_0", [])
    # print(ids_all)
    for ids_map in ids_all:
        id_ = ids_map["delivery_order_id"]
        name = get_queue_name(id_)
        get = queue_ids_map.get(name).append(id_)
    for k, v in queue_ids_map.items():
        multiprocessing.Process(target=send_thread, args=(k, v), name=k).start()
        ids_parts = arr_size(v, 50)
        for ids in ids_parts:
            msg_map = {}
            msg_map["deliveryOrderIds"] = ids
            msg_map["msgType"] = "ADD"
            mq.get_rabbitmq().producter(exchange=k, queue=k, routing_key=k,
                                        message=json.dumps(msg_map, ensure_ascii=False))
            print("send ids.size"+str(ids)+" name"+k)


if __name__ == '__main__':
    send_msg()
    # schedule.every(1).minutes.do(send_msg)
    # while True:
    #   schedule.run_pending()

    # send_msg()
