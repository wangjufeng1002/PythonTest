#coding=utf-8
class Dog:
    #属性
    color = '白色'
    sex   = '公'
    def __init__(self,name):
        self.name = name


    #方法
    def eat(self):
        if self.name is None:
            print("狗在吃骨头")
        print(self.name,"狗在吃骨头")
        self.dead()
    def run(self):
        print(self.name,"狗在跑")
    def dead(self):
        print(self.name,"狗死了")
    def setName(self,name):
        self.name = name;

dog1 = Dog("哈士奇")
dog1.run()

dog2 = Dog("金毛")
dog2.dead()