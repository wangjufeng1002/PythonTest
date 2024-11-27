#coding=utf-8
#匿名函数 没有名字的函数叫做匿名函数
def add2Nums(a,b):
    return  a+b
print(add2Nums(2,2))

lam = lambda a,b:a+b
print(lam(1,2))

lam1 = lambda  a:a*3.14
print(lam1(2909090))

# 可读性太低
if (lambda a:a+10000-2*5)(100000) > 9:
    print("jajhhahah")

