#coding=utf-8
#列表和元组
edward = ['Edward GumBy',42]
john = ['John Smith',50]
database = [edward,john]
print  database

#通用序列操作
#1.索引
greeting = 'Hello'
print greeting[0]
print greeting[-1]

#2.分片
numbers  = [1,2,3,4,5,6,7,8,9,10]
print numbers[3:6]
print numbers[0:1]
print numbers[-3:-1]
print numbers[:3]
print numbers[:]
#2.1 步长
print numbers[0:10:2]
print numbers[::4]
print numbers[-5:-10:-2]
#2.3序列相加
print [1,2,3]+[4,5,6]
print 'Hello ' + ' World!'
#2.4乘法
print 'python'*5
print [42]*10
#空值
sequence = [None] * 10
print sequence

############序列(字符串) 乘法示例
'''
sentence = raw_input("Sentence: ")
screen_width = 80
text_width = len(sentence)
box_width =text_width + 6
left_margin = (screen_width -box_width)//2
print
print ' ' * left_margin + '+' + '-' * (box_width-2) + '+'
print ' ' * left_margin + '|' + ' ' * text_width    + '|'
print ' ' * left_margin + '|' +         sentence     + '|'
print ' ' * left_margin + '|' + ' ' * text_width    + '|'
print ' ' * left_margin + '+' + '-' * (box_width-2) + '+'
'''

#2.5 成员资格
'''
permissions  = 'rw'
print  'w' in permissions
users = ['mlh','foo','bar']
print raw_input("Enter your name : ") in users
'''
#2.6
'''
database = [
    ['albert','1234'],
    ['dilbert','4242'],
    ['smith','7542'],
    ['jones','9843']
]
username = raw_input("User name : ")
pin = raw_input("PIN code : ")
if [username,pin] in database: print  "Access login"
'''
#长度，最小值和最大值
numbers = [100,34,678]
print len(numbers)
print max(numbers)
print min(numbers)
print max(2,3)
print min(2,3)

#2.3 列表
#2.3.1 list函数
'''
someList = list(["Hello","ju"])
"wangufeng".join(someList)
print someList
'''
#2.3.2 基本的列表操作
#1.元素复制
x=[1,1,1]
x[1] = 2
print  x

#2.删除元素
names = ['Alice','Beth','Ceil','Dee-De','Earl']
del names[0]
print  names

#3.分片赋值
'''
name = list("wangjufeng")
print name
name[2:] = list('ar')
print name

name[1:1] = list("wwwww")
print name
name [1:] = []
print name
'''
#2.3.3列表的方法
'''
lst  = [1,2,3]
lst.append(4)
print lst

x = [[1,2],3,4,4,[5,6]]
n = x.count([1,2])
print n

a=[1,2,3]
b=[4,5,6]
a.extend(b[1:])
print a
print a.index(1)

a.insert(1,4)
print a

print  a.pop()
print  a

x = ['to','be','or','not','to','be']
x.remove('be')
print x
x.reverse()
print x
x.sort()
print x

y = x[:]
print x
y.sort()
print y

x=[4,6,2,1,7,9]
y = sorted(x)
print x
print y
print sorted("pyhton")

x=['adadsd','adsadsadsad','ss','dsd']
x.sort(key=len)
print x

x.sort(key=len,reverse=True)
print x
'''

#2.4 不可变序列
x=(42,)
print 3*(42,32,)

print  tuple("hello")
x = 1,2,3


