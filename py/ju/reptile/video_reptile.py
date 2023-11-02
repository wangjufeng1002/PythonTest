# coding=utf-8
import os
import urllib.request
from requests_html import HTMLSession, AsyncHTMLSession
import chardet
import base64
import json

def replite_stock_xin_pian():

   url = 'https://stock.xinpianchang.com/nuxt-api-v2/search/query2?stockType=footage&productTypes=footage&q=&page={}&sort=default&searchEngine=search13&pageSize=100&firstCategoryId=1&isLowWeightAe=0'
   page = 1
   while True:
      req = urllib.request.Request(url.format(page))
      response = urllib.request.urlopen(req)
      result = response.read().decode('utf-8')
      resultJson = json.loads(result)
      list_ = resultJson['list']
      if len(list_) == 0:
         return

      if os.path.exists('E:\\video\\xinpianchang') is False:
         os.makedirs('E:\\video\\xinpianchang')
      for data in list_:
         name_ = data['productName'].replace("/",'').replace('\\','')
         preview_1 = data['preview1']
         if preview_1 is not None:
            urllib.request.urlretrieve(preview_1,
                                       'E:\\video\\xinpianchang\\%s.mp4' % name_)
         preview_2 = data['preview2']
         if preview_2 is not None and preview_2 !='':
            urllib.request.urlretrieve(preview_2,
                                       'E:\\video\\xinpianchang\\%s_2.mp4' % name_)
         preview_3 = data['preview3']
         if preview_3 is not None and preview_3 !='':
            urllib.request.urlretrieve(preview_3,
                                       'E:\\video\\xinpianchang\\%s_3.mp4' % name_)
         print(name_)

      page+=1

if __name__ == '__main__':
    replite_stock_xin_pian()
