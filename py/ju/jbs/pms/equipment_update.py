import csv
import time
import pandas
import xlrd
from toollib.guid import SnowFlake
import openpyxl
from openpyxl.utils import datetime as xl_datetime

from py.ju.jbs.material.material_compare import generate_update_sql
from pymysql_comm import UsingOnlineOMS as oms_online
from pymysql_comm import UsingOnlineOMS as oms_dev
import datetime
import json
from db_sql import *

# 供应商字典
supplier_dict = get_supplier_dict()
# 工厂字典
factory_dict = get_factory_dict()

unit_dict = get_unit_dict()
snow = SnowFlake()

def get_cell_color(cell):
    if cell.fill.start_color.index != '00000000':
        color_type = cell.fill.start_color.type
        if color_type == 'rgb':
            rgb = cell.fill.start_color.rgb
            #print(f'单元格 {cell.coordinate} 的 RGB 颜色: {rgb}')
            return rgb

        elif color_type == 'theme':
            theme = cell.fill.start_color.theme
            tint = cell.fill.start_color.tint
            #print(f'单元格 {cell.coordinate} 的主题颜色索引: {theme}, 色调: {tint}')
            return tint
def get_clamping_type(name):
    if name == '二板式':
        return 1
    if name == '三板式':
        return 2
    if name == '四板式':
        return 3
    if name == '五板式':
        return 4
def get_equipment_type(name):
    if name == '注塑机':
        return 1
    if name == '辅助生产设备':
        return 2
    if name == '机边设备':
        return 3

def build_update(equipment_sheet, rowIndex, title_index_map):
    equipment_field = {}
    # 'FFFFFF00'
    equipment_field['equipment_code'] = equipment_sheet.cell(rowIndex, title_index_map['设备编码']).value
    # 资产原值
    cost_cell = equipment_sheet.cell(rowIndex, title_index_map['资产原值(元)'])
    if get_cell_color(cost_cell) == 'FFFFFF00':
        equipment_field['equipment_cost'] = cost_cell.value
    # 实际能耗
    energy_cell = equipment_sheet.cell(rowIndex, title_index_map['实际能耗(%)'])
    if get_cell_color(energy_cell) == 'FFFFFF00':
        equipment_field['energy_consumption'] = energy_cell.value
    # 额定功率
    rated_power_cell = equipment_sheet.cell(rowIndex, title_index_map['额定功率(kw)'])
    if get_cell_color(rated_power_cell) == 'FFFFFF00':
        equipment_field['rated_power'] = rated_power_cell.value

    # # 额定功率
    # supplier_cell = equipment_sheet.cell(rowIndex, title_index_map['制造商'])
    # if get_cell_color(supplier_cell) == 'FFFFFF00':
    #     if supplier_cell.value is None or supplier_cell.value == '' or supplier_cell.value not in supplier_dict:
    #         print("供应商不存在，设备编码：%s" % equipment_field['equipment_code'])
    #     equipment_field['supplier_code'] = supplier_dict.get(supplier_cell.value)
    return equipment_field


