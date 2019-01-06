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

# 文件的复制
# def copy_file(fileName,backFileName):
#     file = open(fileName, "r")
#     file_back = open(backFileName, "a+")
#     content = file.read()
#     while len(content) > 0:
#         file_back.write(content)
#         content = file.read()
#     file_back.close()
#     file.close()
#
# fileName = input("请输入要拷贝的文件名字：")
#
# backName = fileName[0:fileName.rfind('.')]
# backFile = backName+"testTack"+fileName[fileName.rfind('.'):]
# copy_file(fileName,backFile)

#文件的定位读写
#在文本文件中，没有使用b模式选项打开的文件，只允许从文件头开始计算相对位置，从文件尾计算时就会引发异常
f = open('123.txt','rb')

# print(f.read(4))
# print(f.tell())
# print(f.read(5))
# print(f.tell())
# print(f.read(6))
# print(f.tell())

#seek(offset,from)
#offset:偏移量
#whence:方向
    #0：表示文件开头
    #1: 表示当前位置
    #2: 表示文件末尾
#f.seek(90,0)
# f.seek(0,2)
# print(f.tell())
# f.seek(-1,1)
# print(f.tell())
#print(f.read(10))

import os
#文件重命名
#os.rename("123.txt","12345.txt")
#os.remove("123.txt")



#批量文件重命名
print(os.path.abspath("."))
print(os.listdir(os.path.abspath(".")))

# movieNames = os.listdir(os.path.abspath(".")+"\movies")
# for temp in  movieNames:
#     os.rename(os.path.abspath(".")+"\movies\\"+temp,os.path.abspath(".")+"\movies\\"+"[xxx]-"+temp)
#     print(temp)
print("---dir===")
print(dir(os))
print("---dir===")
#文件夹操作
import os

#os.mkdir("zhangsan")
print(os.getcwd()) #获取当前路径
#os.chdir()         #改变路径
os.listdir()       #获取目录列表
#os.rmdir()         #删除目录