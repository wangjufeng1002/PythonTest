from pymysql_online import UsingMysql as online
from pymysql_dev import UsingMysql as dev
import datetime
import json
from pymysql.converters import escape_string
from db_connect_pool import DEV_POOL
from db_connect_pool import ONLINE_POOL
import multiprocessing


# Imc 出库单
def get_product_sku(page_from, page_size):
    sql = "SELECT * FROM oms_product.`product_sku` limit %d,%d" % (page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()
def get_supplier(page_from, page_size):
    sql = "SELECT * FROM srm_supply.`supplier` limit %d,%d" % (page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()
def get_warehouse(page_from, page_size):
    sql = "SELECT * FROM oms_product.`warehouse` where warehouse_use_type = 2  limit %d,%d" % (page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# DEV imc
def insert_iom(sqls):
    with DEV_POOL.connection() as conn:
        if isinstance(sqls, list):
            for sql in sqls:
                conn.cursor().execute(sql)
        conn.cursor().close()
        conn.commit()


def copy_product_sku(page_from, page_size):
    product_skus = get_product_sku(page_from, page_size)
    product_sku_insert_sql = []
    if len(product_skus) == 0:
        return False
    for purchase_price in product_skus:
        ls = [(k, v) for k, v in purchase_price.items() if (v is not None and k != 'id')]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert into oms_product.`product_sku` (" + keys + ") values (" + values + " ) on duplicate key update sku_name = " + repr(str(purchase_price['sku_name'])) + " ;"
        product_sku_insert_sql.append(sql)
    insert_iom(product_sku_insert_sql)
    return True


def copy_supplier(page_from, page_size):
    suppliers = get_supplier(page_from, page_size)
    supplier_sql = []
    if len(suppliers) == 0:
        return False
    for supplier in suppliers:
        ls = [(k, v) for k, v in supplier.items() if (v is not None and k != 'id')]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert into srm_supply.`supplier` (" + keys + ") values (" + values + " ) on duplicate key update supplier_name = " + repr(str(supplier['supplier_name'])) + " ;"
        supplier_sql.append(sql)
    insert_iom(supplier_sql)
    return True

def copy_warehouse(page_from, page_size):
    warehouses = get_warehouse(page_from, page_size)
    warehouse_sql = []
    if len(warehouses) == 0:
        return False
    for warehouse in warehouses:
        ls = [(k, v) for k, v in warehouse.items() if (v is not None and k != 'id')]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert into oms_product.`warehouse` (" + keys + ") values (" + values + " ) on duplicate key update supplier_code = " + repr(str(warehouse['supplier_code'])) + " ;"
        warehouse_sql.append(sql)
    print(warehouse_sql)
    #insert_iom(warehouse_sql)
    return True

def copy_product_sku_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_order_loop page:{}".format(page_num))
        if copy_product_sku((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1



def copy_supplier_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_supplier_loop page:{}".format(page_num))
        if copy_supplier((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1
def copy_warehouse_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_warehouse_loop page:{}".format(page_num))
        if copy_warehouse((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


if __name__ == '__main__':
    #copy_product_sku_loop(1000)
    #copy_supplier_loop(100)
    copy_warehouse_loop(1000)