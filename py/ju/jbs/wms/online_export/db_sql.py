
from ju.jbs.common.db.db_connect_pool import ONLINE_POOL


def query_delivery_order(sql):
    with ONLINE_POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
