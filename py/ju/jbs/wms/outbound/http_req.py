import urllib.request
import urllib
import json
import db


def cancel_plan_order():
    url = "https://wmsdev-aggreg.jiabs.com/aggreg/wms/preparePlan/cancelPlanOrder"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1533732187472879616",
        "Content-Type": "application/json",
        "token": "974a76852770990c1acfa3639cccc358"
    }
    # postdata = urllib.parse.urlencode({"batchOrderIds": ["BC22081003916"]}).json('utf-8')
    jsonData = json.dumps({"batchOrderIds": ["BC22080903895"]}).encode('utf-8')


    order_map = db.get_batch_order_id("BC22080903895")
    for v in order_map:
        try:
            data_dict = {"batchOrderIds": [v['batch_order_id']]}
            jsonData = json.dumps(data_dict).encode('utf-8')
            request = urllib.request.Request(url=url, headers=headers, data=jsonData, method='POST')
            response = urllib.request.urlopen(request)
            print(response.read().decode('utf-8'))
        except:
            pass


if __name__ == '__main__':


    cancel_plan_order()


