# copy 测试环境数据
import copy
import json

from toollib.guid import SnowFlake

from db_connect_pool import DEV_POOL
from py.ju.jbs.mes.order_plan import mq
from pymysql_comm import UsingOnlineOMS as test

snow = SnowFlake(worker_id=1, datacenter_id=1)


def insert_execute(sqls):
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
def get_product_sku(page_num, page_size, cp_goods_codes):
    page_from = (page_num - 1) * page_size
    # sql = "SELECT * FROM oms_product.`product_sku` where create_time >='2024-07-15'  limit %d,%d" % (
    #     page_from, page_size)
    # sql = "SELECT * FROM oms_product.`product_sku` where goods_type = 2  limit %d,%d" % (
    #     page_from, page_size)

    if cp_goods_codes is None or len(cp_goods_codes) == 0:
        sql = "SELECT * FROM oms_product.`product_sku` where goods_code = 'JBS-PBTB-GF2S1-KJP-7JGY5P'  limit %d,%d" % (
            page_from, page_size)
    else:
        in_sql = ",".join(repr(str(code)) for code in cp_goods_codes)
        sql = "SELECT * FROM oms_product.`product_sku` where goods_code in (%s)  limit %d,%d" % (
            in_sql, page_from, page_size)
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


def get_moulds_with_code(mould_codes):
    in_sql = ','.join(repr(str(code)) for code in mould_codes)
    sql = "SELECT * FROM mes_pms.`mould` where mould_code in (%s)" % in_sql
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_mould_material(mould_codes):
    in_sql = ','.join(repr(str(code)) for code in mould_codes)
    sql = "SELECT * FROM mes_pms.`mould_material` where mould_code in (%s)" % in_sql
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_mould_location():
    sql = "SELECT * FROM mes_pms.`mould_location`"
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_mould_equipment(mould_codes):
    in_sql = ','.join(repr(str(code)) for code in mould_codes)
    sql = "SELECT * FROM mes_pms.`mould_equipment`  where mould_code in (%s)" % in_sql
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_equipment(equipment_codes):
    in_sql = ','.join(repr(str(code)) for code in equipment_codes)
    sql = "SELECT * FROM mes_pms.`equipment`  where equipment_code in (%s)" % in_sql
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_factory_material(page_num, page_size, codes):
    page_from = (page_num - 1) * page_size
    if codes is None or len(codes) == 0:

        sql = "SELECT * FROM oms_product.`factory_material` where create_time >='2024-07-15'  limit %d,%d" % (
            page_from, page_size)
    else:
        in_sql = ','.join(repr(str(code)) for code in codes)
        sql = "SELECT * FROM oms_product.`factory_material` where material_code in (%s) and create_time >='2024-07-15'  limit %d,%d" % (
            in_sql, page_from, page_size)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_bom(page_num, page_size, bom_codes):
    page_from = (page_num - 1) * page_size
    if bom_codes is None or len(bom_codes) == 0:
        sql = "SELECT * FROM oms_product.`bom` where create_time >='2024-07-15'  limit %d,%d" % (
            page_from, page_size)
    else:
        in_sql = ','.join(repr(str(code)) for code in bom_codes)
        sql = "SELECT * FROM oms_product.`bom` where bom_code in (%s) and create_time >='2024-07-15'  limit %d,%d" % (
            in_sql, page_from, page_size)
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


def get_bom_detail(page_num, page_size, bom_codes):
    in_sql = ','.join(repr(str(code)) for code in bom_codes)
    page_from = (page_num - 1) * page_size
    sql = "SELECT * FROM oms_product.`bom_detail` where bom_code in (%s) and create_time >='2024-07-15'  limit %d,%d" % (
        in_sql, page_from, page_size)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_bom_warehouse(bom_codes):
    in_sql = ','.join(repr(str(code)) for code in bom_codes)
    sql = "SELECT * FROM oms_product.`bom_with_warehouse` where bom_code in (%s)" % (in_sql)
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_unit():
    sql = "SELECT * FROM oms_product.`unit`"
    with test() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


ignore_fields = ['id', 'create_time', 'update_time']
warehouse_codes = ['WH0351', 'WH0476', 'WH001', 'WH0003', 'WH0004', 'WH0501', 'WH0503']
supplier_codes = ['OW0064', 'OW0066', 'OW0069', 'OW003', 'OW0073', 'OW0071']
factory_codes = ['GC0012', 'GC0110', 'GC0017', 'GC0015']
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
    insert_execute(work_shop_sql)


