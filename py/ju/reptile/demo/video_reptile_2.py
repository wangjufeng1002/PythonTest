import os
import urllib.request
from requests_html import HTMLSession, AsyncHTMLSession
import chardet
import base64
import json


req = urllib.request.Request("https://uvwwk5w5ub.xyz/km/index.html#/hot_sq?num=0")











user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'


# 添加用户代理到HTTP头部
req.add_header('User-Agent', user_agent)

response = urllib.request.urlopen(req)
result = response.read().decode('utf-8')
print(result)
