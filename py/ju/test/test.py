import threading
import time


# if __name__ == '__main__':
#     file_object = open('D:\\爬虫\\TM\\item-detail-base.txt', "r", encoding='utf-8')
#     writeFile = open('D:\\爬虫\\TM\\item-detail-base-x.txt', "a", encoding='utf-8')
#     lines = file_object.readlines()
#     for lin in lines:
#         if lin[0].isdigit() is False:
#             print(lin[0:10])
#         if len(lin.split("\t"))  > 15:
#             print(lin)
#             writeFile.write(lin)
#             writeFile.flush()


def thread_01():
    while True:
        print("线程1")
        time.sleep(1)


def thread_02():
    while True:
        print("线程2")
        time.sleep(1)


if __name__ == '__main__':
    # thread_01 = threading.Thread(target=thread_01,name="线程1")
    # thread_02 = threading.Thread(target=thread_02,name="线程2")
    # thread_01.start()
    # thread_02.start()
    #
    # while True:
    #     threads = threading.enumerate()
    #     print(len(threads))
    threadProcessSize = 5
    itemUrls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,89,90,56,89]
    r = int(len(itemUrls) / threadProcessSize)
    m = len(itemUrls) % threadProcessSize
    result = r + (1 if m > 0 else 0)
    for i in range(0, result):
        print(itemUrls[threadProcessSize * i: threadProcessSize * (i + 1)])

