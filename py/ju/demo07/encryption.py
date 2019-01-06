#coding=utf-8
import random
ndjiami=str(input('请输入要加密的文件名：'))
Openwj=open(ndjiami,'r')

#创建要加密的文件名
newnamedian=ndjiami.rfind('.')
if newnamedian > 0:
    newnamedian = ndjiami[:newnamedian]
    newnamehou = ndjiami[newnamedian:]
newname = newnamedian + '[jiami]'+ newnamehou

newwrite= open(newname,'w')

content = Openwj.read(1)
while len(content) > 0:
    newwrite.write(content)
    newwrite.write(str(random.randint(11,99)))
    content = Openwj.read(1)
Openwj.close()
newwrite.close()
