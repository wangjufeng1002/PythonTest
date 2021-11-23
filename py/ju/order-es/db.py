#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
import setting
from sshtunnel import SSHTunnelForwarder
import sys
#from dbConnectPool import  POOL

order_basic = None
order_package = None


def initDb(active):
    global server, order_basic, order_package
    if "test" in active:
        server = SSHTunnelForwarder(
            ("10.4.12.122", 22),  # ssh IP和port
            ssh_password="checkos",  # ssh 密码
            ssh_username="checkos",
            remote_bind_addresses=(("myordersbasicdb.idc4", 3306), ("mymt_order_package.db", 3306)))  # 数据库所在的IP和端口
        server.start()

        # order_baisc连接
        order_basic = pymysql.connect(host="127.0.0.1", port=server.local_bind_ports[0], user=setting.ob_use,
                                      password=setting.ob_password, database="orders_basic",
                                      charset="utf8")
        # order-package 连接
        order_package = pymysql.connect(host="127.0.0.1", port=server.local_bind_ports[1], user=setting.op_use,
                                        password=setting.op_password, database="mt_order_package",
                                        charset="utf8")
    elif "prod" in active:
        # order_baisc连接
        order_basic = pymysql.connect(host=setting.ob_host, port=setting.ob_port, user=setting.ob_use,
                                      password=setting.ob_password, database="orders_basic",
                                      charset="utf8", autocommit=True)
        # order-package 连接
        order_package = pymysql.connect(host=setting.op_host, port=setting.op_port, user=setting.op_use,
                                        password=setting.op_password, database="mt_order_package",
                                        charset="utf8", autocommit=True)
    elif "history" in active:
        print()

    else:
        # order_baisc连接
        order_basic = pymysql.connect(host=setting.ob_host_dev, port=setting.ob_port_dev, user=setting.ob_use_dev,
                                      password=setting.ob_password_dev, database="orders_basic",
                                      charset="utf8")
        # order-package 连接
        order_package = pymysql.connect(host=setting.op_host_dev, port=setting.op_port_dev, user=setting.op_use_dev,
                                        password=setting.op_password_dev, database="mt_order_package",
                                        charset="utf8")


def getOrders(id, size):
    # _reConOrderBaisc(order_basic)
    cursor = order_basic.cursor()
    sql = '''select id as id , shop_id as shopId , order_id as orderId, cust_id as custId, status as status, 
    shipping_method_type as shippingMethodType, order_mode as orderMode, order_type as orderType, external_order_id 
    as externalOrderId, receiver_name as receiverName, receiver_mobile_tel as receiverMobileTel, is_presale as 
    isPresale, send_date  as sendDate, order_inner_type as orderInnerType, pay_date as payDate, order_creation_date 
    as orderCreationDate, payment_method_type as paymentMethodType, SHIPPING_LAST_EVENT_DATE as 
    shippingLastEventDate, WAIT_DISTRIBUTION_DATE as waitDistributionDate, WAIT_SHIPPING_RESULT_DATE as 
    waitShippingResultDate, ORDER_CANCEL_DATE as orderCancelDate, from_platform as fromPlatForm, wait_pick_goods_date 
    as waitPickGoodsDate from orders where id >= %d  and order_creation_date >= '2020-01-01' order by id asc  limit 
    %d '''
    cursor.execute(sql % (id, size))

    orders = []
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        order = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            order[columns[j]] = row[j]
        orders.append(order)
    cursor.close()
    return orders


def getOrdersByStartIdEndId(startId, endId, size):
    cursor = order_basic.cursor()
    sql = '''select id as id , shop_id as shopId , order_id as orderId, cust_id as custId, status as status, 
       shipping_method_type as shippingMethodType, order_mode as orderMode, order_type as orderType, external_order_id 
       as externalOrderId, receiver_name as receiverName, receiver_mobile_tel as receiverMobileTel, is_presale as 
       isPresale, send_date  as sendDate, order_inner_type as orderInnerType, pay_date as payDate, order_creation_date 
       as orderCreationDate, payment_method_type as paymentMethodType, SHIPPING_LAST_EVENT_DATE as 
       shippingLastEventDate,
       sync_status as syncStatus,
       WAIT_DISTRIBUTION_DATE as waitDistributionDate, WAIT_SHIPPING_RESULT_DATE as 
       waitShippingResultDate, ORDER_CANCEL_DATE as orderCancelDate, from_platform as fromPlatForm, wait_pick_goods_date 
       as waitPickGoodsDate,last_change_date as lastChangeDate,
       shipping_fee as shippingFeeAmount,
       real_paid_amount as realPaidAmount,
       total as totalAmount,
       payable_amount as payableAmount
       from orders where id >= %d and %d >=id and order_creation_date >= '2020-01-01' order by id asc limit 
       %d '''
    cursor.execute(sql % (int(startId), int(endId), int(size)))

    orders = []
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        order = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            order[columns[j]] = row[j]
        orders.append(order)
    cursor.close()
    return orders


