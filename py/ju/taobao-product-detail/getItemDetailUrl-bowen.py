#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import ItemUrl
import threading, time

tempHeaders = {
    "cookie": "hng=CN%7Czh-CN%7CCNY%7C156; lid=%E6%AE%8B%E5%BF%8D%E7%9A%84%E7%A7%83%E9%B9%AB; enc=AbSivTjEtV9USTxmuSGHR2bQd95SZA9LWNhTdaJPgvUsQOMf%2Fs9soin4pKXSCAEL2yaeVx6Nhl6%2BpeQHLtjOKQ%3D%3D; cna=z2XMGGMVbRoCAXAuRv5JFOGI; pnm_cku822=; cq=ccp%3D1; _m_h5_tk=72c04e50261f3d65969830a48d990c2a_1621506755684; _m_h5_tk_enc=c6382f538d94316d8325601948f0b657; sgcookie=E10072ym0tB5GwnGJXOSIKCFuPili3%2F7Jt0s8sWaxTHenGZvJM26Ubzr4hiOXAH8InP%2BHFs3QP7ymMYY%2BDBcJym%2F2Q%3D%3D; uc3=nk2=0RIgGlUDxx5fJg%3D%3D&vt3=F8dCuw%2B%2FfIrB9q6hbi4%3D&id2=UUppqxL83am2iQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; t=e252601092aa94b1804b5f883734b735; tracknick=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; uc4=id4=0%40U2gjFQous65fn5OU84NxVNM%2BS%2BYm&nk4=0%400yrs34hrgOOnr%2BfuAYME3oMxDpG9; lgc=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; _tb_token_=374393ebbb735; cookie2=1c8660b557e0660f0cc36683a586d14a; xlly_s=1; x5sec=7b2273686f7073797374656d3b32223a223432396565646661656234393931306662326164373636663932313639646334434c617a6e595547454d694970747575316376674d526f4d4d6a49344d7a4d304e4459314e6a73784d4f5868743737352f2f2f2f2f77453d227d; l=eBIE8Mulj-IREAp6BOfZourza779SIRAguPzaNbMiOCP_7fp5LhRW6skRhT9CnGVh68eR3oiiBs_BeYBqIjOov33l6m9qnDmn; isg=BE1NmTQwEYsharWkheQgyztXXGnHKoH8XXZPVo_SjORThm04V3mTzdUQ8BrgRpm0; tfstk=cJJfBgbQyr4fR9ha3nizg3MLubX1ZWef4S_vcBp7vIuIRwtfiN2FRgrcsz2R9g1..",
    "referer": "https://winshare.tmall.com/search.htm?spm=a1z10.3-b-s.w4011-23389038992.279.c2d07652bvojw2&search=y&orderType=defaultSort&pageNo=3&tsearch=y",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}


url = "https://bokuts.tmall.com/i/asynSearch.htm?_ksTS=1622701167227_142&callback=jsonp&mid=w-15421479631-0&wid=15421479631&path=/category.htm&spm=a1z10.5-b-s.w4011-15421479631.165.1b0f2ee5oqkCkY&old_starts=-1m&catId=1141522484&pageNo={pageNo}&search=y&orderType=newOn_desc"


def jsonp(str):
    detailUrl = []
    soup = BeautifulSoup(str, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    for el in find_all:
        detail_url = el.attrs['href']
        detailUrl.append(detail_url)
    return detailUrl




def write_db(detailUrl, page, shopName):
    item_urls = []
    for url in detailUrl:
        if url is not None:
            item_id = re.match(".*?(id=.*&).*", url, re.S).group(1).split('&')[0].replace('id=', '')
            item_url = "http:" + url
            itemUrl = ItemUrl(itemId=item_id, itemUrl=item_url, shopName=shopName)
            item_urls.append(itemUrl)
    dataReptiledb.insertItemUrl(item_urls)


def process_page_list(url, page):
    headers = dataReptiledb.getHeaders()
    headerIndex = 0
    ip_list = dataReptiledb.getIpList()
    getPageNum = page
    while getPageNum < 1000:
        session = HTMLSession()
        print("{thread}线程 开始抓取第 {page}页 {time}".format(thread=threading.current_thread().getName(), page=getPageNum,
                                                       time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        try:
            url_format = url.format(pageNo=getPageNum)
            listResult = session.get(url=url_format, headers=headers[headerIndex],
                                     proxies={'http': random.choice(ip_list)})
            detailUrl = eval(listResult.text)
            detailUrl = list(set(detailUrl))
        except Exception as e:
            # record_file.write(getPageNum)
            print(" %s 线程 抓取第 %d页 发生了一些异常 ： %s" % (threading.current_thread().getName(),getPageNum, e))
            if headerIndex == len(headers) - 1:
                ip_list = dataReptiledb.getIpList()
                headers = dataReptiledb.getHeaders()
                headerIndex = 0
            else:
                ip_list = dataReptiledb.getIpList()
                headerIndex += 1
            # 异常休眠 5秒
            time.sleep(5)
            continue
        else:
            write_db(detailUrl=detailUrl, page=getPageNum, shopName="博库图书专营店")
            time.sleep(random.randint(2, 10))
            # time.sleep(random.randint(10, 20))
            getPageNum += 1


if __name__ == '__main__':
   threading.Thread(target=process_page_list, args=(url, 50,), name="默认排序url").start()
   #threading.Thread(target=process_page_list, args=(url, 1,), name="销量排序url").start()
   #threading.Thread(target=process_page_list, args=(new_url, 50,), name="新品排序url").start()

