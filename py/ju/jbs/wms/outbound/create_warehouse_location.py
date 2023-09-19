import hashlib
import multiprocessing
import random

from py.ju.jbs.wms.outbound.db_connect_pool import POOL

sql_format = "INSERT INTO `oms_product`.`warehouse_location`" \
             " (`warehouse_location_code`, `warehouse_location_name`, `warehouse_code`, `warehouse_area_code`, `channel`, `warehouse_location_type`," \
             " `ww_idx`, `special_mark`, `create_by`, `update_by`)" \
             " VALUES ('{warehouse_location_code}', '{warehouse_location_name}', '{warehouse_code}', '{warehouse_area_code}', " \
             "'通道', 2, '{ww_idx}', 0, '1506441085466206208'," \
             " '456585561941749760')"


def get_ww_idx(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    uuid = m2.hexdigest()
    print(multiprocessing.current_process().name + "===" + uuid)
    return uuid


warehouse_codes = ["WH0001"]


def create_wlc(wlc_prefix, wc):
    for i in range(1,5000):
        wlc= wlc_prefix + str(i)
        wac = '02H'
        sql = sql_format.format(warehouse_location_code=wlc, warehouse_location_name=wlc, warehouse_code=wc,
                                warehouse_area_code=wac, channel=wlc, ww_idx=get_ww_idx(wc + wlc))

        with POOL.connection() as conn:
            conn.cursor().execute(sql)
            conn.commit()

if __name__ == '__main__':
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for wc in warehouse_codes:
        multiprocessing.Process(target=create_wlc, args=(wc.replace("WH", "") + random.choice(s) + "-", wc)).start()
