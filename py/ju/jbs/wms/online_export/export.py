# -*- coding: utf-8 -*-


import xlrd
import pandas as pd
import xlwt
import db_sql

if __name__ == '__main__':
    # f= open("D:\\项目相关\\stock\\出库单.xlsx","w")
    # workbook = xlrd.open_workbook("D:\\项目相关\\stock\\出库单.xlsx")

    workbook = xlwt.Workbook()

    head_sql = "desc delivery_order"

    his_sql = "SELECT * from `his_delivery_order_2023` WHERE id >= %d  and create_time > '2023-08-01'  and create_time < '2023-10-01' and order_status = 30 and print_status in (20,30,40) limit 1000"

    sql = "SELECT * from `delivery_order` WHERE id >=  %d  and create_time > '2023-08-01'  and create_time < '2023-10-01' and order_status = 30 and print_status in (20,30,40) limit 1000"

    deep_id = 39119955
    size = 0
    sheet_index = 1
    sheet = None
    while True:
        if size == 0 or size == 90000:
            sheet = workbook.add_sheet("Sheet" + str(sheet_index))
            fields = db_sql.query_delivery_order(head_sql)
            for i in range(0, len(fields)):
                sheet.write(0, i, fields[0][0])
            sheet_index += 1
            size+=1

        orders = db_sql.query_delivery_order(his_sql % deep_id)
        if len(orders) == 0:
            break
        for order in orders:
            for i in range(0,len(order)):
                if order[0] is None:
                    continue
                sheet.write(size, i, str(order[i]))
            size+=1
        deep_id = orders[-1][0]+1

    workbook.save("D:\\项目相关\\stock\\出库单.xlsx")







