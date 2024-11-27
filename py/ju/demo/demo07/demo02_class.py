#coding=utf-8
# class Test:
#     name ="x"
#     def  __init__(self,age):
#         self.age =age
#     def setName(self,name):
#         self.name = name
# print(Test.name)
# test01 = Test(100)
# test02 = Test(200)
# test01.setName('y')
#
# print(test01.name)
# del test01.name
# print(test01.name)

#类方法，实例方法
class Test02:
   num = 100
   name='x'
   def  __init__(self,age):
       self.age =age
   #类方法
   @classmethod
   def setNum(cls, num):
       cls.num = num
       print("sss")
   #静态方法，可以没有参数，但是必须要有 @staticmethod
   @staticmethod
   def test():
       print('静态方法')

Test02.setNum(9090)
print(Test02.num)
Test02.test()
test02 = Test02(11)
test02.test()
test02.setNum(11)