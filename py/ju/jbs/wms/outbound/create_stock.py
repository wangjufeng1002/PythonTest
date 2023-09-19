import db
import hashlib

sql = "INSERT INTO `wms_work`.`stock` ( `goods_code`, `warehouse_code`, `warehouse_area_code`, " \
      "`warehouse_location_code`, `warehouse_location_type`, `wwg_idx`, `stock_num`, `stock_lock_num`," \
      " `max_stock_num`, `stock_warning_num`, `special_mark`, `sku_name`, `create_time`, `update_time`) " \
      "VALUES ( '{goods_code}', '{warehouse_code}', '{warehouse_area_code}', '{warehouse_location_code}','{warehouse_location_type}', " \
      "'{wwg_idx}', 9999999, 0, 10000000, 0, '{special_mark}'," \
      " 'wjf测试', '2022-09-05 11:51:33', '2022-09-05 10:51:25');"
warehouse_codes = ["WH0019", "WH0001", "WH0024", "WH0016", "WH0020", "WH0021", "WH0004", "WH0022", "WH0003", "WH0025"]

temp = ['A', 'B', "C", "D", "E", "D", ]
warehouse_location_code = "01{}01-{}"

# sql_format = sql.format(goods_code='aaa', warehouse_code="WH00001", warehouse_area_code="1",
#                         warehouse_location_code="1111", warehouse_location_type=1, wwg_idx="1", special_mark=1)
goodsCodes = list(map(lambda x: x['goods_code'], db.get_product_codes(1000000)))

warehouse_locations = db.get_warehouse_localtion("WH0001")


def get_ww_idx(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    uuid = m2.hexdigest()
    return uuid


warehouse_code = "WH0001"

# for i in range(0, len(warehouse_locations)):
#     goods_code = goodsCodes[i]
#     warehouse_location = warehouse_locations[i]
#     execute_sql = sql.format(goods_code=goods_code, warehouse_code=warehouse_code, warehouse_area_code='02H',
#                      warehouse_location_code=warehouse_location['warehouse_location_code'],
#                      warehouse_location_type=warehouse_location['warehouse_location_type'],
#                      wwg_idx=get_ww_idx(warehouse_code + warehouse_location['warehouse_location_code'] + goods_code),
#                      special_mark=warehouse_location['warehouse_location_type'])
#     i += 1
#     try:
#         db.insert_stock_data(execute_sql)
#         print("SUCCESS：" + execute_sql)
#     except:
#         print("ERROR:" + execute_sql)


disable_goods_code = ["JBS-GZDD-SSH-S", "BD20-TZSB-01", "BDF-TZSB-05","DF-JBS-CFZWJ-G503-BK", "DF-JBS-SNH-0213-BU", "DF-JBS-SNH-0214-BU",
                      "D866", "D867", "D868", "D869",
                     "JBS-CTH-1867", "JBS-CTH-1868", "JBS-CTH-1872", "JBS-CTH-1873", "JBS-CTH-1874",
                     "JBS-GSSB-R21-BU", "JBS-GSSB-R22-WT",
                     "DF-JBS-TLZWJ-G1-A30-1",
                     "DF-JBS-LYJ-X200-HQG3G", "DF-JBS-LYJ-X200-QG3G",
                     "DF-JBS-TLZWJ-G2-B40-2SY", "DF-JBS-TLZWJ-G2-B40-3BK", "DF-JBS-TLZWJ-G2-B40-3SY",
                     "DF-YC-LYJ-X200-2G", "DF-YC-LYJ-X200-3G", "DF-YC-LYJ-X240-2G", "DF-YC-LYJ-X240-3G",
                     "DF-JBS-XLYL-GD01", "DF-JBS-XLYL-GD02", "DF-JBS-XLYL-GD03", "DF-JBS-XLYL-GD11", "DF-JBS-XLYL-GD12", "DF-PJ-JBS-SCJ-31S1-BK-KZT", "DF-PJ-JBS-SCJ-31S1-BK-LSB"]

for r_goods_code in disable_goods_code:
    goodsCodes.remove(r_goods_code.replace(" ",""))

for i in range(0, len(warehouse_locations)):
    goods_code = goodsCodes[i]
    if goods_code in disable_goods_code:
        continue
    warehouse_location = warehouse_locations[i]
    execute_sql = sql.format(goods_code=goods_code, warehouse_code=warehouse_code, warehouse_area_code=warehouse_location['warehouse_area_code'],
                 warehouse_location_code=warehouse_location['warehouse_location_code'],
                 warehouse_location_type=warehouse_location['warehouse_location_type'],
                 wwg_idx=get_ww_idx(warehouse_code + warehouse_location['warehouse_location_code'] + goods_code),
                 special_mark=warehouse_location['warehouse_location_type'])
    try:
        db.insert_stock_data(execute_sql)
        print("SUCCESS：" + execute_sql)
    except:
        print("ERROR:" + execute_sql)
