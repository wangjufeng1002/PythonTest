#coding=utf-8
#字典:当索引不好用时

#4.2创建和使用字典
phonebook ={'Alice ':'1234','Beth':'9102','Cecil':'3258'}

#4.2.1 dict 函数
'''
items = [('name','Gumby'),('age',42)]
d = dict(items)
print d['name']
d = dict(name='Gumby',age=42)
print d['age']
'''
#4.2.2 基本字典操作
'''
x = [None]*43
x[42] = 'wang'
x = {}
x[42] = 'Foobar'
print x
'''

#字典示例
#一个简单的数据库
people ={
    'Alice':{
        'phone':'1234',
        'addr' :'Foo drive 23'
    },
    'Beth':{
        'phone':'9102',
        'addr' :'Bar street 42'
    },
    'Cecil':{
        'phone':'232332',
        'addr' :'Baz avenue 90'
    }
}
#针对电话号码和地址使用的描述性标签，会在打印输出的时候用到
lables = {
    'phone' : 'phone number',
    'addr'  : 'address'
}
name = raw_input('Name: ')
#查找电话号码还是地址？
request = raw_input('Phone number (p) or address(a)?')
#使用正确的键：
if request == 'p' : key = 'phone'
if request == 'a' : key = 'addr'
#如果名字是字典中的有效键才打印信息
if name in people: print "%s's %s is %s ." % (name,lables[key],people[name][key])