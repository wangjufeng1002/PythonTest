from pymysql_comm import UsingMysql
import datetime
import json
from pymysql.converters import escape_string
from db_connect_pool import POOL


def inset_refund_appointment_order(order_sql,details_sql):

    with POOL.connection() as conn:
        conn.cursor().execute(order_sql)
        for detail_sql in details_sql:
            conn.cursor().execute(detail_sql)
        conn.cursor().close()
        conn.commit()

