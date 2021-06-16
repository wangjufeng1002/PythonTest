import json
import threading, time
import datetime

# file_object = open('D:\\爬虫\\TM\\item-detail-url.txt', "r", encoding='utf-8')
#
# readline = file_object.readlines()
# print(type(readline))
# print(readline)
# for i in range(10):
#     print(i)


# def sout(i):
#     print(threading.current_thread().name)
#
# threading.Thread(target=sout(i=1),name='Thread').start()
timeStamp = 1622278800000
timeStamp /= 1000.0
print(timeStamp)
timearr = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
print(otherStyleTime)
