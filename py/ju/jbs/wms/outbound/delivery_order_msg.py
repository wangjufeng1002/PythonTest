
import json
import time
from ju.jbs.common.db.db_connect_pool import ONLINE_POOL
from ju.jbs.common.db.pymysql_comm import UsingDev as UsingMysql
import datetime
# def get_delivery_order(ids):
#     ids = ','.join(repr(str(id)) for id in ids)
#     sql = "SELECT * FROM `wms_stock`.`delivery_order` where delivery_order_id in (%s)" % (ids)
#     with ONLINE_POOL.connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         return cursor.fetchall()
def get_delivery_order(ids):
    ids = ','.join(repr(str(id)) for id in ids)
    sql = "SELECT * FROM `wms_stock`.`delivery_order` where delivery_order_id in (%s)" % (ids)
    with UsingMysql() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def getOrderType(type):
    if type == 1:
        return 'SALES_OUTBOUND'
    elif type == 2:
        return 'DISTRIBUTION_OUTBOUND'


def buildOrderDone(order):
    order_map = {}
    order_map['deliveryOrderId'] = order['out_delivery_order_id']
    order_map['outDeliveryOrderId'] = order['delivery_order_id']
    order_map['orderType'] = 'SALES_OUTBOUND'
    order_map['expressCode'] = order['express_code']
    order_map['logisticsCompany'] = order['logistics_company']
    order_map['logisticsCode'] = order['logistics_code']
    order_map['dispatchTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    order_map['packWeight'] = float(order['pack_weight'])
    return order_map



def send_done_msg(ids):
    orders = get_delivery_order(ids)
    for order in orders:
        order_map = buildOrderDone(order)
        orderMsgJson = json.dumps(order_map, ensure_ascii=False)
        print(orderMsgJson)


if __name__ == '__main__':
    ids = [
        'WCK2507301950478760085684224',
        'WCK2507301950459810229637120'
    ]
    send_done_msg(ids)