def build_insert(equipment_sheet, rowIndex, title_index_map):
    supplier_cell = equipment_sheet.cell(rowIndex, title_index_map['制造商'])
    supplier_name = "无铭牌"
    if supplier_cell.value is None or supplier_cell.value == '' or supplier_cell.value not in supplier_dict:
        #print("供应商不存在，设备编码：%s" % equipment_sheet.cell(rowIndex, title_index_map['设备编码']).value)
        return None
    else:
        supplier_name = equipment_sheet.cell(rowIndex, title_index_map['制造商']).value

    if equipment_sheet.cell(rowIndex, title_index_map['设备编码']).value is None:
        return None
    equipment_field = {}
    equipment_field['equipment_id'] = 'E' + str(snow.gen_uid())
    equipment_field['equipment_code'] = equipment_sheet.cell(rowIndex, title_index_map['设备编码']).value
    equipment_field['equipment_name'] = equipment_sheet.cell(rowIndex, title_index_map['设备名称']).value
    equipment_field['supplier_code'] = supplier_dict.get(supplier_name)
    equipment_field['clamping_device_type'] = get_clamping_type(
        equipment_sheet.cell(rowIndex, title_index_map['合膜装置']).value)
    equipment_field['equipment_type'] = get_equipment_type(equipment_sheet.cell(rowIndex, title_index_map['设备类型']).value)
    equipment_field['auth_status'] = 10
    equipment_field['bar_code'] = 1
    equipment_field['equipment_status'] = 10
    equipment_field['factory_code'] = factory_dict.get(equipment_sheet.cell(rowIndex, title_index_map['所属工厂']).value)
    equipment_field['baking_equipment'] = True if equipment_sheet.cell(rowIndex, title_index_map['烘料设备']).value == '是' else False
    equipment_field['measure_unit_code'] = unit_dict.get(equipment_sheet.cell(rowIndex, title_index_map['计量单位']).value)
    equipment_field['equipment_model'] = equipment_sheet.cell(rowIndex, title_index_map['规格型号']).value
    equipment_field['bar_code'] = equipment_sheet.cell(rowIndex, title_index_map['设备资产编码']).value
    equipment_field['used_start_date'] = equipment_sheet.cell(rowIndex, title_index_map['开始使用时间']).value
    equipment_field['equipment_tonnage'] = equipment_sheet.cell(rowIndex, title_index_map['机台吨位(T)']).value
    equipment_field['equipment_location'] = equipment_sheet.cell(rowIndex, title_index_map['位置/机台号']).value
    equipment_field['work_hour_max'] = equipment_sheet.cell(rowIndex, title_index_map['最大工作时长(h)']).value
    equipment_field['productivity'] = equipment_sheet.cell(rowIndex, title_index_map['生产效率(只/小时)']).value
    equipment_field['rated_power'] = equipment_sheet.cell(rowIndex, title_index_map['额定功率(kw)']).value
    equipment_field['equipment_cost'] = equipment_sheet.cell(rowIndex, title_index_map['资产原值(元)']).value
    equipment_field['energy_consumption'] = equipment_sheet.cell(rowIndex, title_index_map['实际能耗(%)']).value
    equipment_field['depreciation_period'] = equipment_sheet.cell(rowIndex, title_index_map['折旧年限(年)']).value
    equipment_field['remark'] = equipment_sheet.cell(rowIndex, title_index_map['备注']).value

    equipment_param = {}
    # equipment_param['equipmentCode'] = equipment_sheet.cell(rowIndex, title_index_map['设备编码']).value
    # equipment_param['screwDiameter'] = equipment_sheet.cell(rowIndex, title_index_map['螺杆直径(mm)']).value
    # equipment_param['glueVolume'] = equipment_sheet.cell(rowIndex, title_index_map['射胶量(g)']).value
    # equipment_param['takeProductSpace'] = equipment_sheet.cell(rowIndex, title_index_map['取产品空间(mm)']).value
    # equipment_param['lockMouldMax'] = equipment_sheet.cell(rowIndex, title_index_map['锁模力最大(ton)']).value
    # equipment_param['openMould'] = equipment_sheet.cell(rowIndex, title_index_map['开模力(ton)']).value
    # equipment_param['openMouldTravel'] = equipment_sheet.cell(rowIndex, title_index_map['开模行程(mm)']).value
    # equipment_param['guidePoleHorizontal'] = equipment_sheet.cell(rowIndex,
    #                                                               title_index_map['导柱内距水平(mm)']).value
    # equipment_param['guidePoleVertical'] = equipment_sheet.cell(rowIndex, title_index_map['导柱内距垂直(mm)']).value
    # equipment_param['mouldCapacityThin'] = equipment_sheet.cell(rowIndex, title_index_map['模容量最薄(mm)']).value
    # equipment_param['mouldCapacityThick'] = equipment_sheet.cell(rowIndex, title_index_map['模容量最厚(mm)']).value
    # equipment_param['mouldMaxDistance'] = equipment_sheet.cell(rowIndex, title_index_map['模板最大距离(mm)']).value
    # equipment_param['oilPumpMaxPower'] = equipment_sheet.cell(rowIndex, title_index_map['油泵电机功率(kw)']).value
    # equipment_param['electricityHeat'] = equipment_sheet.cell(rowIndex, title_index_map['电热量(kw)']).value
    equipment_field['equipment_param'] = equipment_param

    return  equipment_field



