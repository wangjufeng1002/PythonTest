import datetime
import uuid

import pyttsx3

# dir_path = './mp3/'
#
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# # 设置语音（默认为中文）
# engine.setProperty('voice', voices[0].id)
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice)
# engine.setProperty('rate', 200)
#  # 设置音量（默认为1.0）
# engine.setProperty('volume', 1.0)
# filepath = dir_path + '/' + str(uuid.uuid1()).replace("-", "") + "-" + str(
# int(datetime.datetime.now().timestamp() * 1000)) + ".mp3"
# engine.save_to_file('登记成功，不知道设呢么仓包裹', filepath)
# engine.runAndWait()


count = 0
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    count += 1
    print("语音包%s:" % count)
    print(" - ID: %s" % voice.id)
    print(" - 姓名: %s" % voice.name)
    print(" - 语言: %s" % voice.languages)
    print(" - 性别: %s" % voice.gender)
    print(" - 年龄: %s\n" % voice.age)




