# coding=utf-8
from py.ju.reptile.entity import Data
import urllib.request
import chardet
import base64
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

rootUrl = 'aHR0cHM6Ly9iYnMubnRmMS5zaXRlLzIwNDgvdGhyZWFkLnBocD9maWQtMTVzLXBhZ2Ut'
rootUrl = base64.b64decode(rootUrl).decode('utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
''' 防止403'''
opener=urllib.request.build_opener()
urllib.request.install_opener(opener)
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')]

page1 = urllib.request.Request('https://bbs.ntf1.site/2048/thread.php?fid-15s-page-2.html', headers=headers)
page = urllib.request.urlopen(page1)  # 打开网页
htmlCode = page.read()  # 获取网页源代码
print(chardet.detect(htmlCode))  # 打印返回网页的编码方式
print(htmlCode.decode('utf-8'))  # 打印网页源代码

# pageIndex = 2
# while pageIndex < 100:
#     print("开始处理 %d 页" % pageIndex)
#     page1 = urllib.request.Request(rootUrl + str(pageIndex) +'.html', headers=headers)
#     page = urllib.request.urlopen(page1)  # 打开网页
#     htmlCode = page.read()  # 获取网页源代码
#     print(chardet.detect(htmlCode))  # 打印返回网页的编码方式
#     print(htmlCode.decode('utf-8'))  # 打印网页源代码
#     print("开始处理============================================================================")
#     htmlCode = htmlCode.decode('utf-8')
#     clan_rows = re.findall(r'\<td.*\>', htmlCode, re.M | re.I)  # 清洗 <> 开始
#     datas=[]
#     for row in clan_rows:
#         if 'movie' in row:
#             date = re.findall(r'\[.*\]', row, re.M | re.I)
#             uri = re.findall(r'href="/movie.php\?id=\d*\"', row)
#             dec = re.findall(r'd\(\'.*\)', row)
#             # print(date[0] + '+' + uri[0] + '+' + dec[0])
#             url = uri[0].replace('href="', '').replace('"','')
#             dec = dec[0].replace('d(\'', '').replace('\'))', '')
#             print(date[0] + ' ' + url + ' ' + dec)
#             data= Data(date[0],dec,url)
#             datas.append(data)
#             # print(row)
#     ##提取有用字符
#     print(len(datas))
#     # for value in datas:
#     #     page1 = urllib.request.Request(rootUrl +value.url, headers=headers)
#     #     page = urllib.request.urlopen(page1)  # 打开网页
#     #     htmlCode = page.read()  # 获取网页源代码
#     #     # print(chardet.detect(htmlCode))  # 打印返回网页的编码方式
#     #     # print(htmlCode.decode('utf-8'))  # 打印网页源代码
#     #     print("============================下载中================================================")
#     #     htmlCode = htmlCode.decode('utf-8')
#     #     url = re.findall(r'href="/torrent/.*\.torrent\"', htmlCode)
#     #     url = url[0].replace('href="', '').replace('"','')
#     #     #
#     #     # pageFile = open('pageCode.txt', 'w')  # 以写的方式打开pageCode.txt
#     #     # urllib.request.urlretrieve()
#     #     # pageFile.write(str(htmlCode))  # 写入
#     #     # pageFile.close()      # 开了记得关
#     #     filename = base64.b64decode(value.desc).decode('utf-8')
#     #     filename = filename.replace("\"","&")
#     #     filename = filename.replace("\'", "&")
#     #     filename = filename.replace("\n", "&")
#     #
#     #
#     #     urllib.request.urlretrieve(rootUrl+url,
#     #                                'E:\\repltile\\%s.torrent' %filename )
#
#
#     pageIndex+=1
