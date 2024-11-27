#!/usr/bin/env python
# coding=utf-8

# 插入排序 O(nlogn)


def insertion_sort(arr):
    if len(arr) <= 1:
        return

    for i in range(1, len(arr)):
        value = arr[i]
        j = i - 1

        # 查找插入位置
        while j >= 0:
            # arr 中的数字比 value 大时，整体后移，给准备插入的值空出位置
            if arr[j] > value:
                arr[j + 1] = arr[j]
                j = j - 1
            else:
                break
        arr[j + 1] = value
        print(arr)
    print(arr)


if __name__ == '__main__':
    insertion_sort([1, 4, 0, 3, 5, -1])
