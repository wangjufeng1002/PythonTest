# coding=utf-8
from py.ju.reptile.entity import Data
import urllib.request
from requests_html import HTMLSession, AsyncHTMLSession
import chardet
import base64
import re
import ssl
import datetime
import threading


context = ssl._create_unverified_context()
rootUrl = 'aHR0cHM6Ly93d3cuYnRndy54eXovbGlzdC5waHA/Y2xhc3M9Z3VvY2hhbiZwYWdlPQ=='
rootUrl = 'https://www.266532.xyz/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
''' 防止403'''
opener = urllib.request.build_opener()
urllib.request.install_opener(opener)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')]


def process(page,limit):
    pageIndex = page
    endIndex =  pageIndex+limit
    while pageIndex <= endIndex:
        print("开始处理 %d 页" % pageIndex)
        session = HTMLSession()
        detailResponse = session.get(url=rootUrl + 'list.php?class=guochan&page=' + str(pageIndex), headers=headers, proxies={'http://': random.choice(ipList)})
        #page1 = urllib.request.Request(rootUrl + 'list.php?class=guochan&page=' + str(pageIndex), headers=headers)
        page = urllib.request.urlopen(page1, context=context)  # 打开网页
        htmlCode = page.read()  # 获取网页源代码
        # print(chardet.detect(htmlCode))  # 打印返回网页的编码方式
        # print(htmlCode.decode('utf-8'))  # 打印网页源代码
        print("开始处理============================================================================")
        htmlCode = htmlCode.decode('utf-8')
        clan_rows = re.findall(r'\<li.*\>', htmlCode, re.M | re.I)  # 清洗 <> 开始
        datas = []
        for row in clan_rows:
            try:
                if 'movie' in row and '[' in row and ']' in row:
                    date = re.findall(r'\[.*\]', row, re.M | re.I)
                    if date is None:
                        continue
                    uri = re.findall(r'href="/movie\.php\?class=guochan&id=\d*"', row)
                    if uri is None or len(uri) == 0:
                        continue
                    dec = re.findall(r'd\(\'.*\)', row)
                    # print(date[0] + '+' + uri[0] + '+' + dec[0])
                    url = uri[0].replace('href="', '').replace('"', '')
                    dec = dec[0].replace('d(\'', '').replace('\'))', '')
                    # print(date[0] + ' ' + url + ' ' + dec)
                    data = Data(date[0], dec, url)
                    datas.append(data)
            except:
                print("exception row=%s" % (row))
                pass
                # print(row)
        ##提取有用字符
        print(len(datas))
        for value in datas:
            try:
                id = value.url.replace('/movie\.php\?class=guochan&id=', "").replace(".html", "").replace(
                    "/movie.php?class=guochan&id=", "")
                page1 = urllib.request.Request(rootUrl + 'download.php?class=guochan&id=' + id, headers=headers)
                page = urllib.request.urlopen(page1, context=context)  # 打开网页
                htmlCode = page.read()  # 获取网页源代码
                # print(chardet.detect(htmlCode))  # 打印返回网页的编码方式
                # print(htmlCode.decode('utf-8'))  # 打印网页源代码
                print("============================下载中================================================")
                htmlCode = htmlCode.decode('utf-8')
                url = re.findall(r'href=\'/torrent/.*\.torrent\'', htmlCode)
                url = url[0].replace("href=\'", '').replace("\'", '')
                #
                # pageFile = open('pageCode.txt', 'w')  # 以写的方式打开pageCode.txt
                # urllib.request.urlretrieve()
                # pageFile.write(str(htmlCode))  # 写入
                # pageFile.close()      # 开了记得关
                filename = base64.b64decode(value.desc).decode('utf-8')
                filename = filename.replace("\"", "&")
                filename = filename.replace("\'", "&")
                filename = filename.replace("\n", "&")
                filename = filename.replace(".", "")
                filename = filename.replace("1080P<font color=&blue&>[1080p]</font>", "")
                filename = filename.replace("<font color=&blue&>[1080p]</font>", "")
                filename = value.date + "&" + filename
                print("pageIndex="+str(pageIndex) +": "+ rootUrl + url)
                urllib.request.urlretrieve(rootUrl + url,
                                           'E:\\电子书\\rep\\%s.torrent' % filename)
            except:
                print("exception,url=%s".format(value.url))
                pass
            # print(url)
        pageIndex += 1


if __name__ == '__main__':
    page_index= 1
    limit = 100
    process(300,1000)
    #threading.Thread(target=process, args=(page_index, limit,)).start()
    # while page_index < 500:
    #     threading.Thread(target=process,args=(page_index,limit,)).start()
    #     page_index = page_index+limit