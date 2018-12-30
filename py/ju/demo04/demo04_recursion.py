#coding=utf-8
def b(num):
    if num == 0:
        return
    print('xxxxx%d'%num)
    b(num=num-1)
b(10)

def test(num):
    i =1
    sumResult = 0
    while i<=num:
        sumResult = sumResult +i
        i+=1
    return sumResult
result = test(100)
print("result= %d"%result)

def test02(num):
    if num == 0 :
        return 0
    sumResult = test02(num - 1) + num
    return sumResult
print("result= %d"%test02(100))

def test03(num):
    if(num == 1):
        return num
    sum = test03(num-1)*num
    return sum
print("result = %d"%test03(2))