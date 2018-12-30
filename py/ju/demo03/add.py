#coding=utf-8
def mySum(a):
    i = 1
    sumReslt = 0
    while i<=a:
        sumReslt = sumReslt+a
        i+=1
    return sumReslt
num = int(input("请输入一个数字（整数）:"))

result = mySum(num)
print("结果是：",result)