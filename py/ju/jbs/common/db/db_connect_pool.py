import pymysql
from dbutils.pooled_db import PooledDB
from py.ju.jbs.common.config.db_config import (
    dev_host, dev_port, dev_user, dev_password,
    test_host, test_port, test_user, test_password,
    online_host, online_port, online_user, online_password
)


DEV_POOL = PooledDB(
    # 使用链接数据库的模块
    creator=pymysql,
    # 连接池允许的最大连接数，0和None表示不限制连接数
    maxconnections=20,
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached=2,
    # 链接池中最多闲置的链接，0和None不限制
    maxcached=5,
    # 链接池中最多共享的链接数量，0和None表示全部共享。
    # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
    # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
    maxshared=3,
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用。
    #  如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    # 字符编码
    charset='utf8',
    host=dev_host,
    # 端口
    port=dev_port,
    # 数据库用户名
    user=dev_user,
    # 数据库密码
    password=dev_password,
    # 数据库名
    database='wms_stock',
)


TEST_POOL = PooledDB(
    # 使用链接数据库的模块
    creator=pymysql,
    # 连接池允许的最大连接数，0和None表示不限制连接数
    maxconnections=20,
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached=2,
    # 链接池中最多闲置的链接，0和None不限制
    maxcached=5,
    # 链接池中最多共享的链接数量，0和None表示全部共享。
    # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
    # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
    maxshared=3,
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用。
    #  如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    # 字符编码
    charset='utf8',
    host=test_host,
    # 端口
    port=test_port,
    # 数据库用户名
    user=test_user,
    # 数据库密码
    password=test_password,
    # 数据库名
    database='wms_stock',
)

# 线上数据库连接
ONLINE_POOL = PooledDB(
    # 使用链接数据库的模块
    creator=pymysql,
    # 连接池允许的最大连接数，0和None表示不限制连接数
    maxconnections=20,
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached=2,
    # 链接池中最多闲置的链接，0和None不限制
    maxcached=5,
    # 链接池中最多共享的链接数量，0和None表示全部共享。
    # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
    # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
    maxshared=3,
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用。
    #  如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    # 字符编码
    charset='utf8',
    host=online_host,
    # 端口
    port=online_port,
    # 数据库用户名
    user=online_user,
    # 数据库密码
    password=online_password,
    # 数据库名
    database='wms_work',
)
