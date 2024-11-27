# coding=utf-8
import hashlib
import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging
import urllib.parse
import urllib.request
import urllib
import json

import pyttsx3
from flask import Flask, send_file, request

app = Flask(__name__)


@app.route("/callback/", methods=['GET'])
def callback():
    auth_code = request.args.get("auth_code")
    state = request.args.get("state")  # state可根据实际情况使用
    for key, values in request.args.items():
        print(key + " : " + values)
    if auth_code:
        try:
            print(auth_code)
            getToken(auth_code,state)
        except Exception as err:
            logging.warning("get access_token failed, err=%s", err)
        return "SUCCESS"
    return "SUCCESS"


def getToken(authCode, state):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        "employeeid": "1533732187472879616",
        "Content-Type": "application/json",
        "token": "974a76852770990c1acfa3639cccc358"
    }
    json_obj = json.loads(state)
    url = "http://127.0.0.1:11601/qianchuan/api/accessToken"
    data_dict = {"authCode": authCode, "appId": json_obj["appId"], "secret": json_obj["secret"],
                 "shopCode": json_obj["shopCode"]}
    jsonData = json.dumps(data_dict).encode('utf-8')
    request = urllib.request.Request(url=url, headers=headers, data=jsonData, method='POST')
    response = urllib.request.urlopen(request)
    print(response)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app, handler_class=WebSocketHandler)
    server.serve_forever()
