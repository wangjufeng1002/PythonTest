#coding=utf-8
num=0b00000000011
num= num <<2
num = num >> 2
num = num & 0b11111111111
num = num | 0b11111111111
num = num ^ 0b11111111111
num = 9
num = ~num
#print(num)

a = 0b00001001
b = 0b00001010
#print((a|b))
#num=input("tips:")
#print(num)
#int(num)
#hex(num) #十六进制
#oct(num)
#ord(1000.0)
print(int('0b100',2))