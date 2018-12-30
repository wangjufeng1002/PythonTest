# coding=UTF-8
#print("哈——哈")
#print("哈——哈")
#print("哈——哈")
#print("哈——哈")
import time
import calendar
import random
# function 函数
def print_1():
    print("哈——哈")
    print("哈——哈")
    print("哈——哈")
    print("哈——哈")


def print_2():
    print("嘿——嘿")
    print("嘿——嘿")
    print("嘿——嘿")
    print("嘿——嘿")
# 调用函数：即去执行这个函数中的代码
print_2()
currentTime = time.time();
print('currentTime:',currentTime)
#本地时间
localTime = time.localtime();
formatTime = time.asctime(localTime)
#print(localTime)
#print(formatTime)
#print(calendar.month(2018,12))
print(random.randint(0,2))
print(random.uniform(1,5))
print(random.randrange(0,50,2))
