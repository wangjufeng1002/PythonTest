import multiprocessing
import random
import threading
import snowflake.client
import time
import numpy as np
import db
from toollib.snowflake import snow

sql_refund_appointment_order = '''INSERT INTO `wms_stock`.`refund_appointment_order` 
(`refund_appointment_order_id`, `affiliate_order_id`, `delivery_order_id`, `receipt_warehouse_code`, `order_status`,
 `after_sales_type`, `express_code`, `logistics_company`, `refund_reason`, `mark_id`, `create_time`, `update_time`) 
VALUES ('{refund_appointment_order_id}', '{affiliate_order_id}', '', '{receipt_warehouse_code}', 10, 1, '{express_code}', '物流公司', 
'就是想退款', '', now(), now()); '''

sql_refund_appointment_order_detail = '''INSERT INTO `wms_stock`.`refund_appointment_order_detail` 
(`refund_appointment_order_detail_id`, `refund_appointment_order_id`, `source_warehouse_code`, `inbound_status`, `goods_code`, `appointment_num`, `inbound_num`, `create_time`, `update_time`) 
VALUES ('{refund_appointment_order_detail_id}', '{refund_appointment_order_id}', '{source_warehouse_code}', 10, '{goods_code}', 1, 0, now(), now());
'''

# warehouse_codes = ["WH0001","WH0009", "WH0003", "WH0019", "WH0024", "WH0016", "WH0020", "WH0021", "WH0004", "WH0022", "WH0003",
#                    "WH0025", "WH0010"]
warehouse_codes = ["WH0253","WH0045","WH0048","WH0044","WH0045","WH0046","WH0056"]
goods_codes = ["JBS-ZNLJT-6715-GD", "JBS-ZNLJT-6715-GY", "JBS-ZNLJT-6715D-GD", "JBS-ZNLJT-7910-GY",
               "JBS-ZNLJT-7910D-GY", "JBS-ZNLJT-809-CDK", "JBS-ZNLJT-809-DCK", "JBS-ZNLJT-810-CDK",
               "JBS-ZNLJT-810-DCK", "JBS-ZNLJT-811-CDK", "JBS-ZNLJT-811-DCK", "JBS-ZNLJT-CFY12-GWT",
               "JBS-ZNLJT-CFY12-OG", ]


def get_refund_appointment_order_id():
    # snowflake.client.setup("localhost", 8910)
    # guid = snowflake.client.get_guid()
    guid = snow.guid()
    return "TY" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)


def get_refund_appointment_order_detail_id():
    guid = snow.guid()
    return time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)


def get_affiliate_order_id():
    guid = snow.guid()
    return time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)


def get_express_code():
    guid = snow.guid()
    return "ZT" + str(guid);


def create_refund_appointment_order():
    global goods_codes
    # 详情数量
    details_num = random.randint(1,5)
    order_id = get_refund_appointment_order_id()
    np.random.shuffle(goods_codes)
    goods_codes = np.random.choice(goods_codes, details_num)
    details_sql = []
    for goods_code in goods_codes:
        detail_format = sql_refund_appointment_order_detail.format(
            refund_appointment_order_detail_id=get_refund_appointment_order_detail_id(),
            refund_appointment_order_id=order_id,
            source_warehouse_code=random.choice(warehouse_codes),
            goods_code=goods_code)
        details_sql.append(detail_format)
    order_sql = sql_refund_appointment_order.format(refund_appointment_order_id=order_id,
                                                    affiliate_order_id=get_affiliate_order_id(),
                                                    receipt_warehouse_code='WH0392',
                                                    express_code=get_express_code())
    db.inset_refund_appointment_order(order_sql=order_sql, details_sql=details_sql)


if __name__ == '__main__':
    for index in range(1, 1):
        create_refund_appointment_order()
        print(index)
