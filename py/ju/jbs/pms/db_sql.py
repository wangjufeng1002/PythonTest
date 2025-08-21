from pandas.core.window import online

from pymysql_comm import UsingOnlineOMS as oms_online
from pymysql_comm import UsingOnlineOMS as oms_dev


def sql_exe(online: bool = True, sql: str = ""):
    with oms_online() if online else oms_dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_unit(online: bool = True, ):
    sql = "SELECT * FROM oms_product.`unit`"
    return sql_exe(online, sql)


def get_supplier(online: bool = True, ):
    sql = "SELECT * FROM srm_supply.`supplier`"
    return sql_exe(online, sql)


def get_factory(online: bool = True, ):
    sql = "SELECT * FROM oms_product.`produce_factory`"
    return sql_exe(online, sql)


def get_material(online: bool = True, material_code: str = None, ):
    sql = "SELECT * FROM oms_product.`product_sku` where goods_code = \'{material_code}\'".format(
        material_code=material_code)
    return sql_exe(online, sql)


def get_materials(online: bool = True, material_code: list = None):
    in_sql = ','.join(repr(str(code)) for code in material_code)
    sql = "SELECT * FROM oms_product.`product_sku` where goods_code in ({in_sql})".format(in_sql=in_sql)
    return sql_exe(online, sql)


def get_equipment(online: bool = True, equipment_code: str = None):
    sql = "SELECT * FROM mes_pms.`equipment` where equipment_code = \'{equipment_code}\'".format(
        equipment_code=equipment_code)
    return sql_exe(online, sql)


def get_equipments(online: bool = True, equipment_codes: list = None):
    in_sql = ','.join(repr(str(code)) for code in equipment_codes)
    sql = "SELECT * FROM mes_pms.`equipment` where equipment_code in ({in_sql})".format(in_sql=in_sql)
    return sql_exe(online, sql)


def get_mould_equipment(online: bool = True, equipment_code: str = None, mould_code: str = None):
    sql = "SELECT * FROM mes_pms.`mould_equipment` where equipment_code = \'{equipment_code}\' and mould_code  = \'{mould_code}\'".format(
        equipment_code=equipment_code, mould_code=mould_code)
    return sql_exe(online, sql)


def get_mould(online: bool = True, mould_code: str = None):
    sql = "SELECT * FROM mes_pms.`mould` where mould_code  = \'{mould_code}\'".format(mould_code=mould_code)
    return sql_exe(online, sql)


def get_moulds(online: bool = True, mould_codes: list = None):
    in_sql = ','.join(repr(str(code)) for code in mould_codes)
    sql = "SELECT * FROM mes_pms.`mould` where mould_code  in ({in_sql})".format(in_sql=in_sql)
    return sql_exe(online, sql)


def get_equipment_produce_parameter():
    sql_temp = "SELECT * FROM mes_pms.`equipment_produce_parameter` limit {offset},{limit}"

    limit = 10000
    page_num = 1
    results = []
    while True:
        sql = sql_temp.format(offset=(page_num - 1) * limit, limit=limit)
        result = sql_exe(True, sql)
        if len(result) == 0:
            return results
        results.extend(result)
        page_num += 1


def get_mould_equipment_bind(moulds_codes: list = None):
    in_sql = ','.join(repr(str(code)) for code in moulds_codes)
    sql_temp = "SELECT * FROM mes_pms.`mould_equipment` where mould_code in ({in_sql})".format(in_sql=in_sql);
    return sql_exe(True, sql_temp)



def get_unit_dict():
    units = get_unit(online=True)
    unit_dict = {}
    for unit in units:
        unit_dict[unit['unit_name']] = unit['unit_code']
    return unit_dict


def get_factory_dict():
    factories = get_factory(online=True)
    factory_dict = {}
    for factory in factories:
        factory_dict[factory['factory_name']] = factory['factory_code']
    return factory_dict


def get_supplier_dict():
    suppliers = get_supplier(online=True)
    supplier_dict = {}
    for supplier in suppliers:
        supplier_dict[supplier['supplier_name']] = supplier['supplier_code']
    return supplier_dict
