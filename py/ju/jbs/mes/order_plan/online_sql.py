from pymysql_comm import UsingDev as dev
from pymysql_comm import UsingOnline as test
from db_connect_pool import ONLINE_POOL
from toollib.snowflake import snow
import copy


def get_stock(goods_codes):
    goods_code_param = ','.join(repr(str(goods_code)) for goods_code in goods_codes)
    sql = "SELECT * FROM wms_work.`stock` where goods_code in (%s)" % (goods_code_param)
    with ONLINE_POOL() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()
