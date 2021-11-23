#coding=utf-8
import  db
if __name__ == '__main__':
    file = open("C:\\Users\\wangjufeng\\Desktop\\3333333.txt", encoding='utf-8')
    #file = open("/user/local/py-work/3333333.txt", encoding='utf-8')
    while True:
        line = file.readline()  # 包括换行符
        line = line[:-1]  # 去掉换行符
        db.execute(line)
