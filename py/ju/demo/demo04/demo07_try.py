#coding=utf-8
print('--------------2--------------')
try:
   # num = 100
    print(num)
    #open("xxx.txt","r")
except (NameError,IOError) as result:
    print("NameError发生异常")
    print(result)
else:
    print("没有异常")
finally:
    print("我是finally")
print('--------------2--------------')

