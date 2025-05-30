# coding=utf-8
from random import random

from py.ju.reptile.demo.entity import Data
import urllib.request
from requests_html import HTMLSession
import base64
import re
import ssl
from translate import Translator

translator = Translator(from_lang='ja', to_lang='zh')
context = ssl._create_unverified_context()
#rootUrl = 'aHR0cHM6Ly93d3cuYnRndy54eXovbGlzdC5waHA/Y2xhc3M9Z3VvY2hhbiZwYWdlPQ=='
rootUrl = 'https://www.ad3458.com/movie/youma/index_2.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
''' 防止403'''
opener = urllib.request.build_opener()
urllib.request.install_opener(opener)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')]
pattern = r"document\.write\(d\('(.*?)'\)\)"

def process(page,limit):
    pageIndex = page
    endIndex = pageIndex + limit
    pageFile = open('D:\\其他\\电子书\\page_text.txt', 'w')  # 以写的方式打开pageCode.txt
    while pageIndex <= endIndex:
        print("开始处理 %d 页" % pageIndex)
        #session = HTMLSession()
        #detailResponse = session.get(url=rootUrl.format(index=page), headers=headers)
        #print(detailResponse)


        page1 = urllib.request.Request(rootUrl.format(index=page), headers=headers)
        page = urllib.request.urlopen(page1, context=context)  # 打开网页
        html_code = page.read()  # 获取网页源代码
        html_code = html_code.decode('utf-8')
        #print(html_code)

        # 使用re.findall查找所有匹配项
        matches = re.findall(pattern, html_code, re.DOTALL)

        pageFile.writelines("========={index}开始=======\n".format(index=pageIndex))
        # 输出提取结果
        for i, match in enumerate(matches, 1):
            #print(f"匹配项 {i}:")
            translate = translator.translate(base64.b64decode(match).decode('utf-8'))
            print(translate)
            pageFile.writelines(translate)
            #print("-" * 50)
        pageFile.writelines("========={index}结束=======\n".format(index=pageIndex))
        pageFile.flush()
        pageIndex+=1

    pageFile.close()

if __name__ == '__main__':
    page_index= 1
    limit = 100
    process(page_index,limit)
    #threading.Thread(target=process, args=(page_index, limit,)).start()
    # while page_index < 500:
    #     threading.Thread(target=process,args=(page_index,limit,)).start()
    #     page_index = page_index+limit
    #MTAyMjI0XzEwMCBQQUNPIOODkeOCs+ODkeOCs+ODnuODnuassuacm+OCkuaKkeOBiOOBjeOCjOOBquOBhOODpOODquOCv+OCpOebm+OCiuOBruS4ieWNgei3r+Wmuw==