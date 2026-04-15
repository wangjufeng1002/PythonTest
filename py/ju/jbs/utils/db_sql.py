import json
from ju.jbs.common.db.pymysql_comm import UsingOnlineOMS as oms_online
from ju.jbs.common.db.pymysql_comm import UsingOnlineWms as wms_online
from ju.jbs.common.db.pymysql_comm import UsingDev as oms_dev


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


def get_material_mould(material_code):
    sql = "SELECT * FROM mes_pms.`mould_material` where material_code = '{material_code}' ".format(
        material_code=material_code)
    return sql_exe(online=True, sql=sql)


def get_cycle_time(mould_code, equipment_code):
    sql = "SELECT `process_param` FROM mes_pms.`equipment_produce_parameter` where mould_code = '{mould_code}' and equipment_code = '{equipment_code}' ".format(
        mould_code=mould_code, equipment_code=equipment_code)
    result = sql_exe(online=True, sql=sql)
    if len(result) == 0:
        return None
    params = json.loads(result[0]['process_param'])
    if 'cycleTime' in params:
        return params['cycleTime']
    return None


def get_mould(mould_code):
    sql = "SELECT * FROM mes_pms.`mould` where mould_code = '{mould_code}' ".format(
        mould_code=mould_code)
    return sql_exe(online=True, sql=sql)


def get_mould_equipment(mould_code):
    sql = "SELECT * FROM mes_pms.`mould_equipment` where mould_code = '{mould_code}' ".format(
        mould_code=mould_code)
    return sql_exe(online=True, sql=sql)


def get_factory_material(factory_code, page_size, page_num):
    offset = (page_num - 1) * page_size
    sql = ("SELECT * from oms_product.`factory_material` where factory_code = '{factory_code}' "
           "and enable = 1 and material_group = '1822839423929765888,1822839423929765892' limit {offset},{limit}").format(
        factory_code=factory_code, limit=page_size, offset=offset
    )
    return sql_exe(online=True, sql=sql)


def get_factory_material_single(factory_code, material_code, online=True):
    sql = (
        "SELECT * from oms_product.`factory_material` where factory_code = '{factory_code}' and material_code = '{material_code}' ").format(
        factory_code=factory_code, material_code=material_code
    )
    results = sql_exe(online, sql=sql)
    if len(results) == 0:
        return None
    return results[0]


def get_auth_equipment(factory_code, online: bool = True ):
    sql = ("select equipment_code,ip,port from mes_pms.equipment where  factory_code = '{factory_code}' and equipment_type = 1 and supplier_code = 'G100719' and auth_status = 20;"
    .format(factory_code=factory_code))
    return sql_exe(online, sql)


def get_ding_users(online: bool = True, job_number: list = None):
    in_sql = ','.join(repr(str(code)) for code in job_number)
    sql = "SELECT * FROM erp_auth.`ding_user` where job_number in ({in_sql})".format(in_sql=in_sql)
    return sql_exe(online, sql)


def get_ding_user(online: bool = True, job_number: str = None):
    in_sql = ','.join(repr(str(code)) for code in job_number)
    sql = "SELECT * FROM erp_auth.`ding_user` where job_number = '{job_number}'".format(job_number=in_sql)
    return sql_exe(online, sql)