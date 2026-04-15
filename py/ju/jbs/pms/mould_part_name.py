import json
from concurrent.futures import ThreadPoolExecutor
import mq
import openpyxl
from toollib.guid import SnowFlake
from py.ju.jbs.utils import db_sql

mould_update_template_sql = \
    '''update mes_pms.mould set product_name = '{product_name}' ,part_name = '{part_name}' where mould_code = '{mould_code}' ; '''

file_path = 'D:\\项目相关\\mould\\mould_part_name'


def check_data(result, sheetName):
    mould_code = []
    for row in result:
        mould_code.append(str(row['模具编码'].replace(' ', '')).replace('\n', ''))

    mould_codes = list(set(mould_code))
    moulds = db_sql.get_moulds(True, mould_codes)
    exist_mould_codes = []
    error_moulds = []
    for mould in moulds:
        exist_mould_codes.append(mould['mould_code'])
    for m_code in mould_codes:
        if m_code not in exist_mould_codes and m_code.upper() not in exist_mould_codes:
            error_moulds.append(m_code)

    print(sheetName)
    print("数据行数: " + str(len(result)))
    if len(error_moulds) > 0:
        print("异常模具: " + ",".join(str(code) for code in error_moulds))


def read_sheet(filename, sheetName):
    workbook = openpyxl.load_workbook(filename)
    try:
        if sheetName not in workbook:
            return None, sheetName
        sheet = workbook[sheetName]
        title_index_map = {}
        index_title_map = {}
        for cowIndex in range(1, sheet.max_column + 1):
            title = sheet.cell(3, cowIndex).value
            title_index_map[title] = cowIndex
            index_title_map[cowIndex] = title
        shared_list = []
        for rowIndex in range(4, sheet.max_row + 1):
            data = {}
            for cowIndex in range(1, sheet.max_column + 1):
                val = sheet.cell(rowIndex, cowIndex).value
                data[index_title_map[cowIndex]] = str(val).replace('\n', '').strip().upper()


            if ((data['模具编码'] is not None and data['模具编码'] != '' and data['模具编码'] != 'NONE')
                    and (data['产品名称'] is not None and data['产品名称'] != '' and data['产品名称'] != 'NONE')
                    and (data['零件名称'] is not None and data['零件名称'] != '' and data['零件名称'] != 'NONE')
            ):
                shared_list.append(data)
            if ((data['模具编码'] is None or data['模具编码'] == '' or data['模具编码'] == 'NONE' )
                    and (data['产品名称'] is None or data['产品名称'] == '' or data['产品名称'] == 'NONE')
                    and (data['零件名称'] is None or data['零件名称'] == '' or data['零件名称'] == 'NONE')

            ):
                break
            # if len(shared_list) == 10:
            #     break
        print(sheetName + " 数据行数: " + str(len(shared_list)))
        return shared_list, sheetName
    except Exception as e:
        # 捕获所有异常，确保子进程能退出
        print(f"读取失败：{str(e)}")
    finally:
        workbook.close()


def out_put_sql(sqls: list, file_name: str, path: str):
    file = open("{file_path}\\{file_name}.sql".format(file_path=path, file_name=file_name), "w",
                encoding='utf-8')
    for sql in sqls:
        file.write(sql)
        file.write('\n')
    file.flush()
    file.close()
    print(file_name + "写入完成")


def generate_mould_update_sql(results, sheet_name):
    sqls = []
    for data in results:
        update_sql = mould_update_template_sql.format(mould_code=data['模具编码'],
                                                      product_name=data['产品名称'], part_name=data['零件名称'])
        sqls.append(update_sql)
    out_put_sql(sqls, sheet_name + "-模具信息更新", path=file_path)


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
                check_data(result, sheetName)
                generate_mould_update_sql(result, sheetName)
    else:
        result, sheetName = read_sheet(filename, sheet_name)
        check_data(result, sheetName)
        generate_mould_update_sql(result, sheetName)




if __name__ == '__main__':
    read_excel("D:\\项目相关\\mould\\mould_part_name\\产品名称和零件名称【生产二部】.xlsx", False, "生产二部")
    read_excel("D:\\项目相关\\mould\\mould_part_name\\产品名称和零件名称【生产三部】.xlsx", False, "生产三部")
    read_excel("D:\\项目相关\\mould\\mould_part_name\\产品名称和零件名称【生产四部】.xlsx", False, "生产四部")


