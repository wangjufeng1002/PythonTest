#coding=utf-8
'''
def test(num):
    i=0
    while i< num:
        print('_'*20)
        i+=1
test(3)

def test2(num0,*num):
    for temp in num:
        print(temp)
test2(2,33,44,55)
'''
def test3(name,age=18):
    print("name=%s,age=%d"%(name,age))
test3(1)
test3(age=100,name=100)
