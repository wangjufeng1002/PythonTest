import  requests
import json
from requests_html import HTMLSession, AsyncHTMLSession
import time
import telnetlib
import os
import threading, time
def split_list(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]
def telnet():
    host = "10.5.24.60"
    port = 20881
    timeout = 100
    with telnetlib.Telnet(host, port, timeout) as session:
        session.write(b'invoke com.dangdang.item.im.pub.apisoa.service.IProductPageSummaryListOutService.queryProductList({"outerSerialId":"", "class":"com.dangdang.item.im.pub.apisoa.model.dto.OuterRequest"},{"productId":"648236532","dataType":"ONLINE", "class":"com.dangdang.item.im.pub.apisoa.model.dto.productlist.ProductQueryRequestDto"})\n')
        time.sleep(2)
        print(session.read_very_eager().decode('gbk'))


def check():
    format_url = "http://10.5.56.79/v2/find_products.php?by=product_id&keys={productId}&expand=1|2&result_format=json"
    write_file = open('C:\\Users\\wangjufeng\\Desktop\\lj\\result', "w")

    with open('D:\\wechat-data\WXWork\\1688851994959441\\Cache\\File\\2021-09\\商品ID')  as file:
        readlines = file.readlines()
        for line in readlines:
            if line is None or len(line) == 0 :
                continue
            line = line.replace("\n","").replace("\t","").replace(" ","")
            session = HTMLSession()
            get = session.get(format_url.format(productId=line))
            json_data = json.loads(get.text)
            if json_data.get("errorCode") == "0":
                core__get = json_data.get("products").get(line).get("core").get("display_status")
                print("{productId}---{status}".format(productId=line,status=core__get))
                write_file.write("{productId}:{status}".format(productId=line,status=core__get)+"\n")
                write_file.flush()
            else:
                write_file.write("{productId}:{status}".format(productId=line, status="NONE") + "\n")
                write_file.flush()

def curl():
    print("curl start")
    url = 'curl -H \'content-type:application/json\' -d  [{productId}]   "http://10.5.25.66:8083/book/change-status/-1?shopId={shopId}&custId=system&innerSerialId=system"'
    url_2 = 'curl -X POST "http://10.5.25.66:8083/itemRecycleBin/delete?shopId={shopId}&custId=system&innerSerialId=system&productIds={productId}"'
    list =[]
    with open('/usr/local/python-workspace/test/105881098909926.txt')  as file:
        readlines = file.readlines()
        for line in readlines:
            split = line.split("\t")
            if split is None or len(split) < 2:
                continue
            shopId = split[0].replace("\n","").replace("\t","").replace(" ","")
            productId = split[1].replace("\n","").replace("\t","").replace(" ","")
            list.append(shopId+"-"+productId)
            # print(productId + shopId +'\n')
            # print("step1: "+str(os.system(url.format(productId=productId,shopId=shopId)))+"\n")
            # print("step2: "+str(os.system(url_2.format(productId=productId, shopId=shopId)))+"\n")
    return list
def curl_thread(list):
    url = 'curl -H \'content-type:application/json\' -d  [{productId}]   "http://10.5.25.66:8083/book/change-status/-1?shopId={shopId}&custId=system&innerSerialId=system"'
    url_2 = 'curl -X POST "http://10.5.25.66:8083/itemRecycleBin/delete?shopId={shopId}&custId=system&innerSerialId=system&productIds={productId}"'
    for data in list :
        split = data.split("-")
        shopId = split[0]
        productId = split[1]
        print("step1: " + str(os.system(url.format(productId=productId, shopId=shopId))) + "\n")
        print("step2: " + str(os.system(url_2.format(productId=productId, shopId=shopId))) + "\n")
if __name__ == '__main__':
    #telnet()
    #check()
    print("main 开始执行")
    list = curl()
    lists = split_list(list, 30000)
    for temp in lists :
        threading.Thread(target=curl_thread,args=(temp,)).start()

    print("main 执行结束")

