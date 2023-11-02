import tempfile

import pyttsx3
import time

# 临时文件夹
directory = tempfile.TemporaryDirectory()
# 创建临时文件
file = tempfile.TemporaryFile(dir=directory.name)
print(file.name)

engine = pyttsx3.init()
# 设置语速（默认为200）
engine.setProperty('rate', 150)
# 设置音量（默认为1.0）
engine.setProperty('volume', 0.8)
# 设置语音（默认为中文）
engine.setProperty('voice', 'en')

engine.say("登记成功，泾阳仓包裹")
engine.save_to_file("登记成功，泾阳仓包裹", file.name)
engine.runAndWait()

time.sleep(10000000)



# def text_to_speech(text, output_file):
#     engine = pyttsx3.init()
#     engine.save_to_file(text, output_file)
#     engine.runAndWait()
#
# text = "Hello, World!"
# output_file = "output.mp3"

