# copy 测试环境数据

from pymysql_comm import UsingDev as dev
from pymysql_comm import UsingOnline as test
from db_connect_pool import DEV_POOL
from toollib.snowflake import snow
import copy


def insert_sku(sqls):
    with DEV_POOL.connection() as conn:
        if isinstance(sqls, list):
            for sql in sqls:
                conn.cursor().execute(sql)
        conn.cursor().close()
        conn.commit()


def get_work_shop():
    sql = "SELECT * FROM oms_product.`workshop`"
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库
def get_product_sku(page_num, page_size):
    page_from = (page_num - 1) * page_size
    # sql = "SELECT * FROM oms_product.`product_sku` where create_time >='2024-07-15'  limit %d,%d" % (
    #     page_from, page_size)
    # sql = "SELECT * FROM oms_product.`product_sku` where goods_type = 2  limit %d,%d" % (
    #     page_from, page_size)

    sql = "SELECT * FROM oms_product.`product_sku` where goods_code = 'JBS-PBTB-GF2S1-KJP-7JGY5P'  limit %d,%d" % (
        page_from, page_size)

    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_produce_process(page_num, page_size):
    page_from = (page_num - 1) * page_size
    sql = "SELECT * FROM oms_product.`produce_process` where create_time >='2024-07-15'  limit %d,%d" % (
        page_from, page_size)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_factory_material(page_num, page_size):
    page_from = (page_num - 1) * page_size
    sql = "SELECT * FROM oms_product.`factory_material` where create_time >='2024-07-15'  limit %d,%d" % (
        page_from, page_size)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_bom(page_num, page_size):
    page_from = (page_num - 1) * page_size
    sql = "SELECT * FROM oms_product.`bom` where create_time >='2024-07-15'  limit %d,%d" % (
        page_from, page_size)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_bom_detail(page_num, page_size):
    page_from = (page_num - 1) * page_size
    sql = "SELECT * FROM oms_product.`bom_detail` where create_time >='2024-07-15'  limit %d,%d" % (
        page_from, page_size)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


ignore_fields = ['id', 'create_time', 'update_time']
warehouse_codes = ['WH0351', 'WH0476', 'WH001', 'WH0003', 'WH0004']
supplier_codes = ['OW0064', 'OW0066', 'OW0069', 'OW003']
factory_codes = ['GC0012', 'GC0110']
WP_SQL = '''insert ignore into oms_product.`warehouse_product` (`warehouse_code`,`goods_code`) VALUE ('{warehouse_code}', '{goods_code}');'''
SP_SQL = '''insert ignore into oms_product.`sku_supplier` (`supplier_code`,`goods_code`) VALUE ('{supplier_code}', '{goods_code}');'''

