#coding=UTF-8
#1.打开文件
# file = open("123.txt",'a+')
# file.write("你好，嘿嘿")
# file.close()
#
# file =open("123.txt","r")
# print(file.readline())
file = open("123.txt", 'r+')
# content = file.read(5)
# print("--------以下是第一次读取到的数据----------")
# print(content)
#
# content = file.read(5)
# print("--------以下是第二次读取到的数据----------")
# print(content)
#
# content = file.read(5000)
# print("--------以下是第三次读取到的数据----------")
# print(content)


# content = file.readlines(-1)
# print(type(content))
# print("--------以下是第一次读取到的数据----------")
# for temp in content:
#     print(temp)
# content = file.readline()
# while len(content) > 0 :
#     content =file.readline()


# file.write("===========xxxxxxxxxxxxx")
# content = file.read()
# print(content)






file.close()