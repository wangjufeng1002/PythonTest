from elasticsearch import helpers
import db
import json
import time
import datetime
import threading, time
import EsConfig
import requests
import schedule
from LoggerEntity import Logger
logUtils = Logger(filename='./logs/dataMonitor.log', level='info')
index = "order-index"
inde_type = "order_query_key"
# 初始化es db
EsConfig.initEs("prod")
db.initDb("test")
#nohup python DataMonitor.py  >> logs/nohup-dataMonitor.log 2>&1 &
def process():
    logUtils.logger.info("按小时监控任务启动===%s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    global error
    body = '''{
                  "size": 0,
                  "query": {
                    "bool": {
                       "filter": {
                        "range": {
                          "orderCreationDate": {
                                  "from": "%s",
                                  "to": "%s",
                                  "include_lower": true,
                                  "include_upper": true,
                                  "boost": 1
                          }
                        }
                      }
                    }
                  }, 
                  "aggs": {
                    "groupDate": {
                      "date_histogram": {
                        "field": "orderCreationDate",
                        "interval": "hour",
                        "format": "yyyy-MM-dd HH"
                      }
                    }
                  }
                }'''
    now = time.localtime()
    #day = "2021-07-16"
    day = time.strftime('%Y-%m-%d', now)
    es_search = EsConfig.es.search(index=index, doc_type=inde_type, body=body % (day + " 00:00:00", day + " 23:59:59"))
    result_list = es_search.get('aggregations').get('groupDate').get('buckets')
    es_result_map = {}
    for result in result_list:
        es_result_map[result.get("key_as_string")] = result.get("doc_count")
    sql_result_map = {}
    sql_group_count = db.getGroupCount(day)
    for result in sql_group_count:
        sql_result_map[result.get("time")] = result.get("num")
    data = '''{{
    "msgtype": "text",
    "text": {{
        "content": "{desc}",
        "mentioned_mobile_list":["15091751738","18702925292"]
    }}
}}'''
    error = ""
    for (key, val) in sql_result_map.items():
        #排除当前小时
        if key == time.strftime('%Y-%m-%d %H',time.localtime()):
            continue
        if es_result_map.get(key) != val:
            error += "时间: " + key + "db数量: " + str(val) +","+"es数量: "+str(es_result_map.get(key)) + "\n"
    if error.isspace() == False and len(error) > 0 and error.strip() != '':
        error = "es 数据量与 db 中出现不一致请核实: \n" + error + "请关闭 apollo 配置 query.orderListPc.es.switch=false \n"
        print(error)
        # requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7e03d9fc-8eb9-4815-9d97-688f67aea21b',
        #               data=data.format(desc=error).encode("UTF-8"),
        #               headers={'Content-Type': 'application/json; charset=UTF-8'})
    else:
        logUtils.logger.info("数据正常===%s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))

def process_2():
    body = '''{
                     "size": 0,
                     "query": {
                       "bool": {
                          "filter": {
                           "range": {
                             "orderCreationDate": {
                                     "from": "%s",
                                     "to": "%s",
                                     "include_lower": true,
                                     "include_upper": true,
                                     "boost": 1
                             }
                           }
                         }
                       }
                     }, 
                     "aggs": {
                       "groupDate": {
                         "date_histogram": {
                           "field": "orderCreationDate",
                           "interval": "day",
                           "format": "yyyy-MM-dd"
                         }
                       }
                     }
                   }'''
    logUtils.logger.info("按天监控任务启动===%s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    start_day = "2021-03-01"+" 00:00:00"
    end_day= (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d") +  " 23:59:59"
    es_search = EsConfig.es.search(index=index, doc_type=inde_type, body=body % ( start_day, end_day))
    result_list = es_search.get('aggregations').get('groupDate').get('buckets')
    es_result_map = {}
    for result in result_list:
        es_result_map[result.get("key_as_string")] = result.get("doc_count")
    sql_result_map = {}
    sql_group_count = db.getGroupDayCount(start_day,end_day)
    for result in sql_group_count:
        sql_result_map[result.get("time")] = result.get("num")
    data = '''{{
    "msgtype": "text",
    "text": {{
        "content": "{desc}",
        "mentioned_mobile_list":["15091751738","18702925292"]
        }}
    }}'''
    error = ""
    for (key, val) in sql_result_map.items():
        #排除当前小时
        if key == time.strftime('%Y-%m-%d %H',time.localtime()):
            continue
        if es_result_map.get(key) != val:
            error += "时间: " + key + " db数量: " + str(val) + "," + " es数量: " + str(es_result_map.get(key)) + "\n"
    if error.isspace() == False and len(error) > 0 and error.strip() != '':
        error = "es 数据量与 db 中出现不一致请核实: \n" + error + "请关闭 apollo 配置 query.orderListPc.es.switch=false \n"
        requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7e03d9fc-8eb9-4815-9d97-688f67aea21b',
                      data=data.format(desc=error).encode("UTF-8"),
                      headers={'Content-Type': 'application/json; charset=UTF-8'})
        print(error)
    else:
        logUtils.logger.info("按天监控数据正常===%s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
def process_3():
    body = '''
    {   
        "size": 1000000,
        "query": {
        "bool": {
          "filter": [
            {
              "range": {
                "orderCreationDate": {
                  "from": "%s",
                  "to": "%s",
                  "include_lower": true,
                  "include_upper": true,
                  "boost": 1
                }
              }
            }
          ]
        }
      }
    }'''

    orderIds=set()
    startDay = "2021-10-18"+" 14:00:00"
    endDay = "2021-10-18" +" 14:59:59"
    sql_group_count = db.getOrderId(startDay,endDay)
    es_search = EsConfig.es.search(index=index, doc_type=inde_type, body=body % (startDay, endDay))
    for hit in es_search['hits']['hits']:
       orderIds.add(int(hit["_id"]))
    for result in sql_group_count:
       if result.get("order_id") not  in orderIds:
           print(result.get("order_id"))
           requests.get("http://10.5.25.80:10001/syncOrder?orderId="+ str(result.get("order_id")))
           #

    #print(es_search)
if __name__ == '__main__':
    # print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    #按小时统计
    #process()
    #process_2()
    process_3()
    # #按天统计
    # process_2()
    # schedule.every(20).minutes.do(process)
    # schedule.every(30).minutes.do(process_2)
    # while True:
    #     schedule.run_pending()


#print(time.strftime('%Y-%m-%d %H:%m:%S',time.localtime()))
    #process()
    #process_3()
