#coding=utf-8
#子弹
class zidan:
    def __init__(self,shashangli):
        self.shashangli= shashangli
#弹夹
class danjia:
    def __init__(self,num):
        self.danjianum  = num
        self.zidanliebiao = []
    def zhuangdan(self,zidan):
        self.zidanliebiao.append(zidan)
        print("子弹+1...当前的子弹数%d"%len(self.zidanliebiao))
#枪
class Qiang:
    #类属性
    test ='1'
    def __init__(self,name):
        #实例属性
        self.name = name
    def liandanjian(self,danjia):
        self.danjia = danjia
        print("换弹夹")
#人
class Ren:
    def maiqiang(self,qiang):
        self.qiang = qiang
        print("买了一把枪")
    def yazidan(self,danjia,zidan):
        danjia.zhuangdan(zidan)
    def zhuangdanjia(self,danjia):
        self.qiang.liandanjian(danjia)
xiaoming =Ren()
mp5 = Qiang("mp5")
xiaoming.maiqiang(mp5)
#创建弹夹
danjia = danjia(100)
#创建一颗子弹
zidan = zidan(100)
xiaoming.yazidan(danjia,zidan)
xiaoming.zhuangdanjia(danjia)






