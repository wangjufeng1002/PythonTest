#coding=utf-8
import time
class GUN:
    def __init__(self,name,bulletNum):
        self.name = name
        self.bulletNum = bulletNum
    def biubiu(self):
        if self.bulletNum > 0 :
            self.bulletNum -=1
            print("%s还剩%s发子弹"%(self.name,self.bulletNum))
        else:
            print("%s没子弹了"%self.name)
    def __del__(self):
        print()

AK47 = GUN("AK47",5)
JIATELIN = GUN("加特林",10)

while True:
    AK47.biubiu()
    JIATELIN.biubiu()
    time.sleep(1)
