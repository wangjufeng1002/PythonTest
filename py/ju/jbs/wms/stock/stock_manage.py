# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib
from toollib.guid import SnowFlake

snow = SnowFlake()
def stock_add():
    param = {}
    param['outStockOrderId'] = snow.gen_uid()
    param['actionFrom'] = 'PURCHASE_INBOUND'
    param['remark'] = '测试'
    param['sourceType'] = 'WEB'
    param['operator'] = 'wjf'

    detail= {}
    detail['warehouseCode'] = 'WH0001'
    detail['warehouseLocationCode'] = 'WJF-KS'
    detail['batchNo']='20250318'
    detail['goodsCode'] = 'JBS-ZNLJT-810-DCK'
    detail['addStockNum'] = 10
    param_details = []
    param_details.append(detail)

    param['stockDetails']= param_details

    param_json = json.dumps(param).encode('utf-8')


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1533732187472879616",
        "Content-Type": "application/json",
        "token": "974a76852770990c1acfa3639cccc358"
    }
    url = "http://192.168.1.174:11101/stockManager/addStock"
    request = urllib.request.Request(url=url, headers=headers, data=param_json, method='POST')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))


if __name__ == '__main__':
    stock_add()