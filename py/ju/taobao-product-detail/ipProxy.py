import urllib
from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb

ip_url = "https://www.kuaidaili.com/free/inha/{page}/"
# ip_url_2 = "http://www.66ip.cn/{page}.html"
ip_url_2 = "http://www.66ip.cn/areaindex_{area}/{page}.html"
ip_url_3 = "https://ip.jiangxianli.com/?page={page}"

check_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1621580321867_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.447.274e7652DYiZdX&orderType=defaultSort&pageNo=2&tsearch=y"


def checkip(ip_list):
    for ip in ip_list:
        try:
            proxy_host = "https://" + ip
            proxy_temp = {"https": proxy_host}
            res = urllib.urlopen(check_url, proxies=proxy_temp).read()
        except Exception as e:
            ip_list.remove(ip)
            continue
    return ip_list


def getIp():
    ips = []
    for i in range(1, 500):
        print("开始爬取第{page} 页".format(page=i))
        time.sleep(2)
        session = HTMLSession()
        try:
            result = session.get(ip_url.format(page=i))
        except Exception as e:
            print("爬取 ip发生一些异常", e)
            break
        html = BeautifulSoup(result.text, features='html.parser')
        tbody = html.find(name="tbody")
        if tbody is None:
            break
        iter = tbody.children
        for item in iter:
            if isinstance(item, str):
                continue
            ip = item.find_all(name="td", attrs={"data-title": "IP"})
            port = item.find_all(name="td", attrs={"data-title": "PORT"})
            if ip is None or port is None:
                continue
            ip = ip[0].text + ":" + port[0].text
            ips.append(ip)
    ips = checkip(ips)
    dataReptiledb.insertIps(ips)
    return ips


header = {
    "cookie": "Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1621590739,1622010372; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1622010376",
    "referer": "http://www.66ip.cn/areaindex_1/1.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate"

}


# http://www.66ip.cn/areaindex_1/2.html
def getIp_2():
    ips = []
    for areaIndex in range(1, 34):
        j = 0
        while j < 500:
            print("开始爬取第{page} 页".format(page=j))
            contents = []
            try:
                session = HTMLSession()
                result = session.get(url=ip_url_2.format(page=j, area=areaIndex), headers=header)
                result.encoding = result.apparent_encoding
                html = BeautifulSoup(result.text, features='html.parser')
                table_ = html.find_all(name="table")[2]
                contents = table_.contents
                if len(contents) <=1:
                    break
                j+=1
            except:
                print("发生了一点异常")
                break
            for i in range(len(contents)):
                if i < 3:
                    continue
                cont = contents[i]
                if isinstance(cont, str):
                    continue
                ip = cont.contents[0].text
                port = cont.contents[1].text
                ips.append(ip + ":" + port)
        ips = checkip(ips)
        dataReptiledb.insertIps(ips)
    return ips


def getIp_3():
    ips = []
    for i in range(1, 100):
        session = HTMLSession()
        result = session.get(ip_url_3.format(page=i))
        html = BeautifulSoup(result.text, features='html.parser')
        find_all = html.find_all(name="table", attrs={"class": "layui-table"})
        print(find_all)


def wirteIpToText(availableIps):
    file_object = open('D:\\爬虫\\TM\\ip.txt', "a", encoding='utf-8')
    for ip in availableIps:
        file_object.write(ip + '\n')
    file_object.flush()

if __name__ == '__main__':
    #getIp()
    getIp_2()

# ips = getIp()
# print(ips)
# availableIps = checkip(ips)
# wirteIpToText(availableIps=availableIps)

# ips = ['118.187.58.34:53281',
#        '218.249.45.162:52316',
#        '61.135.155.82:443',
#        '123.118.0.27:8118',
#        '103.233.152.140:8080',
#        '114.249.115.204:9000',
#        '60.207.197.18:80',
#        '106.14.198.6:8080',
#        '119.57.156.90:53281',
#        '124.205.155.157:9090',
#        '60.194.240.25:80',
#        '124.192.219.35:80',
#        '103.233.154.242:8080',
#        '106.14.198.6:8080',
#        '61.135.155.82:443',
#        '103.233.154.242:8080',
#        '60.195.132.8:80',
#        '124.205.155.152:9090',
#        '118.144.26.8:80',
#        '124.205.155.148:9090',
#        '103.233.152.140:8080',
#        '61.135.155.82:443',
#        '159.226.21.115:80'
#        ]
# print(checkip(ips))
