#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import ItemUrl, Logger
import threading, time
import constants
import logging

w_xs = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622786529626_126&callback=jsonp127&mid=w-23389038992-0&wid=23389038992&path=/search.htm&spm=a1z10.3-b-s.w4011-23389038992.254.2e277652gIZ829&search=y&keyword=%D0%A1%CB%B5&pageNo=2"

# 综合排序
wenxuan_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1621580321867_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.447.274e7652DYiZdX&orderType=defaultSort&pageNo={pageNo}&tsearch=y"
# 销量排序
wenxuan_sale_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622014477031_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.272.73b67652D3iZj3&pageNo={pageNo}&tsearch=y"
# 新品排序
wenxuan_new_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622014553749_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.288.22787652dTswMv&orderType=newOn_desc&pageNo={pageNo}&tsearch=y"
# 价格排序
wenxuan_price_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622014553749_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.288.22787652dTswMv&orderType=price_asc&pageNo={pageNo}&tsearch=y"

# 干扰 url ,
url = [
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.7.5af911d93V6rF1&ie=utf8&initiative_id=staobaoz_20210219&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E6%AF%8D%E5%A9%B4&suggest=history_1&_input_charset=utf-8&wq=%E6%AF%8D%E5%A9%B4&suggest_query=%E6%AF%8D%E5%A9%B4&source=suggest"
    "https://detail.tmall.hk/hk/item.htm?tbpm=1&spm=a230r.1.14.13.6ebb4793sgX8vA&id=599058260846&cm_id=140105335569ed55e27b&abbucket=17",
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.27.5af911d93V6rF1&q=%E5%AE%B6%E9%A5%B0",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.23.2bdd38bdRsTfHM&id=37236152544&ns=1&abbucket=17",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.66.21d3310cNOJUQi&id=625910266423&ns=1&abbucket=17&sku_properties=21735:44500;122276380:44500;161712509:100189285"
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.9.5af911d98mAeHv&q=%E7%8E%A9%E5%85%B7",
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.22.5af911d98mAeHv&q=%E8%8C%B6%E9%85%92",
    "https://huodong.taobao.com/wow/pm/default/pcgroup/c51a5b?spm=a21bo.21814703.201867-main.34.5af911d98mAeHv&disableNav=YES",
    "https://zc-paimai.taobao.com/list/0___%C9%C2%CE%F7____56968001.htm?spm=a2129.22722945.puimod-zc-focus-2016_3973807750.22.ac263b375GRqhd&auction_source=0&st_param=-1&auction_start_seg=-1",
    "https://item.taobao.com/item.htm?spm=a230r.1.14.103.3afd7408nYsLtv&id=541989840451&ns=1&abbucket=17#detail",
    "https://s.taobao.com/search?q=%E7%83%A4%E7%AE%B1&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306",
    "https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w15914280-18716446969.2.3ec85f3bDI42Bi&id=639769508905&scene=taobao_shop&sku_properties=10004:7195672376",
]
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# logging.basicConfig(filename="./logs/wenxuan-url.log", level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logUtils = Logger(filename='./logs/wenxuan-url.log', level='info')

file_object = open('D:\\爬虫\\TM\\item-detail-url.txt', "a", encoding='utf-8')
record_file = open('D:\\爬虫\\TM\\item-list-record.txt', "a+", encoding='utf-8')


