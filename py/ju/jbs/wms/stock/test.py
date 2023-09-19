# -*- coding: utf-8 -*-

import csv
import pandas
import xlrd

# csv1 = csv.reader(open(r"D:\\库存文件\\库位库存导入(1).xlsx",encoding="utf_8"))
# #csv2 = csv.reader(open("D:\\库存文件\\库位库存导入(2).xlsx"))
#
# for item in csv1:
#     print(item)

workbook = xlrd.open_workbook("D:\\库存文件\\库位库存导入(1).xlsx")
sheets_ = workbook.sheets()[0]

nrows = sheets_.nrows

data_map = []
count_1 = 0

for index in range(1,nrows):
    values = sheets_.row_values(rowx=index)
    if values[1].replace(" ", "") + values[3].replace(" ", "") in data_map:
        count_1+=1
    data_map.append(values[1].replace(" ","") + values[3].replace(" ",""))
print(count_1)

#====2===
workbook_2 = xlrd.open_workbook("D:\\库存文件\\库位库存导入(2).xlsx")
sheets_2 = workbook_2.sheets()[0]
nrows_2 = sheets_2.nrows

count = 0

for index in range(1,nrows_2):
    values = sheets_2.row_values(rowx=index)
    if values[1].replace(" ","") + values[3].replace(" ","") in data_map:
       #print(values[1].replace(" ","") +"<->" +values[3].replace(" ",""))
       count += 1
print(count)
