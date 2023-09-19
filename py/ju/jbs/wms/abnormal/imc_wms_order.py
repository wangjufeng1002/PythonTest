import db

import time
import datetime
import pandas as pd


def get_wms_error_order_id(id_in_sql):
    error_order_ids = ()
    error_order_ids = error_order_ids + db.query_wms_order(id_in_sql)
    error_order_ids = error_order_ids + db.query_wms_order_his(id_in_sql)
    error_order_ids = error_order_ids + db.query_wms_order_his_2022(id_in_sql)
    return error_order_ids


def check_order_status(imc_date_start, imc_date_end):
    page = 1
    imc_order_num = 0
    wms_order_num = 0
    abnormal_order_ids = []
    while True:
        imc_order_ids = db.query_imc_order_page(imc_date_start, imc_date_end, page)
        page = page + 1
        if len(imc_order_ids) == 0:
            return imc_order_num, wms_order_num, abnormal_order_ids
        # 计数
        imc_order_num += len(imc_order_ids)
        id_in_sql = ''
        for imc_id in imc_order_ids:
            id_in_sql = id_in_sql + "'" + imc_id[0] + "',"

        id_in_sql = '(' + id_in_sql[:-1] + ')'

        error_order_ids = get_wms_error_order_id(id_in_sql)
        # 计数
        wms_order_num += len(error_order_ids)
        if len(error_order_ids) == 0:
            continue
        for error_id in error_order_ids:
            abnormal_order_ids.append(error_id[0])


if __name__ == '__main__':
    end_time = pd.Timestamp('2023-01-17')
    while end_time > pd.Timestamp('2022-09-15'):
        start_time = end_time + datetime.timedelta(-1)
        imc_order_num, wms_order_num, abnormal_order_ids = check_order_status(start_time, end_time)
        print(start_time.strftime("%Y-%m-%d") + "<->" + end_time.strftime("%Y-%m-%d") + " " + str(
            imc_order_num) + " " + str(wms_order_num))
        if len(abnormal_order_ids) > 0:
            print(abnormal_order_ids)
        end_time = start_time

    # print(src_day)

    # time.strftime("%Y%m%d%H%M%S", time.localtime())
    # check_order_status("2023-01-01", "2023-01-02")
