import threading

from pymysql_comm import UsingOnlineOMS as online

import multiprocessing
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED


def get_duplicate_bom_detail():
    sql = "SELECT parent_bom_detail_id,material_code  FROM `oms_product`.`bom_detail` where parent_bom_detail_id !=''  GROUP BY parent_bom_detail_id,material_code HAVING count(1) > 1"
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_bom_detail(parent_id, material_code):
    sql = (
        "SELECT * FROM `oms_product`.`bom_detail` where parent_bom_detail_id='{parent_id}' AND material_code='{material_code}' order by create_time asc"
        .format(parent_id=parent_id, material_code=material_code))
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def choice_del_ids(duplicate_details, count):
    file = open("D:\\项目相关\\MES2.0\\{file_name}.sql".format(file_name="物料清单重复处理" + str(count)), "w",
                encoding='utf-8')
    del_ids = []
    count = 0
    for detail in duplicate_details:
        bom_details = get_bom_detail(detail['parent_bom_detail_id'], detail['material_code'])
        if len(bom_details) <= 1:
            continue;
        id_ = bom_details[0]['bom_detail_id']
        del_sql = "delete from `oms_product`.`bom_detail` where bom_detail_id ='{id}';".format(id=id_)
        file.write(del_sql + '\n')
        del_ids.append(id_)
        print("{thead} 第 {count}".format(thead=multiprocessing.current_process().name, count=count))
        count += 1


def split_list(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]


if __name__ == '__main__':

    duplicate_details = get_duplicate_bom_detail()
    lists_ = split_list(duplicate_details, 1000)
    count = 0
    for details in lists_:
        multiprocessing.Process(target=choice_del_ids, args=(details, count,), name='thread-' + str(count)).start()
        count += 1