def jsonp(str):
    detailUrl = []
    soup = BeautifulSoup(str, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    for el in find_all:
        detail_url = el.attrs['href']
        detailUrl.append(detail_url)
    return detailUrl


# 将item url 写入 文件
def write(detailUrl, page):
    file_object.write("==================={page}===========".format(page=page) + '\n')
    file_object.flush()
    for url in detailUrl:
        if url is not None:
            file_object.write("http:" + url + '\n')
    file_object.flush()


def write_db(detailUrl, shopName, category):
    item_urls = []
    for url in detailUrl:
        if url is not None:
            item_id = re.match(".*?(id=.*&).*", url, re.S).group(1).split('&')[0].replace('id=', '')
            item_url = "http:" + url
            itemUrl = ItemUrl(itemId=item_id, itemUrl=item_url, shopName=shopName, category=category)
            item_urls.append(itemUrl)
    dataReptiledb.insertItemUrl(item_urls)


# 干扰函数
def disturbUrl(header, ip):
    time.sleep(random.randint(1, 5))
    randint = random.randint(1, 10)
    if randint % 2 == 0:
        session = HTMLSession()
        session.get(url=random.choice(url), headers=header,
                    proxies={'http': ip})
        logUtils.logger.info("执行一次 其他请求 ")


def process_page_list(url, page, category):
    headers = dataReptiledb.getHeaders()
    headerIndex = 0
    ip_list = dataReptiledb.getIpList()
    # 暂时弃用
    getPageNum = page
    # 获取要处理的页数
    page_pool = dataReptiledb.getPageRecords(shopId=1, isSuccess=0, category=category)
    if page_pool is None or len(page_pool) <= 0:
        return
    successPagePool = set()
    while True:
        tempPage = random.choice(page_pool)
        # 再成功的 页数记录中存在
        if tempPage is successPagePool:
            continue
        session = HTMLSession()
        logUtils.logger.info(
            "{thread}线程 开始抓取第 {page}页 {time} ".format(thread=threading.current_thread().getName(), page=tempPage,
                                                      time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        try:
            url_format = url.format(pageNo=tempPage)
            listResult = session.get(url=url_format, headers=headers[headerIndex],
                                     proxies={'http': random.choice(ip_list)})
            listResult.encoding = "utf-8"
            detailUrl = eval(listResult.text)
            detailUrl = list(set(detailUrl))
            logUtils.logger.info(
                "{thread}线程 抓取第 {page}页 结束 {time} url数量{size} ".format(thread=threading.current_thread().getName(),
                                                                       page=tempPage,
                                                                       time=time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                          time.localtime()),
                                                                       size=len(detailUrl)))
            # 干扰函数
            try:
                disturbUrl(headers[headerIndex], random.choice(ip_list))
            except:
                logUtils.logger.error("其他请求发生异常")
                write_db(detailUrl=detailUrl, shopName="新华文轩网络书店", category=category)
                detailUrl.clear()
        except Exception as e:
            # 干扰函数
            disturbUrl(headers[headerIndex], random.choice(ip_list))
            # 更新库 ，，查询新的
            dataReptiledb.updatePageRecordsBatch(successPagePool, 1, 1, category=category)
            # 清空成功 页数池
            successPagePool.clear()
            # 重新查询
            page_pool = dataReptiledb.getPageRecords(1, 0, category=category)
            # record_file.write(getPageNum)
            logUtils.logger.error(" %s 线程 抓取第 %d页 发生了一些异常 ： %s " % (threading.current_thread().getName(), tempPage, e))
            if headerIndex == len(headers) - 1:
                ip_list = dataReptiledb.getIpList()
                headers = dataReptiledb.getHeaders()
                headerIndex = 0
            else:
                ip_list = dataReptiledb.getIpList()
                headerIndex += 1
            # 异常休眠 5秒
            time.sleep(10)
            continue
        else:
            write_db(detailUrl=detailUrl, shopName="新华文轩网络书店", category=category)
            detailUrl.clear()
            successPagePool.add(tempPage)
            if len(successPagePool) >= 5:
                # 更新库 ，，查询新的
                dataReptiledb.updatePageRecordsBatch(successPagePool, 1, 1, category=category)
                # 清空成功 页数池
                successPagePool.clear()
                # 重新查询
                page_pool = dataReptiledb.getPageRecords(1, 0, category=category)
            time.sleep(random.randint(10, 20))
            # time.sleep(random.randint(10, 20))
            getPageNum += 1


if __name__ == '__main__':
    threading.Thread(target=process_page_list, args=(constants.w_xs, 1, "xs"), name="w_xs").start()
    # time.sleep(5)
    # threading.Thread(target=process_page_list, args=(wenxuan_sale_url, 1,), name="销量排序url").start()
    # time.sleep(5)
    # threading.Thread(target=process_page_list, args=(wenxuan_new_url, 1,), name="新品排序url").start()

# file_object.close()
