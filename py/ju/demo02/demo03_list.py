#coding=utf-8
'''
print("王巨峰")
liebiao=["小王",'小张']
name=["donge","wanghao","张三"]
name.append("王")
print(name.index("王"))
print(name)
length = len(name)
i = 0;
while i<len(name):
    #print("name[%d]=%s"%(i,name[i]))
    print("name[%d]=%s"%(i,name[i]))
    i+=1
print("#######################")
for n in name :
    print(n)
'''
### 列表的相关操作
'''
movies=["加勒比海盗","速度与激情"]
for name in movies:
    print(name)
movieName = input("请输入电影名称:\n")
movies.append(movieName)

movieName = input("请输入要删除的电影名称:\n")
movies.remove(movieName)

movies=["加勒比海盗","速度与激情"]
movieName = input("请输入电影名称:\n")

if movieName in movieName:
    print("您要看的电影，本影院今晚播放！！！")
'''
names=["a","b","c"]
print(names)
names.remove("a")
print(names)
print(names.pop())
print(names)
while True:
    print("AAAA")