def copy_work_shop():
    work_shop_sql = []
    work_shops = get_work_shop()
    for work in work_shops:
        if work['bind_factory'] == 'GC0114' or work['bind_factory'] == 'GC0115':
           work['bind_factory'] = 'GC0012'
        else:
           work['bind_factory'] = 'GC0110'
        ls = [(k, v) for k, v in work.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into oms_product.`workshop` (" + keys + ") values (" + values + ");"
        work_shop_sql.append(sql)
    insert_sku(work_shop_sql)


def copy_produce_process():
    page_num = 1
    for index in range(1, 5000):
        produce_process = get_produce_process(page_num, 100)
        if len(produce_process) == 0:
            break
        produce_process_sql = []
        for process in produce_process:
            if process['bind_factory'] == 'GC0114' or process['bind_factory'] == 'GC0115':
                process['bind_factory'] = 'GC0012'
            else:
                process['bind_factory'] = 'GC0110'
            ls = [(k, v) for k, v in process.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.`produce_process` (" + keys + ") values (" + values + ");"
            produce_process_sql.append(sql)
        insert_sku(produce_process_sql)
        print("copy_product produce_process page_num=%d" % page_num)
        page_num += 1
    return

def copy_product():
    page_num = 1
    for index in range(1, 5000):
        skus = get_product_sku(page_num, 100)
        if len(skus) == 0:
            break
        sku_insert_sql = []
        goods_codes = []
        for sku in skus:
            goods_codes.append(sku['goods_code'])
            ls = [(k, v) for k, v in sku.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.`product_sku` (" + keys + ") values (" + values + ");"
            sku_insert_sql.append(sql)
        insert_sku(sku_insert_sql)

        warehouse_product_insert_sql = []
        supplier_product_insert_sql = []
        for goods_code in goods_codes:
            for warehouse_code in warehouse_codes:
                warehouse_product_insert_sql.append(WP_SQL.format(warehouse_code=warehouse_code, goods_code=goods_code))
            for supplier_code in supplier_codes:
                supplier_product_insert_sql.append(SP_SQL.format(supplier_code=supplier_code, goods_code=goods_code))
        insert_sku(warehouse_product_insert_sql)
        insert_sku(supplier_product_insert_sql)
        print("copy_product process page_num=%d" % page_num)
        page_num += 1
    return


# def copy_factory_material():
#     page_num = 1
#     for index in range(1, 5000):
#         factory_materials = get_factory_material(page_num, 500)
#         if len(factory_materials) == 0:
#             break
#         factory_material_sql = []
#         for material in factory_materials:
#             for factory_code in factory_codes:
#                 copy_material = copy.deepcopy(material)
#                 copy_material['factory_code'] = factory_code
#                 if factory_code == 'GC0012':
#                     copy_material['warehouse_code'] = 'WH0351'
#                     copy_material['warehouse_area_code'] = 'GCKQ1'
#                 else:
#                     copy_material['warehouse_code'] = 'WH0476'
#                     copy_material['warehouse_area_code'] = 'KQ-ZP'
#                 ls = [(k, v) for k, v in copy_material.items() if (v is not None and k not in ignore_fields)]
#                 keys = ','.join([i[0] for i in ls])
#                 values = ','.join(repr(str(i[1])) for i in ls)
#                 sql = "insert ignore into oms_product.factory_material(" + keys + ") values (" + values + ");"
#                 factory_material_sql.append(sql)
#
#         insert_sku(factory_material_sql)
#         print("copy_factory_material process page_num=%d" % page_num)
#         page_num += 1
#     return
def copy_factory_material():
    page_num = 1
    for index in range(1, 5000):
        factory_materials = get_factory_material(page_num, 500)
        if len(factory_materials) == 0:
            break
        factory_material_sql = []
        for material in factory_materials:
            copy_material = copy.deepcopy(material)
            if copy_material['factory_code'] == 'GC0114' or copy_material['factory_code'] == 'GC0115':
                copy_material['factory_code'] = 'GC0012'
                copy_material['warehouse_code'] = 'WH0351'
                copy_material['warehouse_area_code'] = 'GCKQ1'
            else:
                copy_material['factory_code'] = 'GC0110'
                copy_material['warehouse_code'] = 'WH0476'
                copy_material['warehouse_area_code'] = 'KQ-ZP'
            ls = [(k, v) for k, v in copy_material.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.factory_material(" + keys + ") values (" + values + ");"
            factory_material_sql.append(sql)

        insert_sku(factory_material_sql)
        print("copy_factory_material process page_num=%d" % page_num)
        page_num += 1
    return

def copy_bom():
    page_num = 1
    for index in range(1, 5000):
        boms = get_bom(page_num, 500)
        if len(boms) == 0:
            break
        bom_sql = []
        for bom in boms:
            copy_bom = copy.deepcopy(bom)
            if copy_bom['factory_code'] == 'GC0114' or copy_bom['factory_code'] == 'GC0115':
                copy_bom['bom_code'] = str(copy_bom['bom_code']).replace(str(copy_bom['factory_code']), 'GC0012')
                copy_bom['factory_code'] = 'GC0012'
            else:
                copy_bom['bom_code'] = str(copy_bom['bom_code']).replace(str(copy_bom['factory_code']), 'GC0110')
                copy_bom['factory_code'] = 'GC0110'
            ls = [(k, v) for k, v in copy_bom.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.bom(" + keys + ") values (" + values + ");"
            bom_sql.append(sql)

        insert_sku(bom_sql)
        print("copy_bom process page_num=%d" % page_num)
        page_num += 1

# def copy_bom():
#     page_num = 1
#     for index in range(1, 5000):
#         boms = get_bom(page_num, 500)
#         if len(boms) == 0:
#             break
#         bom_sql = []
#         for bom in boms:
#             for factory_code in factory_codes:
#                 copy_bom = copy.deepcopy(bom)
#                 copy_bom['bom_code'] = str(copy_bom['bom_code']).replace(str(copy_bom['factory_code']), factory_code)
#                 copy_bom['factory_code'] = factory_code
#                 ls = [(k, v) for k, v in copy_bom.items() if (v is not None and k not in ignore_fields)]
#                 keys = ','.join([i[0] for i in ls])
#                 values = ','.join(repr(str(i[1])) for i in ls)
#                 sql = "insert ignore into oms_product.bom(" + keys + ") values (" + values + ");"
#                 bom_sql.append(sql)
#
#         insert_sku(bom_sql)
#         print("copy_bom process page_num=%d" % page_num)
#         page_num += 1

# def copy_bom_detail():
#     page_num = 1
#     detail_id_mapping = {}
#     for index in range(1, 5000):
#         boms = get_bom_detail(page_num, 500)
#         if len(boms) == 0:
#             break
#         bom_sql = []
#         for bom_detail in boms:
#             for factory_code in factory_codes:
#                 copy_bom_detail = copy.deepcopy(bom_detail)
#                 copy_bom_detail['bom_code'] = str(copy_bom_detail['bom_code']).replace(str(copy_bom_detail['factory_code']),  factory_code)
#                 copy_bom_detail['factory_code'] = factory_code
#                 # 生成新的detail_id
#                 new_detail_id = snow.guid()
#                 # 放到mapping 中
#                 detail_id_mapping[copy_bom_detail['bom_detail_id']] = new_detail_id
#                 #  赋值新的detail_id
#                 copy_bom_detail['bom_detail_id'] = new_detail_id
#                 #  提取当前的 parent_id
#                 old_parent_id = copy_bom_detail['parent_bom_detail_id']
#                 #  判断当前的parent_id 是否油映射新值
#                 if old_parent_id != '' and detail_id_mapping[old_parent_id] is not None:
#                     copy_bom_detail['parent_bom_detail_id'] = detail_id_mapping[old_parent_id]
#                 if factory_code == 'GC0012':
#                     copy_bom_detail['warehouse_code'] = 'WH0351'
#                     copy_bom_detail['warehouse_area_code'] = 'GCKQ1'
#                 else:
#                     copy_bom_detail['warehouse_code'] = 'WH0476'
#                     copy_bom_detail['warehouse_area_code'] = 'KQ-ZP'
#
#                 ls = [(k, v) for k, v in copy_bom_detail.items() if (v is not None and k not in ignore_fields)]
#                 keys = ','.join([i[0] for i in ls])
#                 values = ','.join(repr(str(i[1])) for i in ls)
#                 sql = "insert ignore into oms_product.bom_detail(" + keys + ") values (" + values + ");"
#                 bom_sql.append(sql)
#
#         insert_sku(bom_sql)
#         print("copy_bom_detail process page_num=%d" % page_num)
#         page_num += 1

def copy_bom_detail():
    page_num = 1
    detail_id_mapping = {}
    for index in range(1, 5000):
        boms = get_bom_detail(page_num, 500)
        if len(boms) == 0:
            break
        bom_sql = []
        for bom_detail in boms:
            copy_bom_detail = copy.deepcopy(bom_detail)
            if copy_bom_detail['factory_code'] == 'GC0114' or copy_bom_detail['factory_code'] == 'GC0115':
                copy_bom_detail['bom_code'] = str(copy_bom_detail['bom_code']).replace(str(copy_bom_detail['factory_code']), 'GC0012')
                copy_bom_detail['factory_code'] = 'GC0012'
                copy_bom_detail['warehouse_code'] = 'WH0351'
                copy_bom_detail['warehouse_area_code'] = 'GCKQ1'
            else:
                copy_bom_detail['bom_code'] = str(copy_bom_detail['bom_code']).replace(str(copy_bom_detail['factory_code']), 'GC0110')
                copy_bom_detail['factory_code'] = 'GC0110'
                copy_bom_detail['warehouse_code'] = 'WH0476'
                copy_bom_detail['warehouse_area_code'] = 'KQ-ZP'
            # 生成新的detail_id
            new_detail_id = snow.guid()
            # 放到mapping 中
            detail_id_mapping[copy_bom_detail['bom_detail_id']] = new_detail_id
            #  赋值新的detail_id
            copy_bom_detail['bom_detail_id'] = new_detail_id
            #  提取当前的 parent_id
            old_parent_id = copy_bom_detail['parent_bom_detail_id']
            #  判断当前的parent_id 是否油映射新值
            if old_parent_id != '' and detail_id_mapping[old_parent_id] is not None:
                copy_bom_detail['parent_bom_detail_id'] = detail_id_mapping[old_parent_id]
            ls = [(k, v) for k, v in copy_bom_detail.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.bom_detail(" + keys + ") values (" + values + ");"
            bom_sql.append(sql)

        insert_sku(bom_sql)
        print("copy_bom_detail process page_num=%d" % page_num)
        page_num += 1


if __name__ == '__main__':
    # copy_work_shop()
    # copy_produce_process()
    copy_product()
    # copy_factory_material()
    # copy_bom()
    # copy_bom_detail()
