#coding=utf-8
#9 * 9 乘法表
i = 1
while i<=9:
    j = 1
    while j <= i:
        print("%d * %d = %d"%(j,i,i*j),end=' ')
        j+=1
    print("")
    i+=1
