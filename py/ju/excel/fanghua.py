import time

import pandas
import xlrd
import xlwt
from toollib.snowflake import snow
import numpy as np

if __name__ == '__main__':
    workbook = xlrd.open_workbook("C:\\Users\\PC\\Desktop\\业主名单.xlsx")
    sheets_ = workbook.sheets()[0]
    rows = sheets_.nrows
    count_1 = 0

    room_mobile = []

    for index in range(0, rows, 2):
        room = sheets_.row_values(rowx=index)[0]
        if room is None or room == '':
            continue
        phone = sheets_.row_values(rowx=index + 1)[0]
        if phone is None or phone == '':
            phone = ''
        else:
            phone = str(int(phone))
        room_mobile.append(room + "<->" + phone)
        print(room + "<->" + phone)

    room_mobile_group = []
    for i in range(0,16):
        room_mobile_group.append([])

    for rm in room_mobile:
        splits = str(rm).split("<->")
        room = splits[0]
        building_number = room.split("-")[0].replace("芳", "")
        room_mobile_group[int(building_number)].append(rm)
    print(len(room_mobile_group))

    #创建一个Workbook对象
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建一个Sheet对象
    for index in range(1, len(room_mobile_group)):
        build_rooms = room_mobile_group[index]
        sheet = workbook.add_sheet(str(index) + "#")
        for room_index in range(0, len(build_rooms)):
            splits = str(build_rooms[room_index]).split("<->")
            room = splits[0]
            mobile = splits[1]
            # 写入数据到单元格
            sheet.write(room_index, 0, room)  # 在第一行第一列写入'Hello'
            sheet.write(room_index, 1, mobile)  # 在第一行第二列写入'World'
            workbook.save('C:\\Users\\PC\\Desktop\\整理后.xlsx')
