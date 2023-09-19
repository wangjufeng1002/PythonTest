#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import multiprocessing
import random

I = random.randint(1, 500)
import threading

import snowflake.client
import time
import numpy as np
import mq
import db
from toollib.snowflake import snow

sql_order = '''INSERT INTO `wms_stock`.`delivery_order` (`delivery_order_id`, `out_delivery_order_id`, `batch_order_id`, `source_order_id`, `decrypt_id`, `order_status`, `print_param_acquire_status`, `print_param`, `print_plat`,
 `print_status`, `owner_code`, `order_type`, `plat_code`,
 `shop_code`, `goods_num`, `goods_species`, `goods_type`, `carton_code`, `expect_weight`, `single_plan`, `logistics_code`, `logistics_company`, 
 `logistics_mode`, `express_code`, `mark_sort`, `mark_id`, `sender_name`, `sender_mobile`, `sender_province`, `sender_city`,
  `sender_district`, `sender_detail_address`, `buyer_name`, `receiver_name`, `receiver_mobile`, `receiver_province`,
   `receiver_city`, `receiver_district`, `receiver_town`, `receiver_detail_address`, `buyer_remark`, `seller_remark`,
    `warehouse_code`, `create_by`, `order_pick_by`, `pack_weight`, `pack_length`, `pack_width`, `pack_height`,
     `lock_stock_status`, `exception_type`, `print_param_fail_reason`, `outer_remark`, `serial_no`, `trade_time`, `print_num`,
      `frozen_status`,`auto_mark_type`, `delivery_time`, `outbound_time`)
 VALUES ('{delivery_order_id}', '{out_delivery_order_id}', '', '', '', 10, 30, '', '', 10, 'OW003', 2, 'TB', 
 'SH001', '{goods_num}', '{goods_species}', '{goods_type}', 'YGX', 1.201, b'0', '{logistics_code}', '', 2, '{express_code}', 0, '', 'jbs',
  '15000000000', '陕西省', '西安市', '莲湖区', '鱼化寨街道', 'fei', 'fei', '15000000000', 
  '陕西省', '西安市', '莲湖区', '', '小城故事', '', '', '{warehouse_code}', '', '', 0.00000, 0.00, 0.00, 0.00, 10, 1, '', '', '',
   '2022-08-05 15:30:55', 0, b'0',  0,'1970-01-01 08:00:01', '1970-01-01 08:00:01');

'''

sql_detail = ''' INSERT INTO `wms_stock`.`delivery_order_detail` (`delivery_order_detail_id`, `delivery_order_id`, `goods_code`, `plat_sku_id`, `plat_sku_name`, `plat_spu_id`, `plat_spu_name`, `goods_num`) VALUES('{delivery_order_detail_id}', '{delivery_order_id}', '{goods_code}', '', '', '', '', '{goods_num}');'''


def get_deliveryOrder_id():
    # snowflake.client.setup("localhost", 8910)
    # guid = snowflake.client.get_guid()
    guid = snow.guid()
    return "WCK" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)


def get_deliveryOrder_detail_id():
    guid = snow.guid()
    return time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)


def buildDetail(originGoodsCodes):
    # np.random.shuffle(originGoodsCodes)
    # goodsSpecies = 1
    # details = []
    # for code in originGoodsCodes[0:goodsSpecies]:
    #     detailMap = {}
    #     detailMap.setdefault("goodsCode", code)
    #     detailMap.setdefault("goodsNum", random.randint(1, 50))
    #     details.append(detailMap)
    # return details
    details = []
    for code in originGoodsCodes:
        detailMap = {}
        detailMap.setdefault("goodsCode", code)
        detailMap.setdefault("goodsNum", 1)
        details.append(detailMap)
    return details


def buildDetail_V2(num):
    goodsCodes = list(map(lambda x: x['goods_code'], db.get_product_codes(num)))
    details = []
    for code in goodsCodes:
        detailMap = {}
        detailMap.setdefault("goodsCode", code)
        detailMap.setdefault("goodsNum", random.randint(1, 100))
        details.append(detailMap)
    return details


def countGoodsNum(orderDetails):
    goods_num = 0
    for detail in orderDetails:
        goods_num += detail.get("goodsNum")
    return goods_num