def out_put_insert_sql(equipment_list: list, table, file_name):
    sql = '''insert into mes_pms.{table}({field_sql}) values({value_sql});'''
    file = open("D:\\测试文件\\pms\\{file_name}.sql".format(file_name=file_name), "w", encoding='utf-8')
    for equipment in equipment_list:
        field_sql = ''
        value_sql = ''
        for field in equipment:
            if equipment[field] is not None:
                field_sql += '`' + field + '`,'
                if type(equipment[field]) == int or type(equipment[field]) == float:
                    value_sql += str(equipment[field]) + ','
                if type(equipment[field]) == str:
                    value_sql += '\'' + str(equipment[field]) + '\','
                if type(equipment[field]) == dict:
                    value_sql += '\'' + json.dumps(equipment[field], ensure_ascii=False).replace('\"', '\\"') + '\','
                if type(equipment[field]) == bool:
                    value_sql += str(1 if equipment[field] is True else 0) + ','
                if type(equipment[field]) == datetime.datetime:
                    value_sql += '\'' + str(equipment[field].strftime('%Y-%m-%d %H:%M:%S')) + '\','
        field_sql = field_sql[:-1]
        value_sql = value_sql[:-1]
        print(sql.format(table=table, field_sql=field_sql, value_sql=value_sql))
        file.write(sql.format(table=table, field_sql=field_sql, value_sql=value_sql) + '\n')

def out_put_update_sql(equipment_list: list, table, file_name):
    sql = '''update mes_pms.{table} set {set_sql} where equipment_code = {equipment_code};'''
    file = open("D:\\测试文件\\pms\\{file_name}.sql".format(file_name=file_name), "w", encoding='utf-8')
    for equipment in equipment_list:
        set_value = ''
        for field in equipment:
            if field == 'equipment_code':
                continue
            if equipment[field] is not None:
                if type(equipment[field]) == int or type(equipment[field]) == float:
                    set_value += '`'+field +'`' + '=' + str(equipment[field]) + ','
                if type(equipment[field]) == str:
                    set_value += '`'+field +'`' + '=' + '\'' + str(equipment[field]) + '\','
                if type(equipment[field]) == dict:
                    set_value += '`' + field + '`' + '=' +'\'' + json.dumps(equipment[field], ensure_ascii=False).replace('\"', '\\"') + '\','
                if type(equipment[field]) == bool:
                    set_value += '`'+field +'`' + '=' + str(1 if equipment[field] is True else 0) + ','
                if type(equipment[field]) == datetime.datetime:
                    set_value += '`'+field +'`' + '=' + '\'' + str(equipment[field].strftime('%Y-%m-%d %H:%M:%S')) + '\','
        set_value = set_value[:-1]
        print(sql.format(table=table, set_sql=set_value, equipment_code='\'' + str(equipment['equipment_code']) + '\''))
        file.write(sql.format(table=table, set_sql=set_value,
                              equipment_code='\'' + str(equipment['equipment_code']) + '\'') + "\n")

def generate_update_sql(equipment_update_list):
    out_put_update_sql(equipment_update_list,'equipment', "0530-修改")
    return


def generate_insert_sql(equipment_insert_list):
    out_put_insert_sql(equipment_insert_list, 'equipment', "0530-新增")
    return


def read_excel(filename):
    workbook = openpyxl.load_workbook(filename)
    equipment_sheet = workbook["注塑机"]
    title_index_map = {}
    equipment_update_list = []
    equipment_insert_list = []
    for cowIndex in range(1, equipment_sheet.max_column + 1):
        title = equipment_sheet.cell(1, cowIndex).value
        title_index_map[title] = cowIndex
    for rowIndex in range(2, equipment_sheet.max_row + 1):
        remark1 = equipment_sheet.cell(rowIndex, title_index_map['备注1']).value
        if remark1 == '修改':
            update = build_update(equipment_sheet, rowIndex, title_index_map)
            if update is not None:
                equipment_update_list.append(update)
        if remark1 == '新增':
            insert = build_insert(equipment_sheet, rowIndex, title_index_map)
            if insert is not None:
                equipment_insert_list.append(insert)
    generate_update_sql(equipment_update_list)
    generate_insert_sql(equipment_insert_list)

if __name__ == '__main__':
    read_excel("D:\测试文件\pms\设备-基础信息202505-30.xlsx.xlsx")
