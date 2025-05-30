
# -*- coding: utf-8 -*-



def get_stock(goods_codes):
    goods_code_param = ','.join(repr(str(goods_code)) for goods_code in goods_codes)
    sql = "SELECT * FROM wms_work.`stock` where goods_code in (%s)" % (goods_code_param)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()