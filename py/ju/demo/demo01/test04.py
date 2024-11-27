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
'''
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
'''
#4.2.3 字典格式化字符串

phonebook ={'Alice ':'1234','Beth':'9102','Cecil':'3258'}
print "Cecil's phone number is %(Cecil)s." % phonebook

template = '''
            <html>
                <head>
                   <title>%(title)s</title>
                   <body>
                    <h1>%(title)s</h1>
                    <p>%(text)s</p>
                   </body>
                </head>
            </html>'''
data = {'title':'My Home Page','text':'Welcome to my home page!'}
print template % data


#4.2.4 字典方法
#1.clear
'''
d = {}
d['name'] = 'Gumby'
d['age'] = 42
print  d
print  d.clear()

x = {}
y = x
x['key'] = 'value'
print y

#x = {}

x.clear()
print y
'''
#2.copy
# 浅复制，在修改的时候不改变原始字典，删除会影响原始字典
'''
x = {"username":"admin","mechines":['foo','bar','baz']}
y = x.copy()
y['username'] = 'mln'
y['mechines'].remove('baz')
print  x
print  y
'''
#深度复制
'''
from copy import deepcopy
d = {}
d['names']  = ["Alfred",'Bertrand']
c = d.copy()
dc = deepcopy(d)
d['names'].append('Clive')
print c
print  dc
'''
#3 fromkeys
'''
print {}.fromkeys(['name','age'])
print dict.fromkeys(['name','age'])
print dict.fromkeys(['name','age'],'(unknow)')
'''
#4 get
'''
d = {}
print d['name']
print d.get('name')
'''
d =  {}
d['name'] = 'Eric'
print d.get('name')

#代码清单4-2 字典方法示例

#使用 get()的简单数据库
'''
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
#使用get()提供默认值
person = people.get(name,{})
lable = lables.get(key,key)
result = person.get(key,'not available')
print "%s's %s is %s ." % (name,lable,result)
'''
#5.has_key
'''
d = {}
print d.has_key('name')
d['name'] = 'Eric'
print  d.has_key('name')

#6.items 和 iteritms
d = {'name':'wangjufeng','age':'22','addr':'陕西省西安市港务区新筑镇贺韶村二组'}
print  d.items()
print d.iteritems()
'''
#7.keys 和 iterkeys
d = {'name':'wangjufeng','age':'22','addr':'陕西省西安市港务区新筑镇贺韶村二组'}
print  d.keys()
print  d.iterkeys()
#8.pop
d = {'x':1,'y':2}
d.pop('x')
print d
#9.popitem
d = {'x':1,'y':2}
d.popitem()
print  d
d.popitem()
print d

#10 .setdefault
d = {}
d.setdefault('name','N/A')
print d
print d.setdefault('name','wang')
#11.update
d = {'x':1,'y':2}
x = {'x':10}
d.update(x)
print d
#12.value 和 itervalues
print d.values()
print d.itervalues()



