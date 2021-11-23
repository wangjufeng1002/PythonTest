#coding=utf-8
from pymysql_comm import UsingMysql


def execute(sql):
    print(sql)
    with UsingMysql() as um:
        um.cursor.execute(sql)
        um._conn.commit()
