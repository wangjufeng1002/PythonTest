
from ju.jbs.common.db.db_connect_pool import ONLINE_POOL
import copy


def get_stock(goods_codes):
    goods_code_param = ','.join(repr(str(goods_code)) for goods_code in goods_codes)
    sql = "SELECT * FROM wms_work.`stock` where goods_code in (%s)" % (goods_code_param)
    with ONLINE_POOL() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_delivery_order(ids):
    ids = ','.join(repr(str(ids)) for id in ids)
    sql = "SELECT * FROM wms_stock.`delivery_order` where delivery_order_id in (%s)" % (ids)
    with ONLINE_POOL() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()
