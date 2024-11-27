#coding=utf-8
class ShorInputException(Exception):
    '''你定义的异常类'''
    def __init__(self,length,atleast):
        Exception.__init__(self)
        self.length = length
        self.atleast = atleast

try:
    s = input('请输入----> ')
    if len(s) < 3:
         raise ShorInputException(len(s),3)
except EOFError:
    print("/n你输入了一个技术标记符EOF")
except ShorInputException as x:
    print("ShorInputException: %d,%d"%(x.length,x.atleast))
else:
    print("没有异常")