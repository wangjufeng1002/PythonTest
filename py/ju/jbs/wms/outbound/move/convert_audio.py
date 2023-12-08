import os
import json
from pymysql_online import UsingMysql as online


def get_warehouse():
    sql = "SELECT warehouse_code,warehouse_name FROM oms_product.`warehouse` where warehouse_use_type = 2 and status = 1"
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


warehouse_map = {}
warehouses = get_warehouse()
for wh in warehouses:
    warehouse_map.setdefault(wh['warehouse_code'],wh['warehouse_name'])


path = "C:\\Users\\PC\\Desktop\\语音文件\\"
listdir = os.listdir(path)

for file in listdir:
    print(file)

if __name__ == '__main__':
    list = []
    dict = {"A":1,"S":2}
    list.append(dict)
    print(json.dumps(list))
