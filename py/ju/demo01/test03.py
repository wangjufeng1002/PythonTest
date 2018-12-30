#coding=utf-8
#字符串的使用
#3.1
'''
website = 'http://www.python.org'
print website[3:]
c
#3.2 字符串格式化:精简版
format = "Hello %s, %s enough for ya?"
values = ("world","Hot")
print format % values
'''

'''
format = "Pi with three decimals: %.3f"
from math import pi
print format % pi

from string import  Template
s = Template('$x,glorious $x!')
print  s.substitute(x='slurm')

s = Template("It's ${x}tastic!")
print  s.substitute(x='slurm')

s = Template("Make $$ selling $x!")
print  s.substitute(x='slurm')

s = Template("A $thing must never $action. ")
d = {}
d['thing'] = 'gentleman'
d['action'] = 'show his socks'
print  s.safe_substitute(d)
'''
#3.3 字符串格式化：完整版
'''
print '%s plus %s equals %s' % (1,1,4)
print  'Price of eggs : %d ' % 42
print  'Price of eggs : %X ' % 42
print  'Price of eggs : %i ' % 42
print  'Price of eggs : %+d ' % -42
print  'Price of eggs : %r ' % 42
print  'Price of eggs : %s ' % 42
print  'Price of eggs : %.3f ' % 42.12131

#3.3.1 简单转换
print  'Price of eggs : %d ' % 42
print  'Price of eggs : %X ' % 42
print  'Price of eggs : %i ' % 42
print  'Price of eggs : %+d ' % -42
print  'Price of eggs : %r ' % 42
print  'Price of eggs : %s ' % 42
'''
'''
#3.3.2 字宽和精度
print '%10f' % pi
print '%10.2f' % pi
print '%-10.2f' % pi #左对齐
print '%.2f' % pi
print '%.5s' % 'Guido van Rossum'
print '%-*.*f' % (5,1,pi)
#3.3.3 符号，对齐和用0补充
'''
'''
print '%010.2f' % pi
print  010
print '%10.2f' % pi
'''

#字符串格式化示例
#使用给定的宽度打印格式化后的价格列表
'''
width = input('Please enter width: ')
price_width = 10
item_width = width - price_width
header_format  = '%-*s%*s'
format         = '%-*s%*.2f'
print '=' * width
print header_format % (item_width,'Item',price_width,'Price')
print '-' * width
print format % (item_width,'Apples',price_width,0.4)
print format % (item_width,'Pears',price_width,0.5)
print format % (item_width,'Cantaloupes',price_width,1.92)
print format % (item_width,'Dried Apricouts(16 oz .)',price_width,8)
print format % (item_width,'Prunes(4 lbs)',price_width,12)
print '='*width
'''

#3.4字符串方法

#3.4.1 find
'''
title = 'wangjufeng'
print  title.find('j')

subject = '$$$ Get rich now !!! $$$ '
print subject.find('$$$')

print subject.find('$$$',3)

print subject.find('!!!',0,20)
'''
#3,4.2 join
'''
seq = [1,2,3,4,5]
sep = '+'
print sep.join(seq)
'''
'''
seq = ['1','2','3','4','5']
sep = '+'
print sep.join(seq)

dirs = 'wang','ju','feng'
print '/'.join(dirs)

print 'C:'+ '\\'.join(dirs) 
'''
#3.4.3 lower
'''
print 'WANGJUFENG'.lower();
name = 'Gumby'
names = ['gumby','smith','jones']
if name.lower() in names : print 'Fount it'

print  'wangjufeng love liujuan '.title();
import string
print string.capwords("this's all ,folks")
'''
#3.4.4
#print 'This is a test'.replace('is','eez')

#3.4.5 split
print '1+2+3+4+5'.split("+")

#3.4.6 strip
print ' internal whitespace is kept    ' .strip()

names = ['gumby','smith','jones']
name = 'gumby  '
if name in names : print 'Fount it'
if name.strip().lower() in names : print 'Fount it'
#3.4.7 translate
from string import maketrans
table = maketrans('cs','kz')
print  len(table)
print  table[97:123]
print  maketrans('','')[97:123]
print "this is an increible test".translate(table)







 