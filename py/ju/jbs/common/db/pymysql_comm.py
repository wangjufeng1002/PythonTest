import pymysql
from timeit import default_timer
from ju.jbs.common.config.db_config import (
    dev_host, dev_port, dev_user, dev_password,
    test_host, test_port, test_user, test_password,
    online_host, online_port, online_user, online_password,
    oms_online_host, oms_online_port, oms_online_user, oms_online_password
)


# ---- 用pymysql 操作数据库
def get_dev_connection():
    conn = pymysql.connect(host=dev_host, port=dev_port, user=dev_user, password=dev_password)
    return conn


# ---- 使用 with 的方式来优化代码
class UsingDev(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_dev_connection()
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


# ---- 用pymysql 操作数据库
def get_test_connection():
    conn = pymysql.connect(host=test_host, port=test_port, user=test_user, password=test_password)
    return conn


# ---- 使用 with 的方式来优化代码
class UsingTest(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_test_connection()
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


# ---- 用pymysql 操作数据库
def get_online_connection():
    conn = pymysql.connect(host=online_host, port=online_port, user=online_user, password=online_password)
    return conn

# ---- 使用 with 的方式来优化代码
class UsingOnlineWms(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_online_connection()
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


# ---- 用pymysql 操作数据库
def get_oms_online_connection():
    conn = pymysql.connect(host=oms_online_host, port=oms_online_port, user=oms_online_user, password=oms_online_password)
    return conn

# ---- 使用 with 的方式来优化代码
class UsingOnlineOMS(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_oms_online_connection()
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
