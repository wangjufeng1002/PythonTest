from pandas.io.sas.sas_constants import align_1_length

from py.ju.jbs.utils.pymysql_comm import UsingOnlineOMS as oms_online
from py.ju.jbs.utils.pymysql_comm import UsingOnlineWms as wms_online

wms_database = ['wms_stock', 'wms_work']
# oms_database = ['oms_business',
#                 'oms_gss',
#                 'oms_logistics',
#                 'oms_ops',
#                 'oms_product',
#                 'oms_report',
#                 'oms_strategy',
#                 'oms_data',
#                 'cbs_ops']

oms_database = ['mes_order', 'mes_aps', 'mes_pms']

query_tale = ("select TABLE_NAME FROM information_schema.TABLES  WHERE  "
              "TABLE_SCHEMA = '{database}' AND TABLE_TYPE = 'BASE TABLE'")
select_columns = ("select COLUMN_NAME FROM information_schema.COLUMNS  WHERE  "
                  "TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{tale_name}'")


def get_tables(date_base, is_oms: bool = True):
    with oms_online() if is_oms else wms_online() as um:
        um.cursor.execute(query_tale.format(database=date_base))
        return um.cursor.fetchall()


def get_column(database, table_name, is_oms: bool = True):
    with oms_online() if is_oms else wms_online() as um:
        um.cursor.execute(select_columns.format(database=database, tale_name=table_name))
        return um.cursor.fetchall()


alter_sql = 'alter table {database}.{table_name} '
add_create_time = '''ADD create_time  timestamp   default CURRENT_TIMESTAMP not null comment '创建时间' '''
add_update_time = '''ADD update_time  timestamp   default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间' '''


def out_put_sql(sqls: list, file_name: str):
    file = open("D:\项目相关\补充创建时间更新时间\\{file_name}.sql".format(file_name=file_name), "w",
                encoding='utf-8')
    for sql in sqls:
        file.write(sql)
        file.write('\n')
    file.flush()
    file.close()
    print(file_name + "写入完成")


def scan_generate_sql(date_bases, is_oms: bool = True):
    if date_bases is None or len(date_bases) == 0:
        return
    for database in date_bases:
        tale_add_sqls = []
        for table_name in get_tables(database, is_oms=is_oms):
            tale_add_sql_parts = []
            columns = get_column(database, table_name['TABLE_NAME'], is_oms=is_oms)
            column_names = [column['COLUMN_NAME'] for column in columns]
            if 'create_time' not in column_names:
                tale_add_sql_parts.append(add_create_time)
                # tale_add_sql = alter_sql.format(database=database,
                #                                 table_name=table_name['TABLE_NAME']) + add_create_time
            if 'update_time' not in column_names:
                tale_add_sql_parts.append(add_update_time)
            if len(tale_add_sql_parts) > 0:
                tale_add_sql = alter_sql.format(database=database, table_name=table_name['TABLE_NAME'])
                align_length = len(tale_add_sql)
                for i in range(len(tale_add_sql_parts)):
                    if i > 0:
                        tale_add_sql = tale_add_sql + "\n" + " " * align_length + "," + tale_add_sql_parts[i]
                    else:
                        tale_add_sql = tale_add_sql + tale_add_sql_parts[i]
                tale_add_sql = tale_add_sql + ";"
                tale_add_sqls.append(tale_add_sql)
        out_put_sql(tale_add_sqls, database)
        print(f"{database}".format(database=database) + " 处理完成")


if __name__ == '__main__':
    #scan_generate_sql(date_bases=wms_database, is_oms=False)
    scan_generate_sql(date_bases=oms_database, is_oms=True)