def getOrdersBylastChangeDate(startTime, endTime):
    cursor = order_basic.cursor()
    sql = '''select id as id , shop_id as shopId , order_id as orderId, cust_id as custId, status as status, 
        shipping_method_type as shippingMethodType, order_mode as orderMode, order_type as orderType, external_order_id 
        as externalOrderId, receiver_name as receiverName, receiver_mobile_tel as receiverMobileTel, is_presale as 
        isPresale, send_date  as sendDate, order_inner_type as orderInnerType, pay_date as payDate, order_creation_date 
        as orderCreationDate, payment_method_type as paymentMethodType, SHIPPING_LAST_EVENT_DATE as 
        shippingLastEventDate, WAIT_DISTRIBUTION_DATE as waitDistributionDate, WAIT_SHIPPING_RESULT_DATE as 
        waitShippingResultDate, ORDER_CANCEL_DATE as orderCancelDate, from_platform as fromPlatForm, wait_pick_goods_date 
        as waitPickGoodsDate from orders where last_change_date >= '%s' and '%s'>= last_change_date
        and order_creation_date >= '2020-01-01' '''
    cursor.execute(sql % (startTime, endTime))

    orders = []
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        order = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            order[columns[j]] = row[j]
        orders.append(order)
    cursor.close()
    return orders


def getOrdersByIntervalLastChangeDate(min):
    cursor = order_basic.cursor()
    sql = '''select id as id , shop_id as shopId , order_id as orderId, cust_id as custId, status as status, 
        shipping_method_type as shippingMethodType, order_mode as orderMode, order_type as orderType, external_order_id 
        as externalOrderId, receiver_name as receiverName, receiver_mobile_tel as receiverMobileTel, is_presale as 
        isPresale, send_date  as sendDate, order_inner_type as orderInnerType, pay_date as payDate, order_creation_date 
        as orderCreationDate, payment_method_type as paymentMethodType, SHIPPING_LAST_EVENT_DATE as 
        shippingLastEventDate, WAIT_DISTRIBUTION_DATE as waitDistributionDate, WAIT_SHIPPING_RESULT_DATE as 
        waitShippingResultDate, ORDER_CANCEL_DATE as orderCancelDate, from_platform as fromPlatForm, wait_pick_goods_date 
        as waitPickGoodsDate from orders where last_change_date >= date_sub(NOW(), interval %d DAY)
        and order_creation_date >= '2020-01-01' '''
    cursor.execute(sql % (min))

    orders = []
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        order = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            order[columns[j]] = row[j]
        orders.append(order)
    cursor.close()
    return orders


def getOrderMax():
    sql = "select max(id) as id from orders"
    cursor = None
    try:
        cursor = order_basic.cursor()
        cursor.execute(sql)
        fetchall = cursor.fetchall()
    finally:
        cursor.close()

    ##返回最大的ID
    return fetchall[0][0]


def getOrderCustDetailByCustId(custId):
    sql = "select cust_id as custId,nick_name as custNickName from order_cust_detail where cust_id = %s "
    executeSql = sql % custId
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    result = cursor.fetchall()
    custs = []
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        cust = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            cust[columns[j]] = row[j]
        custs.append(cust)
    cursor.close()
    return custs


def getOrderCustDetail(custIds):
    sqlParam = ",".join(custIds)
    sql = "select cust_id as custId,nick_name as custNickName from order_cust_detail where cust_id in (%s)"
    executeSql = sql % sqlParam
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    result = cursor.fetchall()
    custs = {}
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        cust = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        custId = None
        for j in range(len(columns)):
            cust[columns[j]] = row[j]
            if "custId" in columns[j]:
                custId = row[j]
        custs[custId] = cust
    cursor.close()
    return custs


