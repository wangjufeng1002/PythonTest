# coding=UTF-8
# info
info={"name":"zhangsan","add":"山东"}
info['x']="Q"
#info.clear()  #清空
#del info['x'] #删除

#print(info.pop("x"))
print(info)
keys = info.keys()
if "name" in keys:
    print(info["name"])
if "!!!" not in info.values():
    print("!!! 不存在")
else:
    print("在")

if info.__contains__("x") :
    print(info["x"])
else:
    print("xbucunz")


for val in info.values():
    print(val)

for item in info.items():
    print(item)
for key,val in info.items():
    print("key=%s,val=%s"%(key,val))






