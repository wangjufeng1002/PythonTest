import sys
import threading

from pymysql_online import UsingMysql as online
from pymysql_dev import UsingMysql as dev
import datetime
import json
from pymysql.converters import escape_string
from db_connect_pool import DEV_POOL
from db_connect_pool import ONLINE_POOL
import multiprocessing

replace_warehouse_code = ['WH0016', 'WH0019', 'WH0020', 'WH0021', 'WH0022', 'WH0023', 'WH0024', 'WH0025', 'WH0040',
                          'WH0042',
                          'WH0043', 'WH0044', 'WH0045', 'WH0046', 'WH0047', 'WH0048', 'WH0049', 'WH0050', 'WH0051',
                          'WH0052',
                          'WH0053', 'WH0056', 'WH0057', 'WH0058', 'WH0059', 'WH0060', 'WH0061', 'WH0062', 'WH0063',
                          'WH0064',
                          'WH0065', 'WH0066', 'WH0067', 'WH0068', 'WH0069', 'WH0070', 'WH0071', 'WH0072', 'WH0073',
                          'WH0074', 'WH0075', 'WH0076',
                          'WH0077', 'WH0078', 'WH0079', 'WH0080', 'WH0081', 'WH0082', 'WH0083', 'WH0084', 'WH0085',
                          'WH0086', 'WH0087', 'WH0088',
                          'WH0089', 'WH0091', 'WH0093', 'WH0094', 'WH0095', 'WH0096', 'WH0097', 'WH0098', 'WH0099',
                          'WH0100', 'WH0101', 'WH0102',
                          'WH0103', 'WH0104', 'WH0105', 'WH0107', 'WH0108', 'WH0109', 'WH0110', 'WH0111', 'WH0112',
                          'WH0113', 'WH0114', 'WH0115', 'WH0116',
                          'WH0117', 'WH0118', 'WH0119', 'WH0120', 'WH0121', 'WH0122', 'WH0123', 'WH0124', 'WH0125',
                          'WH0126', 'WH0127', 'WH0128', 'WH0129',
                          'WH0130', 'WH0131', 'WH0132', 'WH0133', 'WH0134', 'WH0135', 'WH0136', 'WH0137', 'WH0138',
                          'WH0139', 'WH0140', 'WH0141', 'WH0142',
                          'WH0143', 'WH0144', 'WH0145', 'WH0146', 'WH0147', 'WH0148', 'WH0149', 'WH0150', 'WH0151',
                          'WH0152', 'WH0153', 'WH0154', 'WH0155', 'WH0156',
                          'WH0157', 'WH0158', 'WH0159', 'WH0160', 'WH0161', 'WH0162', 'WH0163', 'WH0164', 'WH0165',
                          'WH0166', 'WH0167', 'WH0168', 'WH0169', 'WH0170',
                          'WH0172', 'WH0173', 'WH0174', 'WH0175', 'WH0176', 'WH0177', 'WH0178', 'WH0179', 'WH0180',
                          'WH0181', 'WH0182', 'WH0183', 'WH0184', 'WH0185', 'WH0186', 'WH0187', 'WH0188', 'WH0189',
                          'WH0190', 'WH0191', 'WH0192', 'WH0193', 'WH0194', 'WH0195', 'WH0196', 'WH0197', 'WH0198',
                          'WH0199', 'WH0200', 'WH0201', 'WH0202', 'WH0203', 'WH0204', 'WH0205', 'WH0206', 'WH0207',
                          'WH0208', 'WH0209', 'WH0210', 'WH0211', 'WH0212', 'WH0213', 'WH0214', 'WH0215', 'WH0216',
                          'WH0217', 'WH0218', 'WH0219', 'WH0220', 'WH0221', 'WH0222', 'WH0223', 'WH0224', 'WH0226',
                          'WH0227', 'WH0228', 'WH0229', 'WH0230', 'WH0231', 'WH0233', 'WH0234', 'WH0235', 'WH0236',
                          'WH0237', 'WH0238', 'WH0239', 'WH0240', 'WH0241', 'WH0243', 'WH0244', 'WH0245', 'WH0246',
                          'WH0247', 'WH0248', 'WH0249', 'WH0250', 'WH0251', 'WH0252', 'WH0254', 'WH0255', 'WH0256',
                          'WH0257', 'WH0258', 'WH0260', 'WH0261', 'WH0262', 'WH0263', 'WH0264', 'WH0265', 'WH0267',
                          'WH0268', 'WH0269', 'WH0270', 'WH0287', 'WH0288', 'WH0289', 'WH0290', 'WH0291', 'WH0292',
                          'WH0293', 'WH0294', 'WH0295', 'WH0296', 'WH0297', 'WH0298', 'WH0299', 'WH0300', 'WH0301',
                          'WH0302', 'WH0303', 'WH0304', 'WH0305', 'WH0306', 'WH0307', 'WH0308', 'WH0309', 'WH0310',
                          'WH0311', 'WH0312', 'WH0313', 'WH0314', 'WH0315', 'WH0316', 'WH0317', 'WH0318',
                          'WH0319', 'WH0320', 'WH0321', 'WH0322', 'WH0323', 'WH0324', 'WH0325', 'WH0326', 'WH0328',
                          'WH0329', 'WH0333']

