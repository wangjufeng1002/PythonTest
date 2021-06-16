# coding=utf-8
import pandas as pd
import xlrd

file_object = open('C:\\Users\\wangjufeng\\Desktop\\代退运费.txt', "w", encoding='utf-8')
sql = "update refund_audit set sync_status = 100, approve_failed_count =0 where order_id = %d and source_id=%d and shop_id = %d and is_agree = 2 and refund_source = 7 and refund_amount=%.2f ;"
excel_reader = pd.ExcelFile("D:\\wechat-data\\WXWork\\1688851994959441\\Cache\\File\\2021-06\\代退运费+仅退款不退货.xlsx")
sheet_names = excel_reader.sheet_names
df_data =  excel_reader.parse(sheet_name=sheet_names[0])  # 读取表单的内容，i是表单名的索引，等价于pd.read_excel('文件.xlsx', sheet_name=sheet_names[i])
for row in df_data.values:
    eSQL = sql % (row[0], row[1], row[2], round(row[4], 2))
    file_object.write(eSQL + "\n")
    file_object.flush()


file_object = open('C:\\Users\\wangjufeng\\Desktop\\仅退款.txt', "w", encoding='utf-8')
sql = "update refund_audit set sync_status = 100, approve_failed_count =0 where order_id = %d and source_id=%d and shop_id = %d and is_agree = 2 and refund_source = 9 and refund_amount=%.2f ;"
excel_reader = pd.ExcelFile("D:\\wechat-data\\WXWork\\1688851994959441\\Cache\\File\\2021-06\\代退运费+仅退款不退货.xlsx")
sheet_names = excel_reader.sheet_names
df_data = excel_reader.parse(sheet_name=sheet_names[1])  # 读取表单的内容，i是表单名的索引，等价于pd.read_excel('文件.xlsx', sheet_name=sheet_names[i])
for row in df_data.values:
    eSQL = sql % (row[0], row[1], row[2], round(row[4], 2))
    file_object.write(eSQL + "\n")
    file_object.flush()