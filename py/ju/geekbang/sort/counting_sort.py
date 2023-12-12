#!/usr/bin/env python
# coding=utf-8

# 计数排序

# arr = [3,5,2,1,4]
# c   = [] * (max(arr)+1)
# c   = [0,1,1,1,1,1]           -- 保存 arr 中每个值的个数，c 数组中的下标为 arr 中的值，c 数组值为对应arr 值的个数
# c -> add =   [0,1,2,3,4,5]    -- 依次累加，计算出arr 中每个值对应新数组中的下标，累加之后，c 中的值为 arr 值（c中下标） 所对应再数组中的下标
#

def counting_sort(arr):
    """
        :type arr: List[int]
        :rtype: List[int]
    """
    if len(arr) <= 1:
        return

    max = arr[0]
    for i in range(1, len(arr)):
        if max < arr[i]:
            max = arr[i]

    c = [0] * (max + 1)

    # 计算每个元素的个数，放入C中
    for i in range(0, len(arr)):
        c[arr[i]] += 1

    # print(arr)
    # print(c)
    # 依次累加 C 中的元素
    for i in range(1, len(c)):
        c[i] = c[i - 1] + c[i]
    print(c)

    # 临时数组r,存储排序之后的结果
    r = [None] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        index = c[arr[i]] - 1
        r[index] = arr[i]
        c[arr[i]] -= 1

    for i in range(0, len(arr)):
        arr[i] = r[i]
    print(arr)


if __name__ == '__main__':
    counting_sort([3, 5, 2, 1, 4])