warehouse_code_sql = ','.join(repr(str(code)) for code in replace_warehouse_code)


# Imc 出库单
def get_delivery(page_from, page_size):
    sql = "SELECT * FROM erp_iom.`delivery_order` where warehouse_delivery_time >='2023-09-01' and warehouse_code in (%s) limit %d,%d" % (
        warehouse_code_sql, page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# imc 出库单详情
def get_delivery_details(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`sub_delivery_order` where delivery_order_id in (%s)" % (orderIds)
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


# 退货应收
def get_return_order(page_from, page_size):
    sql = "SELECT * FROM erp_iom.`return_order` where arrive_time >='2023-09-01' and order_status in (50,60,40,70) limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 退货应收详情
def get_return_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`return_order_detail` where return_order_id in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统退单
def get_refund_order(page_from, page_size):
    sql = "SELECT * FROM oms_ops.`refund_order` where create_time >='2023-09-01'  limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 系统退单子单
def get_refund_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM oms_ops.`sub_refund_order` where refund_id in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 采退，采入
def get_purchase_in_refund(page_from, page_size):
    sql = "SELECT * FROM erp_iom.`stock_order` where billing_time >='2023-09-01' and order_type in (5,6)  and status in (3,13,14) limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 采退，采入
def get_purchase_in_refund_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`stock_order_detail` where stock_order_code in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库
def get_no_order(page_from, page_size):
    sql = "SELECT * FROM erp_iom.`no_order_inbound_order` where arrive_time >='2023-09-01'  limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库子单
def get_no_order_detail(orderIds):
    orderIds = ','.join(repr(str(orderId)) for orderId in orderIds)
    sql = "SELECT * FROM erp_iom.`sub_no_order_inbound_order` where inbound_order_code in (%s)" % (orderIds)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 无单退货入库
def get_purchase_price(page_from, page_size):
    sql = "SELECT * FROM srm_billing.`purchase_price`  limit %d,%d" % (
        page_from, page_size)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


# 复制imc 出库单到 开发环境
def copy_delivery_order(page_from, page_size):
    delivery_order_ids = []
    delivery_orders = get_delivery(page_from, page_size)
    if len(delivery_orders) == 0:
        return False
    delivery_order_insert_sql = []
    for delivery_order in delivery_orders:
        delivery_order_ids.append(delivery_order['delivery_order_id'])
        ls = [(k, v) for k, v in delivery_order.items() if (k != 'revoke_time' and v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.delivery_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    ## 查询详情
    details = get_delivery_details(delivery_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.sub_delivery_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)

    insert_iom(delivery_order_insert_sql)
    return True


def copy_return_order(page_from, page_size):
    return_order_ids = []
    return_orders = get_return_order(page_from, page_size)
    if len(return_orders) == 0:
        return False
    delivery_order_insert_sql = []
    for return_order in return_orders:
        return_order_ids.append(return_order['return_order_id'])
        ls = [(k, v) for k, v in return_order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.return_order (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    ## 查询详情
    details = get_return_order_detail(return_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.return_order_detail (" + keys + ") values (" + values + ");"
        delivery_order_insert_sql.append(sql)
    insert_iom(delivery_order_insert_sql)
    return True


def copy_refund_order(page_from, page_size):
    refund_order_ids = []
    return_orders = get_refund_order(page_from, page_size)
    if len(return_orders) == 0:
        return False
    refund_order_insert_sql = []
    for return_order in return_orders:
        refund_order_ids.append(return_order['refund_id'])
        ls = [(k, v) for k, v in return_order.items() if (k != 'revoke_time' and v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`refund_order` (" + keys + ") values (" + values + ");"
        refund_order_insert_sql.append(sql)
    ## 查询详情
    details = get_refund_order_detail(refund_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into oms_ops.`sub_refund_order` (" + keys + ") values (" + values + ");"
        refund_order_insert_sql.append(sql)
    insert_iom(refund_order_insert_sql)
    return True


def copy_purchase_order(page_from, page_size):
    purchase_order_ids = []
    purchase_orders = get_purchase_in_refund(page_from, page_size)
    if len(purchase_orders) == 0:
        return False
    purchase_order_insert_sql = []
    for purchase_order in purchase_orders:
        purchase_order_ids.append(purchase_order['stock_order_code'])
        ls = [(k, v) for k, v in purchase_order.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore  into erp_iom.`stock_order` (" + keys + ") values (" + values + ");"
        purchase_order_insert_sql.append(sql)
    ## 查询详情
    details = get_purchase_in_refund_detail(purchase_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if ( v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.`stock_order_detail` (" + keys + ") values (" + values + ");"
        purchase_order_insert_sql.append(sql)
    insert_iom(purchase_order_insert_sql)
    return True


def copy_no_order(page_from, page_size):
    no_order_ids = []
    no_orders = get_no_order(page_from, page_size)
    if len(no_orders) == 0:
        return False
    no_order_insert_sql = []
    for no_order in no_orders:
        no_order_ids.append(no_order['inbound_order_code'])
        ls = [(k, v) for k, v in no_order.items() if (k != 'id' and v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.`no_order_inbound_order` (" + keys + ") values (" + values + ");"
        no_order_insert_sql.append(sql)
    ## 查询详情
    details = get_no_order_detail(no_order_ids)
    if len(details) == 0:
        return False
    for detail in details:
        ls = [(k, v) for k, v in detail.items() if (k != 'id' and v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into erp_iom.`sub_no_order_inbound_order` (" + keys + ") values (" + values + ");"
        no_order_insert_sql.append(sql)
    insert_iom(no_order_insert_sql)
    return True


def copy_purchase_price(page_from, page_size):
    purchase_prices = get_purchase_price(page_from, page_size)
    purchase_prices_insert_sql = []
    if len(purchase_prices) == 0:
        return False
    for purchase_price in purchase_prices:
        ls = [(k, v) for k, v in purchase_price.items() if (v is not None)]
        keys = ','.join([i[0] for i in ls])
        values = ','.join(repr(str(i[1])) for i in ls)
        sql = "insert ignore into srm_billing.`purchase_price` (" + keys + ") values (" + values + ");"
        purchase_prices_insert_sql.append(sql)
    insert_iom(purchase_prices_insert_sql)
    return True


def copy_delivery_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        copy_delivery_order((page_num - 1) * page_size, page_size)
        print("copy_delivery_order_loop page:{}".format(page_num))
        page_num += 1


def copy_return_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_return_order_loop page:{}".format(page_num))
        if copy_return_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_purchase_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_order_loop page:{}".format(page_num))
        if copy_purchase_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_refund_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_refund_order_loop page:{}".format(page_num))
        if copy_refund_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_no_order_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_no_order_loop page:{}".format(page_num))
        if copy_no_order((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1


def copy_purchase_price_loop(page_size):
    page_num = 1
    for index in range(1, 100000):
        print("copy_purchase_price_loop page:{}".format(page_num))
        if copy_purchase_price((page_num - 1) * page_size, page_size) is False:
            break
        page_num += 1






if __name__ == '__main__':
    # page_num = 1
    # page_size = 1000
    # for index in range(1, 100000):
    #     copy_delivery_order((page_num - 1) * page_size, page_size)
    #     copy_return_order((page_num - 1) * page_size, page_size)
    #     copy_purchase_order((page_num - 1) * page_size, page_size)
    #     copy_refund_order((page_num - 1) * page_size, page_size)
    #     copy_no_order((page_num - 1) * page_size, page_size)
    #     page_num += 1

    multiprocessing.Process(target=copy_delivery_order_loop, args=(1000,), name='delivery_order').start()
    multiprocessing.Process(target=copy_return_order_loop, args=(1000,), name='return_order').start()
    multiprocessing.Process(target=copy_purchase_order_loop, args=(1000,), name='purchase_order').start()
    multiprocessing.Process(target=copy_refund_order_loop, args=(1000,), name='refund_order').start()
    multiprocessing.Process(target=copy_no_order_loop, args=(1000,), name='no_order').start()

