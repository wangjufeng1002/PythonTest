# coding=utf-8
from py.ju.reptile.entity import Data
import urllib.request
import chardet
import base64
import re
import datetime
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
''' 防止403'''
opener=urllib.request.build_opener()
urllib.request.install_opener(opener)
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')]
page1 = urllib.request.Request("https://www.0c0bd5cb03db.com/index/home.html", headers=headers)
page = urllib.request.urlopen(page1)  # 打开网页
htmlCode = page.read()  # 获取网页源代码
# print(chardet.detect(htmlCode))  # 打印返回网页的编码方式
# print(htmlCode.decode('utf-8'))  # 打印网页源代码