def create_order(warehouseCodes, warehouse_code, logisticsCodes, logistics_code, goodsCodes, prepareDetails):
    order_id = get_deliveryOrder_id()

    out_order_id = get_deliveryOrder_id()

    # 生成组合装订单
    details = prepareDetails if prepareDetails is not None else buildDetail(random.choice(combin_groups))
    # details = prepareDetails if prepareDetails is not None else buildDetail(goodsCodes)
    # details = prepareDetails if prepareDetails is not None else buildDetail_V2(10)
    goods_num = countGoodsNum(details)

    #warehouse_code = warehouse_code if warehouse_code is not None else random.choice(warehouseCodes)

    warehouse_code = 'WH0001'
    logistics_code = logistics_code if logistics_code is not None else random.choice(logisticsCodes)

    order_sql = sql_order.format(delivery_order_id=order_id, out_delivery_order_id=out_order_id,
                                 goods_num=goods_num, goods_species=len(details),
                                 goods_type=1 if (len(details) == 1 and goods_num == 1) else 2,
                                 logistics_code=logistics_code, warehouse_code=warehouse_code, express_code=snow.guid()
                                 )
    detail_sql = []
    for detail in details:
        detail_sql.append(
            sql_detail.format(delivery_order_detail_id=get_deliveryOrder_detail_id(), delivery_order_id=order_id,
                              goods_code=detail.get("goodsCode"), goods_num=detail.get("goodsNum")
                              ))
    try:
        db.inset_delivery_order(order_sql, detail_sql)
    except:
        pass

    print("thred:{},delivert_order_id={},warehouse_code={} logistics_code={}".format(
        multiprocessing.current_process().name, order_id, warehouse_code, logistics_code))


warehouse_codes = ["WH0001", "WH0019", "WH0024", "WH0016", "WH0020", "WH0021", "WH0004", "WH0022", "WH0003",
                   "WH0025"]
logistics_codes = ["LG0004", "LG0001", "LG0002", "LG0003"]

goods_codes = ["JBS-ZNLJT-6715-GD", "JBS-ZNLJT-6715-GY", "JBS-ZNLJT-6715D-GD", "JBS-ZNLJT-7910-GY",
               "JBS-ZNLJT-7910D-GY", "JBS-ZNLJT-809-CDK", "JBS-ZNLJT-809-DCK", "JBS-ZNLJT-810-CDK",
               "JBS-ZNLJT-810-DCK", "JBS-ZNLJT-811-CDK", "JBS-ZNLJT-811-DCK", "JBS-ZNLJT-CFY12-GWT",
               "JBS-ZNLJT-CFY12-OG", ]


combin_groups = [
                 ["JBS-281-48", "JBS-281-38"],  #JDZYD-TC157
                 ["JBS-TGQ-2326-2P", "JBS-ZTMTD-CX03-PK","JBS-ZTMTD-8003-GN","JBS-ZTMTD-02-FLR-GN","JBS-ZTMTD-02-FLR-BN","JBS-ZTMTD-02-FLR-GY","JBS-ZTMTD-01-LMR-PK"
                     ,"JBS-ZTMTD-01-LMR-GN","JBS-ZTMTD-01-LMR-GY"], #JBS-TC-009164

                 ["JBS-ST-7301-PK-S", "JBS-ST-7301-PK-M","JBS-ST-7301-PK-L"], #JBS-TC-00240
                 ["JBS-ST-7301-PK-M" , "JBS-ST-7301-BU-M","JBS-ST-7106-PK-M","JBS-ST-7106-BU-M"], #JBS-TC-00231
                 ["JBS-QJQ" , "J-923"], #JBS-TC-007133 禁用

                 ["JBS-PB-AL20-60"],
                 ["JBS-ZNLJT-810-DCK", "JBS-ZNLJT-811-CDK", "JBS-ZNLJT-811-DCK", "JBS-ZNLJT-CFY12-GWT"]
]


def loop_create(detail):
    for wc in warehouse_codes:
        if detail is None:
            detail = buildDetail(goods_codes)
        for lc in logistics_codes:
            for i in range(1, 100):
                create_order(warehouse_codes, wc, logistics_codes, lc, goods_codes, detail)


def test_create_logistic_types():
    logistics_types = [2, 3, 4, 5, 6, 8, 9, 10, 16, 22, 35, 43, 49, 76, 77, 81, 86, 99, 100, 177, 210, 211, 212, 213]
    for c in range(1, 100000):
        types = set()
        for i in range(0, len(logistics_types)):
            types.add(random.choice(logistics_types))
        type_str = ''
        for type in types:
            type_str += str(type) + ","

        type_str = type_str.strip(",")
        db.insert_test(type_str)


# snowflake_start_server 启动 雪花算法服务
if __name__ == '__main__':
    for i in range(1,100):
        create_order(warehouse_codes,None,logistics_codes,None,goods_codes,None)

    # np.random.shuffle(warehouse_codes)
    # loop_create()
    # detail = buildDetail(goods_codes)
    # for i in range(1,20):
    #     multiprocessing.Process(target=loop_create, args=(None,), name="createThread" + str(i)).start()


    #create_order(warehouse_codes, None, logistics_codes, None, goods_codes, None)

    # for i in range(1,50):
    #     multiprocessing.Process(target=test_create_logistic_types, name="createThread" + str(i)).start()