def getOrderLabel(orderId):
    sql = '''select 
        label  as orderLable,
        label_comment as orderLableComment
        from order_label where ref_id= %d order by creation_date DESC'''
    executeSql = sql % orderId
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    return getResult(cursor)


def getResult(cursor):
    orderLabels = []
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        orderLabel = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            orderLabel[columns[j]] = row[j]
        orderLabels.append(orderLabel)
    return orderLabels


def getRefundAudits(orderId):
    '''SELECT
        order_id as _id,
        concat('{\"sourceId\":\"',source_id,'\",','\"isAgree\":\"',is_agree,'\",','\"refundSource\":\"',refund_source,'\"}') as refundAduits
    FROM refund_audit'''
    sql = ''' select source_id as sourceId ,
                is_agree as isAgree,
                refund_source as refundSource
              from refund_audit where order_id = %d 
         '''
    executeSql = sql % orderId
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    return getResult(cursor)


def getPackage(orderId):
    """SELECT
        order_id as _id,
        order_id as orderId,
        concat('{\"expressNo\":\"',express_no,'\",','\"expressCompany\":\"',REPLACE(express_company, '\\\"', '\\\\\"'),'\"}') as expresses
    FROM order_package"""
    sql = "select express_no as expressNo , express_company as expressCompany from order_package where order_id = %d"
    executeSql = sql % orderId
    cursor = order_package.cursor()
    cursor.execute(executeSql)
    return getResult(cursor)


def getProduts(orderId):
    sql = "select product_id as productId , product_name as productName from order_items where order_id = %d"
    executeSql = sql % orderId
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    return getResult(cursor)

# custIds = []
# custIds.append("19821166")
# custs = getOrderCustDetail(custIds)
# audits = getRefundAudits(5563528267)
# print(audits)

# order_max = getOrderMax()
# print(order_max)

def getGroupCount(day):
    #initDb("prod")
    sql = '''select count(1) num ,DATE_FORMAT(order_creation_date,'%Y-%m-%d %H') as time from orders 
where order_creation_date >= '{day}' GROUP BY time'''
    try:
        order_basic.ping(reconnect=True)
        cursor = order_basic.cursor()
        cursor.execute(sql.format(day=day))
        result = getResult(cursor)
    except:
        cursor.close()
        order_basic.rollback()
    else:
        cursor.close()
        order_basic.commit()
        return result
def getGroupDayCount(start_day,end_day):
    #initDb("prod")
    sql = '''select count(1) num ,DATE_FORMAT(order_creation_date,'%Y-%m-%d') as time from orders 
where order_creation_date >= '{start_day}' and '{end_day}'>=order_creation_date GROUP BY time'''
    try:
        order_basic.ping(reconnect=True)
        cursor = order_basic.cursor()
        cursor.execute(sql.format(start_day=start_day,end_day=end_day))
        result = getResult(cursor)
    except:
        cursor.close()
        order_basic.rollback()
    else:
        cursor.close()
        order_basic.commit()
        return result

def getOrderId(date1,date2):
    #initDb("prod")
    sql = '''select * from orders 
    where order_creation_date >= '{date1}' and '{date2}' >= order_creation_date '''
    try:
        order_basic.ping(reconnect=True)
        cursor = order_basic.cursor()
        cursor.execute(sql.format(date1=date1,date2=date2))
        result = getResult(cursor)
    except Exception as e:
        cursor.close()
        order_basic.rollback()
    else:
        cursor.close()
        order_basic.commit()
        return result

def getOrderShareAmouns(orderId):
    sql = ''' select share_amount as shareAmount ,
                IFNULL(rate_partner,0) as ratePartner,
                share_type as shareType,
                cash_type  as cashType,
              from order_apport_amount where order_id = %d 
         '''
    executeSql = sql % orderId
    cursor = order_basic.cursor()
    cursor.execute(executeSql)
    return getResult(cursor)


def getIdByOrderId(orderId):
    connection = POOL.connection()
    try:
        sql = "select id from orders where order_id = '%s' limit 10000"
        executeSql = sql % orderId
        cursor = connection.cursor()
        cursor.execute(executeSql)
        result = cursor.fetchall()
        custs = []
        description = cursor.description
        columns = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            cust = {}
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                cust[columns[j]] = row[j]
            custs.append(cust)
        cursor.close()
        return custs
    finally:
        connection.close()
