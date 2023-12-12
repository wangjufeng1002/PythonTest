#!/usr/bin/env python
# coding=utf-8

# 归并排序

def merge(arr, p, q, r):
    i = p
    j = q + 1
    k = 0
    tmp = [None] * (r - p + 1)

    while i <= q and j <= r:
        if arr[i] < arr[j]:
            tmp[k] = arr[i]
            k += 1
            i += 1
        else:
            tmp[k] = arr[j]
            k += 1
            j += 1

    # 判断部分数据不为空
    start = i
    end = q
    if j <= r:
        start = j
        end = r

    # 将剩余的数据拷贝到临时列表
    while start <= end:
        tmp[k] = arr[start]
        k += 1
        start += 1

    # 用临时列表替换原始数据数据
    for i in range(0, r - p + 1):
        arr[p + i] = tmp[i]

    ##print(arr)
    return arr


def merge_sort(arr):
    return merge_sort_part(arr, 0, len(arr) - 1)


def merge_sort_part(arr, p, r):
    if p >= r:
        return

    # 计算中间点 // 除法是整数
    q = (p + r) // 2

    merge_sort_part(arr, p, q)
    merge_sort_part(arr, q + 1, r)

    return merge(arr, p, q, r)


if __name__ == '__main__':
    arr = [2, 10, 4, 11, 1, 3]
    print(merge_sort(arr))
    # for i in range(0,10):
    #     print(i)