def copy_produce_process():
    page_num = 1
    for index in range(1, 5000):
        produce_process = get_produce_process(page_num, 100)
        if len(produce_process) == 0:
            break
        produce_process_sql = []
        for process in produce_process:
            if process['bind_factory'] == 'GC0114' or process['bind_factory'] == 'GC0115':
                process['bind_factory'] = 'GC0015'
            else:
                process['bind_factory'] = 'GC0017'
            process['create_time'] = None
            process['update_time'] = None
            ls = [(k, v) for k, v in process.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.`produce_process` (" + keys + ") values (" + values + ");"
            produce_process_sql.append(sql)
        insert_execute(produce_process_sql)
        print("copy_product produce_process page_num=%d" % page_num)
        page_num += 1
    return


def copy_product(copy_goods_codes):
    page_num = 1
    for index in range(1, 5000):
        skus = get_product_sku(page_num, 100, copy_goods_codes)
        if len(skus) == 0:
            break
        sku_insert_sql = []
        goods_codes = []
        for sku in skus:
            sku['sku_id'] = snow.gen_uid()
            goods_codes.append(sku['goods_code'])
            ls = [(k, v) for k, v in sku.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.`product_sku` (" + keys + ") values (" + values + ");"
            sku_insert_sql.append(sql)
        insert_execute(sku_insert_sql)

        warehouse_product_insert_sql = []
        supplier_product_insert_sql = []
        for goods_code in goods_codes:
            for warehouse_code in warehouse_codes:
                warehouse_product_insert_sql.append(WP_SQL.format(warehouse_code=warehouse_code, goods_code=goods_code))
            for supplier_code in supplier_codes:
                supplier_product_insert_sql.append(SP_SQL.format(supplier_code=supplier_code, goods_code=goods_code))
        insert_execute(warehouse_product_insert_sql)
        insert_execute(supplier_product_insert_sql)
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
def copy_factory_material(codes):
    page_num = 1
    for index in range(1, 5000):
        factory_materials = get_factory_material(page_num, 500, codes)
        if len(factory_materials) == 0:
            break
        factory_material_sql = []
        for material in factory_materials:
            copy_material = copy.deepcopy(material)
            if copy_material['factory_code'] == 'GC0114' or copy_material['factory_code'] == 'GC0115':
                copy_material['factory_code'] = 'GC0015'
                copy_material['warehouse_code'] = 'WH0501'
                copy_material['warehouse_area_code'] = 'JS-S02'
            else:
                copy_material['factory_code'] = 'GC0017'
                copy_material['warehouse_code'] = 'WH0503'
                copy_material['warehouse_area_code'] = 'WJF-01'
            copy_material['create_time'] = None
            copy_material['update_time'] = None
            ls = [(k, v) for k, v in copy_material.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.factory_material(" + keys + ") values (" + values + ");"
            factory_material_sql.append(sql)

        insert_execute(factory_material_sql)
        print("copy_factory_material process page_num=%d" % page_num)
        page_num += 1
    return


def copy_mould_location():
    mould_locations = get_mould_location()
    mould_location_insert = []
    for mould_location in mould_locations:
        mould_location['factory_code'] = 'GC0015'
        ls = [(k, v) for k, v in mould_location.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into mes_pms.`mould_location` (" + keys + ") values (" + values + ");"
        mould_location_insert.append(sql)
    insert_execute(mould_location_insert)


# 复制模具
def copy_mould_code(codes):
    moulds = get_moulds_with_code(codes)
    if len(moulds) == 0:
        return
    mould_insert = []
    for mould in moulds:
        mould['manage_unit_code'] = 'GC0015'
        ls = [(k, v) for k, v in mould.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into mes_pms.`mould` (" + keys + ") values (" + values + ");"
        mould_insert.append(sql)

    mould_materials = get_mould_material(codes)
    mould_material_insert = []
    for mould_material in mould_materials:
        ls = [(k, v) for k, v in mould_material.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into mes_pms.`mould_material` (" + keys + ") values (" + values + ");"
        mould_material_insert.append(sql)

    mould_equipments = get_mould_equipment(codes)
    mould_equipment_insert = []
    equipment_codes = []
    for mould_equipment in mould_equipments:
        ls = [(k, v) for k, v in mould_equipment.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into mes_pms.`mould_equipment` (" + keys + ") values (" + values + ");"
        mould_equipment_insert.append(sql)
        equipment_codes.append(mould_equipment['equipment_code'])

    equipments = get_equipment(equipment_codes)
    equipment_insert = []
    for equipment in equipments:
        if equipment['supplier_code'] == 'G100721':
            equipment['supplier_code'] = 'G100127'
        if equipment['supplier_code'] == 'G100719':
            equipment['supplier_code'] = 'G100126'
        if equipment['supplier_code'] == 'G100720':
            equipment['supplier_code'] = 'G100128'
        equipment['factory_code'] = 'GC0015'
        ls = [(k, v) for k, v in equipment.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into mes_pms.`equipment` (" + keys + ") values (" + values + ");"
        equipment_insert.append(sql)

    insert_execute(mould_insert)
    insert_execute(mould_material_insert)
    insert_execute(mould_equipment_insert)
    insert_execute(equipment_insert)

    print("copy_product mould finish")
    return


def copy_bom_warehouse(bom_codes):
    # boms_warehouse = get_bom_warehouse(bom_codes)
    sql = '''INSERT INTO `oms_product`.`bom_with_warehouse` ( `bom_code`, `receive_warehouse_code`) VALUES ( '{bom_code}', 'WH_EMPTY');;
'''
    insert_sqls = []
    for code in bom_codes:
        sql = sql.format(bom_code=code)
        insert_sqls.append(sql)
    insert_execute(insert_sqls)


def copy_bom_fun(bom_codes, page_size):
    page_num = 1
    for index in range(1, 5000):
        boms = get_bom(page_num, page_size, bom_codes)
        if len(boms) == 0:
            break
        bom_sql = []
        new_bom_codes = []
        current_bom_codes = []
        material_codes = []
        for bom in boms:
            copy_bom = copy.deepcopy(bom)
            if copy_bom['factory_code'] == 'GC0114' or copy_bom['factory_code'] == 'GC0115':
                copy_bom['bom_code'] = str(copy_bom['bom_code']).replace(str(copy_bom['factory_code']), 'GC0015')
                copy_bom['factory_code'] = 'GC0015'
            else:
                copy_bom['bom_code'] = str(copy_bom['bom_code']).replace(str(copy_bom['factory_code']), 'GC0017')
                copy_bom['factory_code'] = 'GC0017'
            ls = [(k, v) for k, v in copy_bom.items() if (v is not None and k not in ignore_fields)]
            keys = ','.join([i[0] for i in ls])
            values = ','.join(repr(str(i[1])) for i in ls)
            sql = "insert ignore into oms_product.bom(" + keys + ") values (" + values + ");"
            bom_sql.append(sql)
            current_bom_codes.append(bom['bom_code'])
            new_bom_codes.append(copy_bom['bom_code'])
            material_codes.append(bom['material_code'])
        try:

            details, detail_material_codes, cite_bom_codes = copy_bom_detail(list(set(current_bom_codes)))

            insert_execute(details)
            insert_execute(bom_sql)

            # 复制BOM -仓库
            copy_bom_warehouse(list(set(new_bom_codes)))

            ## 复制工厂物料
            material_codes.extend(detail_material_codes)
            copy_factory_material(list(set(material_codes)))

            # 复制引用BOM
            if cite_bom_codes is not None and len(cite_bom_codes) > 0:
                copy_bom_fun(list(set(cite_bom_codes)), 1000)

        except Exception as e:
            # 捕获所有异常，确保子进程能退出
            print(f"读取失败：{str(e)}")
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

def copy_bom_detail(bom_codes):
    page_num = 1
    detail_id_mapping = {}
    bom_sql = []
    material_codes = []
    cite_bom_codes = []
    for index in range(1, 5000):
        boms = get_bom_detail(page_num, 500, bom_codes)
        if len(boms) == 0:
            break

        for bom_detail in boms:
            copy_bom_detail = copy.deepcopy(bom_detail)
            if copy_bom_detail['factory_code'] == 'GC0114' or copy_bom_detail['factory_code'] == 'GC0115':
                copy_bom_detail['bom_code'] = str(copy_bom_detail['bom_code']).replace(
                    str(copy_bom_detail['factory_code']), 'GC0015')
                copy_bom_detail['factory_code'] = 'GC0015'
                copy_bom_detail['warehouse_code'] = 'WH0501'
                copy_bom_detail['warehouse_area_code'] = 'JS-S02'

                if bom_detail['cite_bom_code'] is not None and bom_detail['cite_bom_code'] != '':
                    copy_bom_detail['cite_bom_code'] = str(bom_detail['cite_bom_code']).replace(
                        str(bom_detail['factory_code']), 'GC0015')
                copy_bom_detail['create_time'] = None
                copy_bom_detail['update_time'] = None
            else:
                copy_bom_detail['bom_code'] = str(bom_detail['bom_code']).replace(
                    str(bom_detail['factory_code']), 'GC0017')
                copy_bom_detail['factory_code'] = 'GC0017'
                copy_bom_detail['warehouse_code'] = 'WH0503'
                copy_bom_detail['warehouse_area_code'] = 'WJF-01'

                if bom_detail['cite_bom_code'] is not None and bom_detail['cite_bom_code'] != '':
                    copy_bom_detail['cite_bom_code'] = str(bom_detail['cite_bom_code']).replace(
                        str(bom_detail['factory_code']), 'GC0017')

                copy_bom_detail['create_time'] = None
                copy_bom_detail['update_time'] = None

            if bom_detail['cite_bom_code'] is not None and bom_detail['cite_bom_code'] != '':
                cite_bom_codes.append(bom_detail['cite_bom_code'])

            material_codes.append(copy_bom_detail['material_code'])
            # 生成新的detail_id
            new_detail_id = snow.gen_uid()
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
        print("copy_bom_detail process page_num=%d" % page_num)
        page_num += 1
    return bom_sql, material_codes, cite_bom_codes


def send_equipment_msg(equipment_codes):
    for equipment_code in equipment_codes:
        msg_map = {"msgId": snow.gen_uid(), "equipmentCode": equipment_code}
        mq.get_rabbitmq().producter(exchange='mes-pms_equipment_modify_notify_exchange',
                                    queue='',
                                    routing_key='',
                                    message=json.dumps(msg_map, ensure_ascii=False))

def send_mould_msg(mould_codes):
    for mould_code in mould_codes:
        msg_map = {"msgId": snow.gen_uid(), "mouldCode": mould_code}
        mq.get_rabbitmq().producter(exchange='mes-pms_mould_modify_notify_exchange',
                                    queue='',
                                    routing_key='',
                                    message=json.dumps(msg_map, ensure_ascii=False))

def copy_uits():
    units = get_unit()
    unit_sqls = []
    for unit in units:
        ls = [(k, v) for k, v in unit.items() if (v is not None and k not in ignore_fields)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into oms_product.`unit` (" + keys + ") values (" + values + ");"
        unit_sqls.append(sql)
    insert_execute(unit_sqls)


if __name__ == '__main__':
    # copy_work_shop()
    # copy_produce_process()
    # copy_product(['2000-B00215', '2000-C00090', '2000-B00280', '2000-C00089', '2000-C00054',
    #              '2000-C00053', '2000-C00052', '2000-C00051', '2000-C00050', '2000-C00049', '2000-C00048',
    #              '2000-B00279', ])

    # copy_factory_material()
    # copy_bom_fun(['GC0114-1000-D00382-V1.0'], 1)
    # copy_mould_location()
    # copy_mould_code(['WRJ-YL-002',
    #                  'WRJ-YL-001',
    #                  'WRJ-YL-005',
    #                  'WRJ-YL-004',
    #                  'WRJ-YL-008',
    #                  'WRJ-YL-007',
    #                  'WRJ-YL-003',
    #                  'WRJ-YL-006', ])

    #send_equipment_msg([])
    # send_mould_msg(['WRJ-YL-001',
    #                     'WRJ-YL-002',
    #                     'WRJ-YL-003',
    #                     'WRJ-YL-004',
    #                     'WRJ-YL-005',
    #                     'WRJ-YL-006',
    #                     'WRJ-YL-007',
    #                     'WRJ-YL-008', ])

    copy_uits()
