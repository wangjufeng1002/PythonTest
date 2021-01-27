# coding=utf-8
import urllib.request
import chardet
import base64
import re

x = 0
imglist = [0,1,2]
for img in imglist:

    print(img)

    urllib.request.urlretrieve('http://ppic.meituba.com/uploads/160322/8-1603220U50O23.jpg', 'E:\\repltile\\%s.jpg' % x)

    x += 1

