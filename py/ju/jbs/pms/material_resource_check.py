from numpy.ma.extras import unique

from py.ju.jbs.utils import db_sql


def out_put_sql(datas: list, file_name: str):
    file = open("D:\\项目相关\\mould-equipment\\0929\\数据检查\\{file_name}.sql".format(file_name=file_name), "w",
                encoding='utf-8')
    for data in datas:
        file.write(data)
        file.write('\n')
    file.flush()
    file.close()
    print(file_name + "写入完成")


def check_mould_equipment():
    db_sql.get_moulds()


factory_map = {
    "GC0114": "生产一部",
    "GC0116": "生产三部",
    "GC0115": "生产二部",
    "GC0117": "生产四部"
}


def get_material_attr_desc(attr: int):
    if attr == 1:
        return "自制"
    elif attr == 2:
        return "外购"
    elif attr == 3:
        return "委外"
    elif attr == 4:
        return "调拨"
    elif attr == 5:
        return "内部生产协作"
    else:
        return ''


def get_material_attr(attrs: list):
    return ','.join(get_material_attr_desc(int(attr)) for attr in attrs)


def check_material_resource(factory_code, material_code):
    factory_material = db_sql.get_factory_material_single(factory_code, material_code)
    if factory_material is None:
        print(f"{material_code}, 未找到工厂物料")
        return

    attr_desc = get_material_attr(factory_material['material_attr'].split(','))
    if attr_desc == '内部生产协作':
        return
    material_moulds = db_sql.get_material_mould(material_code)
    error_datas = []
    if len(material_moulds) == 0:
        print(f"{material_code}, {attr_desc}, 未找到模具信息")
        error_datas.append(f"{material_code},{attr_desc},未找到模具信息")
        return
    mould_codes = []
    for mould in material_moulds:
        get_moulds = db_sql.get_mould(mould['mould_code'])
        if len(get_moulds) == 0:
            # print(f"{mould['mould_code']},未找到模具基础信息")
            continue
        if get_moulds[0]['manage_unit_code'] != factory_code:
            continue
            # error_datas.append(f"{material_code},{mould['mould_code']},管理单位不属于{factory_map[factory_code]}")
            # print(f"{material_code},{mould['mould_code']},管理单位不属于{factory_map[factory_code]}")
        else:
            mould_codes.append(mould['mould_code'])

    if len(mould_codes) == 0:
        print(f"{material_code},{attr_desc},未找到符合生产的模具")
        return

    mould_codes = list(unique(mould_codes))
    for mould_code in mould_codes:
        equipments = db_sql.get_mould_equipment(mould_code)
        if len(equipments) == 0:
            print(f"{material_code},{attr_desc},{mould_code},未找到绑定关系")
            error_datas.append(f"{material_code},{attr_desc},{mould_code},未找到绑定关系")
        for equipment in equipments:
            time = db_sql.get_cycle_time(mould_code, equipment['equipment_code'])
            if time is None:
                print(f"{material_code},{attr_desc},{mould_code},{equipment['equipment_code']} 循环时间为空")
    return error_datas


def check_factory_material_resource(factory_code):
    print(f'{factory_code} ============ 检查开始')
    page_size = 1000
    page_num = 1
    error_datas = []
    while True:
        materials = db_sql.get_factory_material(factory_code=factory_code, page_num=page_num, page_size=page_size)
        if len(materials) == 0:
            break
        for material in materials:
            if '1' in material['material_attr'] or '3' in material['material_attr']:
                error_datas_parts = check_material_resource(factory_code, material['material_code'])
                if len(error_datas_parts) > 0:
                    error_datas.extend(error_datas_parts)
        page_num = page_num + 1

    out_put_sql(error_datas, factory_code)

    print(f'{factory_code} ============ 检查结束')


def check_material_resource_with_codes(factory_code, material_codes):
    print(f' ============ {factory_map[factory_code]} 检查开始 ============ ')
    for material_code in material_codes:
        check_material_resource(factory_code, material_code)
    print(f' ============ {factory_map[factory_code]} 检查结束 ============ ')


if __name__ == '__main__':
    # check_factory_material_resource("GC0114")
    # check_factory_material_resource("GC0115")
    # check_factory_material_resource("GC0116")
    # check_factory_material_resource("GC0117")

    # "GC0114": "生产一部",
    # "GC0116": "生产三部",
    # "GC0115": "生产二部",
    # "GC0117": "生产四部"

    factory_code = "GC0115"
    material_code_str = '2000-B00534,2000-C00176,2000-B00533,2000-C00187,2000-B00434,2000-B00524,2000-C00265,2000-B00530,2000-C00177,2000-J00041,2000-A00052,2000-C00268,2000-C00266,2000-C00267,2000-C00248,2000-C00280,2000-B01289,2000-B00572,2000-C00307,2000-C00308,4000-K00123,2000-C00310,2000-C00309,2000-B00097,2000-J00040,2000-C00271,2000-C00312,2000-J00006,2000-K00005,2000-C00311,2000-C00247,2000-C00249,2000-J00042,2000-C00270,2000-C00262,2000-C00261,2000-C00263,2000-A00051,2000-C00264,2000-C00260,2000-C00259,2000-B00144,2000-B01285,2000-C00250,2000-B00532,2000-C00251,2000-C00269,2000-F00017,2000-C00188,2000-C00189,2000-C00433'
    check_material_resource_with_codes(factory_code, material_code_str.split(','))
