import pymysql
from timeit import default_timer


host = '192.168.1.201'
port = 3306
db = 'wms_stock'
user = 'oms_test'
password = 'h6I8RiqSzL'

# host = '192.168.47.210'
# port = 3306
# db = 'data-scraping'
# user = 'root'
# password = '123456'




# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


# ---- 使用 with 的方式来优化代码
class UsingMysql(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()
    @property
    def cursor(self):
        return self._cursor

