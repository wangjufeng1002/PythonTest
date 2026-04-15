# 设备初始化
import json
from concurrent.futures import ThreadPoolExecutor
import mq
import openpyxl
from toollib.guid import SnowFlake
from py.ju.jbs.utils import db_sql

snow = SnowFlake(worker_id=1, datacenter_id=1)

param_update_sql = '''INSERT INTO `mes_pms`.`equipment_produce_parameter`(`produce_param_id`, `equipment_code`, `connect_status`, `produce_status`, `operate_type`, `mould_code`, `priority`, `process_param`)
  VALUES ('{id}', '{equipment_code}', 0, 0, 0, '{mould_code}',  2147483647, '{param}') on duplicate key update process_param = JSON_SET(process_param, '$.cycleTime', {cycleTime});'''

# 循环时间更新SQL
param_cycle_update_template_sql = '''update `mes_pms`.`equipment_produce_parameter` set process_param = JSON_SET(process_param, '$.cycleTime', {cycleTime}),
    need_machine_side = {need_machine_side} where `produce_param_id`  = '{produce_param_id}';'''

# 循环时间更新SQL
# param_cycle_update_template_sql = '''update `mes_pms`.`equipment_produce_parameter` set need_machine_side = {need_machine_side} where `produce_param_id`  = '{produce_param_id}';'''
# 设备周边更新sql
equipment_side_update_template_sql = '''INSERT ignore INTO `mes_pms`.`equipment_side` (`equipment_side_id`, `equipment_produce_param_id`, `equipment_side_code`) VALUES ('{equipment_side_id}', '{equipment_produce_param_id}', '{equipment_side_code}');'''

param_worker_update_template_sql = '''INSERT INTO `mes_pms`.`equipment_worker` (`equipment_produce_param_id`, `pilot_num`, `injection_num`, `stir_num`, `crush_num`)
 VALUES ('{id}', {pilot_num}, {injection_num}, {stir_num}, {crush_num}) on duplicate key update `pilot_num`={pilot_num},injection_num={injection_num},`stir_num`= {stir_num},`crush_num`={crush_num};'''

mould_equipment_bind_template_sql = '''INSERT ignore INTO  `mes_pms`.`mould_equipment` (`mould_equipment_id`, `mould_code`, `equipment_code`, `priority`) VALUES ('{id}', '{mould_code}', '{equipment_code}', 1);'''


def generate_update_sql(result, sheet_name):
    param_map = get_equipment_param_map()
    cycle_update_sqls = []
    equipment_side_update_sqls = []
    param_worker_update_sqls = []
    for data in result:
        unique_key = str(data['设备编码']) + str(data['模具编号'])
        if unique_key not in param_map:
            print("设备编码：%s 模具编码：%s 设备参数不存在".format(data['设备编码'], data['模具编号']))
            continue

        have_equipment_side = False
        # 设备周边更新
        for i in range(0, 10):
            suffix = '' if i == 0 else str(i)
            code_col_key = '子单-设备编码' + suffix
            name_col_key = '子单-设备名称' + suffix
            if code_col_key in data:
                if data[code_col_key] is not None and data[code_col_key] != '':
                    equipment_side_update_sql = equipment_side_update_template_sql.format(
                        equipment_side_id='ES' + str(snow.gen_uid()),
                        equipment_produce_param_id=param_map[unique_key][
                            'produce_param_id'],
                        equipment_side_code=str(data[code_col_key]))
                    have_equipment_side = True
                    equipment_side_update_sqls.append(equipment_side_update_sql)

        # 循环时间更新SQL
        cycle_update_sql = param_cycle_update_template_sql.format(
            produce_param_id=param_map[unique_key]['produce_param_id'],
            cycleTime=data["循环时间(s)"], need_machine_side=(1 if have_equipment_side else 0))
        # cycle_update_sql = param_cycle_update_template_sql.format(
        #     produce_param_id=param_map[unique_key]['produce_param_id'],
        #     need_machine_side=(1 if have_equipment_side else 0))
        cycle_update_sqls.append(cycle_update_sql)

        # 注塑人工
        param_worker_update_sql = param_worker_update_template_sql.format(id=param_map[unique_key]['produce_param_id'],
                                                                          pilot_num=data['调机师'],
                                                                          injection_num=data['注塑操作师'],
                                                                          stir_num=data['搅拌操作师'],
                                                                          crush_num=data['粉碎操作师'])
        param_worker_update_sqls.append(param_worker_update_sql)

    out_put_sql(cycle_update_sqls, sheet_name + "-设备参数循环时间更新")
    out_put_sql(equipment_side_update_sqls, sheet_name + "-设备周边更新")
    out_put_sql(param_worker_update_sqls, sheet_name + "-设备人工更新")


