# coding=utf-8
import hashlib
import os
from typing import Union
import pyttsx3
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import urllib.parse
import logging
from logging import handlers


dir_path = './mp3/'

log_path = './logs/'

exists = os.path.exists(dir_path)
if exists is False:
    os.mkdir(dir_path)
exists = os.path.exists(log_path)
if exists is False:
    os.mkdir(log_path)


# 日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个handler，用于将日志输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

#  创建一个handler，用于将日志输出到文件
fh = handlers.TimedRotatingFileHandler(filename='./logs/server.log', when='D', backupCount=3, encoding="utf-8")
fh.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

app = FastAPI(http2=False)

@app.get("/convert")
async def convert(text: str, rate: Union[int, None] = None):
    # 待转换文本
    if text is None or text == '':
        return "ERROR"

    # 设置语速（默认为200）
    if rate is None:
        rate = 200
    text = urllib.parse.unquote(text)
    # 文字+语速转换成md5
    text_md5 = hashlib.md5((text + str(rate)).encode(encoding='UTF-8')).hexdigest()

    filepath = dir_path + '/' + text_md5 + ".mp3"

    # 缓存中有且文件存在
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="audio/mpeg")

    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(voice)

    engine = pyttsx3.init()
    # 设置语速（默认为200）
    engine.setProperty('rate', rate)
    # 设置音量（默认为1.0）
    engine.setProperty('volume', 1)
    engine.setProperty('voice', 'zh')

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    response = FileResponse(filepath, media_type="audio/mpeg")
    return response


@app.get("/health")
async def health():
    return {"200": "Server is healthy"}


# 重置缓存
@app.get("/resetCache")
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

    # 初始化缓存
    init_cache()

    # 启动app
    uvicorn.run(app='jbs_tts:app', host="0.0.0.0", port=29081, workers=4, log_config=None)
