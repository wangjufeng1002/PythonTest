#!/usr/bin/env python
# coding=utf-8

# 快速排序 O(nlogn)


def quick_sort(arr):
    quick_sort_part(arr, 0, len(arr) - 1)


def quick_sort_part(arr, p, r):
    if p >= r:
        return

    q = partition(arr, p, r)

    quick_sort_part(arr, p, q - 1)
    quick_sort_part(arr, q + 1, r)



def partition(arr, p, r):

    pivot = arr[r]
    i = p
    for j in range(p, r):
        # i 始终指向在比 pivot 大的数值上。（碰到比pivot 小的数字，i 才会往后移动，碰到比pivot大的数字后，i 会停止移动）
        if arr[j] < pivot:
            tmp = arr[i]
            arr[i] = arr[j]
            arr[j] = tmp
            i = i + 1
        print(arr)

    tmp = arr[i]
    arr[i] = arr[r]
    arr[r] = tmp
    return i


if __name__ == '__main__':
    arr = [6, 11, 12, 9, 8]
    quick_sort(arr)

    print(arr)