def out_put_sql(sqls: list, file_name: str):
    file = open("D:\\项目相关\\mould-equipment\\0930\\设备参数\\{file_name}0930.sql".format(file_name=file_name), "w",
                encoding='utf-8')
    for sql in sqls:
        file.write(sql)
        file.write('\n')
    file.flush()
    file.close()
    print(file_name + "写入完成")


def generate_mould_equipment_bind_sql(results, sheet_name):
    sqls = []
    for data in results:
        insert_sql = mould_equipment_bind_template_sql.format(id='EM' + str(snow.gen_uid()),
                                                              mould_code=data['模具编号'],
                                                              equipment_code=data['设备编码'])
        sqls.append(insert_sql)
    out_put_sql(sqls, sheet_name + "-模具设备绑定")


def get_equipment_param_map():
    all_param = db_sql.get_equipment_produce_parameter()
    param_map = {}
    for param in all_param:
        param_map[param['equipment_code'] + param['mould_code']] = param
    return param_map


def find_duplicates(arr):
    count = {}
    duplicates = []
    for item in arr:
        # 统计次数
        count[item] = count.get(item, 0) + 1
        # 若次数首次达到2，加入重复列表（避免重复添加）
        if count[item] == 2:
            duplicates.append(item)
    return duplicates  # 返回所有重复元素（去重后的）


