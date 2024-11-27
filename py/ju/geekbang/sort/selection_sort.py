#!/usr/bin/env python
# coding=utf-8

# 选择排序


def selection_sort(arr):
    if len(arr) <= 1:
        return

    # 每次选择一个最小的放到已排序区间
    for i in range(0, len(arr)):
        min_index = i
        for j in range(i, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        temp = arr[i]
        arr[i] = arr[min_index]
        arr[min_index] = temp
    print(arr)


if __name__ == '__main__':
    selection_sort([2, 3, 1, 0, 4])
