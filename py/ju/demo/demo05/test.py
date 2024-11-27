#coding=utf-8
def printHello():
    print("-"*30)
    print("******* hello *******")
    print("-"*30)
#print('------ in test.py------')
#printHello()
#print('-------out test.py-----')
#print(__name__)
def main():
    print("这里是main函数")
    printHello()
    pass
## 再本文件中执行__name__ = __main__ 再其他文件中调用为本模块名
if __name__ == '__main__':
    print('------ in test.py------')
    printHello()
    print('-------out test.py-----')