def send_mould_change_msg(online, mould_codes):
    snow = SnowFlake()
    rabbitmq = mq.get_rabbitmq(online)
    for code in mould_codes:
        msg = {}
        msg['mouldCode'] = code
        msg['msgId'] = snow.gen_uid()
        rabbitmq.sender(exchange='mes-pms_mould_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        #print("已发送" + msg["mouldCode"])
    rabbitmq.close()


def check_data(result, sheetName):
    if result is None:
        return
    # 设备-模具，设备，设备参数
    equipment_code = []
    mould_code = []
    unique_kes = []
    for row in result:
        unique_kes.append(row['设备编码'] + '<-->' + row['模具编号'])
        if row['循环时间(s)'] is None:
            print(row['设备编码'] + row['模具编号'] + "循环时间为空")
        if row['调机师'] is None:
            print(row['设备编码'] + row['模具编号'] + "调机师为空")
        if row['搅拌操作师'] is None:
            print(row['设备编码'] + row['模具编号'] + "搅拌操作师为空")
        if row['粉碎操作师'] is None:
            print(row['设备编码'] + row['模具编号'] + "粉碎操作师为空")
        if row['注塑操作师'] is None:
            print(row['设备编码'] + row['模具编号'] + "注塑操作师为空")
        equipment_code.append(row['设备编码'])
        # if '子单-设备编码' in row and (row['子单-设备编码'] is not None and row['子单-设备编码'] != ''):
        #     equipment_code.append(str(row['子单-设备编码']))
        # if '子单-设备编码1' in row and (row['子单-设备编码1'] is not None and row['子单-设备编码1'] != ''):
        #     equipment_code.append(str(row['子单-设备编码1']))
        # if '子单-设备编码2' in row and (row['子单-设备编码2'] is not None and row['子单-设备编码2'] != ''):
        #     equipment_code.append(str(row['子单-设备编码2']))
        # if '子单-设备编码3' in row and (row['子单-设备编码3'] is not None and row['子单-设备编码3'] != ''):
        #     equipment_code.append(str(row['子单-设备编码3']))
        # if '子单-设备编码4' in row and (row['子单-设备编码4'] is not None and row['子单-设备编码4'] != ''):
        #     equipment_code.append(str(row['子单-设备编码4']))
        # if '子单-设备编码5' in row and (row['子单-设备编码5'] is not None and row['子单-设备编码5'] != ''):
        #     equipment_code.append(str(row['子单-设备编码5']))
        # if '子单-设备编码6' in row and (row['子单-设备编码6'] is not None and row['子单-设备编码6'] != ''):
        #     equipment_code.append(str(row['子单-设备编码6']))
        mould_code.append(str(row['模具编号']))

        for i in range(0, 10):
            suffix = '' if i == 0 else str(i)
            code_col_key = '子单-设备编码' + suffix
            name_col_key = '子单-设备名称' + suffix
            if code_col_key in row and (row[code_col_key] is not None and row[code_col_key] != ''):
                equipment_code.append(str(row[code_col_key]))
            # 检查有机边设别名称，但是无编码
            if name_col_key in row and (row[name_col_key] is not None and row[name_col_key] != ''):
                if row[code_col_key] is None or row[code_col_key] == '':
                    print(row['设备编码'] + "--" + row['模具编号'] + "机边设备名称：" + row[name_col_key])

    equipment_codes = list(set(equipment_code))
    mould_codes = list(set(mould_code))

    equipments = db_sql.get_equipments(True, equipment_codes)
    moulds = db_sql.get_moulds(True, mould_codes)
    exist_equipment_codes = []
    exist_mould_codes = []
    for equipment in equipments:
        exist_equipment_codes.append(equipment['equipment_code'])
    for mould in moulds:
        exist_mould_codes.append(mould['mould_code'])

    error_equipments = []
    error_moulds = []
    for e_code in equipment_codes:
        if e_code not in exist_equipment_codes:
            error_equipments.append(e_code)
    for m_code in mould_codes:
        if m_code not in exist_mould_codes:
            error_moulds.append(m_code)

    # 重复数据
    duplicates = find_duplicates(unique_kes)
    print(sheetName)
    print("数据行数: " + str(len(result)))
    if len(error_equipments) > 0:
        print("异常设备: " + ",".join(str(code) for code in error_equipments))
    if len(error_moulds) > 0:
        print("异常模具: " + ",".join(str(code) for code in error_moulds))
    if len(duplicates) > 0:
        print("重复数据: " + str(len(duplicates)) + "条: " + ",".join(str(code) for code in duplicates))
    #send_mould_change_msg(True, mould_codes)
    #print("模具变更消息同步完成")


def read_excel(filename, multithreading: bool = False, sheet_name=None):
    if multithreading:
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            future1 = executor.submit(read_sheet, filename, "生产一部")
            futures.append(future1)
            future2 = executor.submit(read_sheet, filename, "生产二部")
            futures.append(future2)
            future3 = executor.submit(read_sheet, filename, "生产三部")
            futures.append(future3)
            future4 = executor.submit(read_sheet, filename, "生产四部")
            futures.append(future4)

            for future in futures:
                result, sheetName = future.result()  # 阻塞获取结果
                # generate_update_sql(result)
                check_data(result, sheetName)

                # print(f"结果：{len(result)}")
                generate_mould_equipment_bind_sql(result, sheetName)

                # generate_update_sql(result, sheetName)
    else:
        result, sheetName = read_sheet(filename, sheet_name)
        check_data(result, sheetName)

        #generate_mould_equipment_bind_sql(result, sheetName)

        generate_update_sql(result, sheetName)


def read_sheet(filename, sheetName):
    workbook = openpyxl.load_workbook(filename)
    try:
        if sheetName not in workbook:
            return None, sheetName
        sheet = workbook[sheetName]
        title_index_map = {}
        index_title_map = {}
        for cowIndex in range(1, sheet.max_column + 1):
            title = sheet.cell(2, cowIndex).value
            title_index_map[title] = cowIndex
            index_title_map[cowIndex] = title
        shared_list = []
        for rowIndex in range(3, sheet.max_row + 1):
            data = {}
            for cowIndex in range(1, sheet.max_column + 1):
                val = sheet.cell(rowIndex, cowIndex).value
                data[index_title_map[cowIndex]] = val

            # if data['设备编码'] is None or data['设备编码'] == '':
            #     print(sheetName + "设备编码为空，行" + str(rowIndex))
            # if data['模具编号'] is None or data['模具编号'] == '':
            #     print(sheetName + "模具编号为空，行" + str(rowIndex))

            if (data['设备编码'] is not None and data['设备编码'] != '') and (
                    data['模具编号'] is not None and data['模具编号'] != ''):
                shared_list.append(data)
            if (data['设备编码'] is None or data['设备编码'] == '') and (
                    data['模具编号'] is None or data['模具编号'] == ''):
                break
            # if len(shared_list) == 10:
            #     break
        # print(sheetName + " 数据行数: " + str(len(shared_list)))
        return shared_list, sheetName
    except Exception as e:
        # 捕获所有异常，确保子进程能退出
        print(f"读取失败：{str(e)}")
    finally:
        workbook.close()


if __name__ == '__main__':
    # read_excel("D:\\项目相关\\mould-equipment\\0930\\ERP模具基础信息(一厂).xlsx", False, "生产一部")
    read_excel("D:\\项目相关\\mould-equipment\\26-01-26\\ERP模具基础信息(一厂）.xlsx", False, "生产一部")
    # read_excel("D:\\项目相关\\mould-equipment\\0930\\ERP模具基础信息(三厂).xlsx", False, "生产三部")
    # read_excel("D:\\项目相关\\mould-equipment\\0930\\ERP模具基础信息(四厂).xlsx", False, "生产四部")

    # equipment = db_sql.get_mould_equipment(True, 'JBS-2-ZS-69', 'T20-S-11-2')
    # print(equipment)
    # parameter = db_sql.get_equipment_produce_parameter()
    # print(len(parameter))
