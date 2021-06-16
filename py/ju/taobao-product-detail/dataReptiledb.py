#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
from entity import Book, ItemUrl


def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


def getHeaders():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    headers = []
    cursor = conn.cursor()
    execute = cursor.execute("select `cookie`,`referer`,`user-agent` from headers")
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    df = pd.DataFrame(columns=columns)
    for i in range(len(result)):
        head = {}
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            head[columns[j]] = row[j]
        headers.append(head)

    cursor.close()
    return headers


def insertDetailPrice(book):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "INSERT INTO `data-reptile`.`book`" \
          " ( `tm_id`, `book_name`, `book_isbn`, `book_auther`, `book_price`, `book_fix_price`, `book_prom_price`, `book_prom_price_desc`, " \
          "`book_active_desc`, `shop_name`,`book_prom_type`,`book_active_start_time`,`book_active_end_time`) " \
          "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " \
          "ON DUPLICATE KEY " \
          "UPDATE " \
          "book_name= '%s' " \
          ", book_isbn= '%s' " \
          ", book_auther = '%s' " \
          ", book_price = '%s'" \
          ", book_fix_price = '%s'" \
          ", book_prom_price = '%s'" \
          ", book_prom_price_desc = '%s'" \
          ", book_active_desc = '%s'" \
          ", shop_name = '%s'" \
          ", book_prom_type = '%s'" \
          ", book_active_start_time = '%s'" \
          ", book_active_end_time = '%s'" \
          % (book.getTmId(), book.getName(), book.getIsbn(), book.getAuther(), book.getPrice(), book.getFixPrice(),
             book.getPromotionPrice(), book.getPromotionPriceDesc(), book.getActiveDescStr(), book.getShopName(),
             book.getPromotionType(), book.getActiveStartTime(), book.getActiveEndTime(),

             book.getName(), book.getIsbn(), book.getAuther(), book.getPrice(), book.getFixPrice(),
             book.getPromotionPrice(), book.getPromotionPriceDesc(), book.getActiveDescStr(), book.getShopName(),
             book.getPromotionType(), book.getActiveStartTime(), book.getActiveEndTime(),
             )
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("数据库插入Price发生异常 {}", e)
        conn.rollback()
    finally:
        cursor.close()


def insertIp(ip):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "INSERT INTO `data-reptile`.`ip_pool` (`ip`) VALUES ('%s') ON DUPLICATE KEY UPDATE ip = '%s'" % (ip, ip)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("数据库插入ip发生异常 {}", e)
        conn.rollback()
    finally:
        cursor.close()


def insertIps(ips):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    sql = "INSERT INTO `data-reptile`.`ip_pool` (`ip`) VALUES ('%s') ON DUPLICATE KEY UPDATE ip = ip"
    cursor = conn.cursor()
    for ip in ips:
        exeSql = sql % ip
        try:
            cursor.execute(exeSql)
            conn.commit()
        except Exception as e:
            print("数据库插入ip发生异常 {}", e)
            conn.rollback()
    cursor.close()


def getIpList():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select ip from `ip_pool`"
    try:
        cursor.execute(sql)
        fetchall = cursor.fetchall()
        ips = []
        for ip in list(fetchall):
            try:
                ips.append(ip[0])
            except:
                print("异常ip %s" % ip)
        return ips
    except Exception as e:
        print("查询ip发生异常 {}", e)
    finally:
        cursor.close()


def insertItemUrl(itemUrls):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "INSERT INTO `data-reptile`.`item_url` ( `item_id`, `item_url`, `shop_name`) VALUES ( '%s', '%s', '%s')" \
          " ON DUPLICATE KEY UPDATE item_id = '%s' ,item_url = '%s',shop_name = '%s' "

    for itemUrl in itemUrls:
        exeSql = sql % (
            itemUrl.itemId, itemUrl.itemUrl, itemUrl.shopName, itemUrl.itemId, itemUrl.itemUrl, itemUrl.shopName
        )
        try:
            cursor.execute(exeSql)
            conn.commit()
        except Exception as e:
            print("数据库插入 item_url 发生异常 {}", e)
            conn.rollback()
    cursor.close()


def getItemUrl(page, page_size):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    if page is None or page <= 0:
        page = 1
    if page_size is None:
        page_size = 1000
    offset = (page - 1) * page_size
    sql = "select item_id as itemId,item_url as itemUrl,shop_name as shopName from `item_url` where is_success != 1  order by update_time ASC limit %d,%d"
    e_sql = sql % (offset, page_size)
    execute = cursor.execute(e_sql)
    if execute <= 0:
        return None
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    itemUrlObjs = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        itemUrl = {}
        itemUrlObj = ItemUrl(itemId=None, itemUrl=None, shopName=None)
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            itemUrl[columns[j]] = row[j]
        dict2obj(itemUrlObj, itemUrl)
        itemUrlObjs.append(itemUrlObj)
    return itemUrlObjs


def updateSuccessFlag(flag, itemId):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "update  `item_url` set is_success = '%d' where item_id = '%s' " % (flag, itemId)
    try:
        execute = cursor.execute(sql)
        conn.commit()
    except:
        conn.close()
        print("更新 item_url 失败")
        return False
    if execute <= 0:
        return False
    else:
        conn.close()
        return True


def getPageIndex(page, shopId, isSuccess):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select page_index  from `page_record` where  page_index = %d and shop_id = %d and is_success = %d"
    cursor.execute(sql % (page, shopId, isSuccess))
    fetchall = cursor.fetchall()
    pageIndex = []
    for page in list(fetchall):
        try:
            pageIndex.append(page[0])
        except:
            print("page_index %s" % page)
    return pageIndex


def getPageRecords(shopId, isSuccess,category):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select page_index  from `page_record` where  shop_id = %d and is_success = %d and category ='%s'"
    cursor.execute(sql % (shopId, isSuccess,category))
    fetchall = cursor.fetchall()
    pageIndex = []
    for page in list(fetchall):
        try:
            pageIndex.append(page[0])
        except:
            print("page_index %s" % page)
    return pageIndex


def updatePageRecords(page, shopId, isSuccess,category):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "update `page_record` set is_success = %d  where page_index = %d and shop_id = %d and category='%s'"
    cursor.execute(sql % (isSuccess, page, shopId,category))
    conn.commit()
    cursor.close()


def updatePageRecordsBatch(page, shopId, isSuccess,category):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "update `page_record` set is_success = %d  where page_index = %d and shop_id = %d and category='%s'"

    for tempPage in page:
        cursor.execute(sql % (isSuccess, tempPage, shopId,category))

    conn.commit()
    cursor.close()


def insertPageIndex(page, shopId, isSuccess,category):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="data-reptile",
                           charset="utf8")
    sql = "insert into `page_record`(page_index,shop_id,is_success,category) values(%d,%d,%d,'%s')"
    cursor = conn.cursor()
    cursor.execute(sql % (page, shopId, isSuccess,category))
    conn.commit()
    cursor.close()


# s = [10000,10000000,10000]
# updatePageRecordsBatch(s,1,0)
# #
if __name__ == '__main__':
    for i in range(1, 1001):
        insertPageIndex(i, 1, 0, 'xs')
    #print(getItemUrl(page=100, page_size=1000))
    #print(getIpList())

