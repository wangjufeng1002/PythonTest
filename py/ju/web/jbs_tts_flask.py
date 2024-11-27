# coding=utf-8
import hashlib
import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging
import urllib.parse

import pyttsx3
from flask import Flask, send_file, request

dir_path = './mp3/'

app = Flask(__name__)

# 加载缓存文件
mp3_cache = {}

logging.basicConfig(level=logging.INFO)


@app.route("/convert", methods=['GET'])
def convert():
    # 两次编码，这里手动解码
    text = urllib.parse.unquote(request.args.get("text"))
    rate = request.args.get("rate")
    # 待转换文本
    if text is None or text == '':
        return "ERROR"

    # 设置语速（默认为200）
    if rate is None:
        rate = 200

    # 文字+语速转换成md5
    text_md5 = hashlib.md5((text + str(rate)).encode(encoding='UTF-8')).hexdigest()

    # 缓存中有且文件存在
    if mp3_cache.get(text_md5) is not None and os.path.exists(mp3_cache.get(text_md5)):
        # return Response(file_send(mp3_cache[text_md5]), content_type="audio/mpeg")
        return send_file(mp3_cache[text_md5])

    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(voice)

    engine = pyttsx3.init()
    # 设置语速（默认为200）
    engine.setProperty('rate', rate)
    # 设置音量（默认为1.0）
    engine.setProperty('volume', 1)
    engine.setProperty('voice', 'zh')

    filepath = dir_path + '/' + text_md5 + ".mp3"
    engine.save_to_file(text, filepath)
    engine.runAndWait()

    # 加入缓存
    mp3_cache[text_md5] = filepath
    # response = Response(file_send(filepath), content_type="audio/mpeg")
    return send_file(filepath)


# send big file
def file_send(file_path):
    with open(file_path, 'rb') as f:
        while 1:
            data = f.read(20 * 1024 * 1024)  # per 20M
            if not data:
                break
            yield data


@app.route("/health")
async def health():
    return {"200": "Server is healthy"}


# 重置缓存
@app.route("/resetCache")
async def resetCache():
    init_cache()
    return {"200": "cache reset success"}


# 初始化缓存
def init_cache():
    mp3_cache.clear()
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith("mp3") is False:
                continue
            mp3_cache[filename.replace(".mp3", '')] = os.path.join(dirpath, filename)


if __name__ == '__main__':
    exists = os.path.exists(dir_path)
    if exists is False:
        os.mkdir(dir_path)
    # 初始化缓存
    init_cache()
    # 启动app
    # uvicorn.run(app='jbs_tts_flask:app', host="0.0.0.0", port=29081, workers=4)
    # app.run(host="0.0.0.0", port=29081)

    # server = pywsgi.WSGIServer(('0.0.0.0', 29081), app, handler_class=WebSocketHandler)
    # server.serve_forever()
    # print("aaa")
