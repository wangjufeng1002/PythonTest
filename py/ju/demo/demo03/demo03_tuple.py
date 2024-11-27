#coding=UTF-8
import operator
tup1=("physics","chemistry",1997,2000)
tup2=(1,2,3,4,5,6)
tup3="a","b","c","d"
tup4=(80,)
'''
print(tup4)
print("tup1[0]: ",tup1[0])
print("tup1[1,3]: ",tup1[1:3])
print("tup2[1,-1]: ",tup1[1:-1])
'''
#元组是不能修改的
#tup4[0]=100
#tup5 = tup4+tup1+tup2+tup3
#print(tup5)
#元组的值是不允许删除的，但是可以使用del语句删除整个元组
#del tup5
#print(tup5)

#元组的运算
print(len(tup1))
print(tup3*4)
print(3 in tup3)
print(operator.le(tup3,tup1))
print(operator.lt(tup3,tup1))
print(min(tup3))