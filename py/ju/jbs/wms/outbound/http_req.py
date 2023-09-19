import random
import urllib.request
import urllib
import json
import db
import multiprocessing
import numpy as np


def cancel_order_process(headers, v):
    url = "https://wmsdev-aggreg.jiabs.com/aggreg/wms/preparePlan/cancelPlanOrder"
    data_dict = {"batchOrderIds": [v['batch_order_id']]}
    jsonData = json.dumps(data_dict).encode('utf-8')
    request = urllib.request.Request(url=url, headers=headers, data=jsonData, method='POST')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))


def cancel_plan_order():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1533732187472879616",
        "Content-Type": "application/json",
        "token": "974a76852770990c1acfa3639cccc358"
    }
    order_map = db.get_batch_order_id("BC22083104247")
    for v in order_map:
        try:
            multiprocessing.Process(target=cancel_order_process, args=(headers, v)).start()
        except:
            pass


def query_delivery_order_agg():
    warehouse_local_codes = list(map(lambda x: x['warehouse_location_code'], db.get_warehouse_localtion("WH0001")))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1533732187472879616",
        "Content-Type": "application/json",
        "token": "974a76852770990c1acfa3639cccc358"
    }
    url = "https://wmsdev-aggreg.jiabs.com/aggreg/wms/deliverOrder/searchDeliveryOrderPage"
    # url = "http://127.0.0.1/aggreg/wms/deliverOrder/searchDeliveryOrderPage"
    # url = "https://dmsaggreg.jiabs.com/aggreg/wms/deliverOrder/searchDeliveryOrderPage"
    choice = list(np.random.choice(warehouse_local_codes, size=3000))
    data_dict = {"warehouseLocationCodes": choice, "warehouseCode": "WH0001"}
    jsonData = json.dumps(data_dict).encode('utf-8')
    request = urllib.request.Request(url=url, headers=headers, data=jsonData, method='POST')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))


def query_delivery_order_agg_test():
    warehouse_local_codes = list(map(lambda x: x['warehouse_location_code'], db.get_warehouse_localtion("WH0001")))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1539151295396986880",
        "Content-Type": "application/json",
        "token": "179a8cee5135703060fa79ac531ca2e0",
        "currentpageresourceid": "1535153950995734529"
    }
    url = "https://dmsaggreg.jiabs.com/aggreg/wms/deliverOrder/searchDeliveryOrderPage"
    choice = list(np.random.choice(warehouse_local_codes, size=1020))
    data_dict = {"warehouseLocationCodes": choice, "warehouseCode": "WH0001"}
    jsonData = json.dumps(data_dict).encode('utf-8')
    request = urllib.request.Request(url=url, headers=headers, data=jsonData, method='POST')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))


def query_delivery_order_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1533732187472879616",
        "Content-Type": "application/json",
        "token": "974a76852770990c1acfa3639cccc358"
    }
    url = "http://127.0.0.1:10011/deliveryOrder/searchDeliveryOrderPage"
    goods_codes = list(map(lambda x: x['goods_code'], db.get_product_codes(10000)))
    data_dict = {"allMatchGoodsCodes": goods_codes, "warehouseCode": "WH0001"}
    jsonData = json.dumps(data_dict).encode('utf-8')
    request = urllib.request.Request(url=url, headers=headers, data=jsonData, method='POST')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))


def query_es_test():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "Authorization": "Basic ZWxhc3RpYzpzWndGc1p1eU13Xng1dQ==",
        "Content-Type": "application/json",
    }
    #url = "http://192.168.1.201:9200/wms_delivery_order/_search"
    url = "http://es-cn-7mz255aof00025bt6.public.elasticsearch.aliyuncs.com:9200/wms_delivery_order/_search"
    query_json = '''
                     {
                        "query": {
                         "bool": {
                          "must": [
                            {
                             "terms_set": {
                                  "goodsCodes": {
                                    "terms": [ "JBS", "ABC"],
                                    "minimum_should_match_field": "goodsSpecies"
                                  }
                                }
                            }
                          ],
                          "adjust_pure_negative": true,
                          "boost": 1
                        }
                      }
                    }
                    '''
    query_json_obj = json.loads(query_json)
    query_json_obj["query"]["bool"]["must"][0]["terms_set"]["goodsCodes"]["terms"] = list(map(lambda x: x['goods_code'], db.get_product_codes(5000)))

    #request = urllib.request.Request(url=url, headers=headers, data=query_json.encode('utf-8'), method='POST')
    request = urllib.request.Request(url=url, headers=headers, data=json.dumps(query_json_obj).encode('utf-8'), method='POST')
    try:
        response = urllib.request.urlopen(request)
        print(json.load(response))
    except:
        pass



if __name__ == '__main__':
    query_delivery_order_agg()
    #query_delivery_order_agg_test()
    #query_es_test()
    #query_delivery_order_stock()