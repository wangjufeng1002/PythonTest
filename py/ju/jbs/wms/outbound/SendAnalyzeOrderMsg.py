#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import mq
import db
import schedule
import multiprocessing
import time
def arr_size(arr,size):
    s=[]
    for i in range(0,int(len(arr))+1,size):
        c=arr[i:i+size]
        s.append(c)
    newlist = [x for x in s if x]
    return newlist

def get_queue_name(deliveryOrderId):
    return "analyze_order_refresh_"+str(hash(deliveryOrderId) % 3)


def send_msg():
    print(time.strftime("%Y%m%d-%H:%M:%S", time.localtime()) + "执行一次发送订单分析任务")
    global get
    db.updateDeliveryOrderExpress("2022-08-09 00:00:00")
    start_time = "2022-08-09 00:00:00"
    ids_all = db.getDeliveryOrderIds(start_time)
    queue_ids_map = {}
    queue_ids_map.setdefault("analyze_order_refresh_0", [])
    queue_ids_map.setdefault("analyze_order_refresh_1", [])
    queue_ids_map.setdefault("analyze_order_refresh_2", [])
    # print(ids_all)
    for ids_map in ids_all:
        id_ = ids_map["delivery_order_id"]
        name = get_queue_name(id_)
        get = queue_ids_map.get(name).append(id_)
    for k, v in queue_ids_map.items():
        ids_parts = arr_size(v, 50)
        for ids in ids_parts:
            msg_map = {}
            msg_map["deliveryOrderIds"] = ids
            msg_map["msgType"] = "ADD"
            mq.get_rabbitmq().producter(exchange=k, queue=k, routing_key=k,
                                        message=json.dumps(msg_map, ensure_ascii=False))


if __name__ == '__main__':
    send_msg()
    # schedule.every(5).minutes.do(send_msg)
    # while True:
    #   schedule.run_pending()

    #send_msg()

