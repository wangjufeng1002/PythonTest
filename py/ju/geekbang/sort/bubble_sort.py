#!/usr/bin/env python
# coding=utf-8

# 冒泡排序 属于线性排序

def bubble_sort(arr):
    if len(arr) <= 0:
        return
    for i in range(0, len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j + 1]
                arr[j + 1] = arr[j]
                arr[j] = temp
    print(arr)


if __name__ == '__main__':
    print(bubble_sort([8, 1, 0, 3, 5, 2]))
