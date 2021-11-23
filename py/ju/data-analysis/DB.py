import pymysql

# order_baisc连接
order_basic = pymysql.connect(host="192.168.47.210", port="3306", user="root",
                              password="123456", database="data-scraping",
                              charset="utf8")