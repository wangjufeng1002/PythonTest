#coding=utf-8
import keyword

def isKeyWord(text):
    flag =1
    #flag =  1 表示是表示符 0表示不是标识符
    #不能是数字开头
    if not text[0].isdigit(): # 检测第一位是不是数字
        print("HeHeHe")
        if keyword.iskeyword(text): #判断是不是关键字
            flag = 0
        else:
            text1 = text.replace('_','')
            if not text1.isalnum(): #检测字符串是否由字母和数字组成
                flag = 0
    else :
         flag = 0

    if flag == 0:
        print("不是标示符")
    else:
        print("是标示符")
isKeyWord("HEHEHE")