
import xlrd
import xlwt
import xlsxwriter
from xlutils.copy import copy

# if __name__ == '__main__':
#     workbook = xlrd.open_workbook("C:\\Users\\PC\\Desktop\\退货入库物流单号.xlsx")
#
#     # 将已存在的excel拷贝进新的excel
#     new_workbook = copy(workbook)
#     xlwt.Workbook()
#
#     # 获取sheet
#     new_worksheet = new_workbook.get_sheet(0)
#     data_set = ["wjf,wkf"]
#     # 写入数据
#     row = 5  # 已存在文件中的数据行数
#     for data in data_set:
#         new_worksheet.write(row, 0, data[0])
#         new_worksheet.write(row, 1, data[1])
#
#
#         row += 1

def edit_excel():
    # 打开已有的Excel文件
    workbook = xlrd.open_workbook('existing_file.xls')

    # 获取第一个工作表
    worksheet = workbook.sheet_by_index(0)

    # 获取工作表的行数和列数
    num_rows = worksheet.nrows
    num_cols = worksheet.ncols

    # 创建一个新的工作簿
    new_workbook = xlwt.Workbook()

    # 添加一个工作表
    new_worksheet = new_workbook.add_sheet('Sheet1')

    # 复制已有的数据
    for row in range(num_rows):
        for col in range(num_cols):
            # 获取单元格的值
            cell_value = worksheet.cell_value(row, col)

            # 将单元格的值写入新的工作表
            new_worksheet.write(row, col, cell_value)

    # 写入新的数据
    new_worksheet.write(num_rows, 0, 'New Data 1')
    new_worksheet.write(num_rows, 1, 'New Data 2')

    # 保存新的工作簿
    new_workbook.save('existing_file.xls')



