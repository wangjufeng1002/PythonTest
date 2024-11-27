#!/usr/bin/env python
# coding=utf-8

# 二分查找

def binary_search(arr, value):
    low = 0
    high = len(arr) - 1

    while low <= high:
        # mid = (low + high) // 2
        # mid = low + (high - low) // 2
        mid = low + ((high - low) >> 1)
        if arr[mid] == value:
            return mid
        elif arr[mid] < value:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# 二分查找，递归实现
def binary_search_recursion(arr, value, low, high):
    if low is None or high is None:
        low = 0
        high = len(arr) - 1

    if low > high:
        return -1

    mid = low + ((high - low) >> 1)
    if arr[mid] == value:
        return mid
    elif arr[mid] < value:
        low = mid + 1
    else:
        high = mid - 1

    return binary_search_recursion(arr, value, low, high)


# 查找第一个值等于给定值的元素
def binary_search_first(arr, value):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + ((high - low) >> 1)
        if arr[mid] > value:
            high = mid - 1
        elif arr[mid] < value:
            low = mid + 1
        else:
            if mid == 0 or arr[mid - 1] != value:
                return mid
            high = mid - 1

    return -1


# 查找最后一个值等于给定值的元素
def binary_search_last(arr, value):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + ((high - low) >> 1)
        if arr[mid] > value:
            high = mid - 1
        elif arr[mid] < value:
            low = mid + 1
        else:
            if mid == 0 or arr[mid + 1] != value:
                return mid
            low = mid + 1
    return -1


# 查找第一个大于等于给定值的元素
def binary_search_first_GT_EQ(arr, value):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + ((high - low) >> 1)
        if arr[mid] < value:
            low = mid + 1
        else:
            if mid == 0 or (arr[mid - 1] < value):
                return mid
            high = mid - 1
    return -1


# 查找最后一个小于等于给定值的元素
def binary_search_last_LET_EQ(arr, value):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + ((high - low) >> 1)
        if arr[mid] > value:
            high = mid - 1
        else:
            if mid == 0 or (arr[mid + 1] > value):
                return mid
            low = mid + 1
    return -1


# 旋转数组，先找到旋转中心，将数组一分为二，再次使用二分查找在其中某一个区间中查找
# 4，5，6，1，2，3
def binary_search_circle(arr, value):
    low = 0
    high = n = len(arr) - 1
    if arr[low] == value:
        return low
    if arr[high] == value:
        return high
    while low <= high:
        # 计算中间下标
        mid = low + ((high - low) >> 1)
        if arr[mid] == value:
            return mid

        # 如果 arr[mid] >= arr[0] 说明分割点在 mid 右侧 ,mid左侧为有序，mid右侧可能为无序
        if arr[0] <= arr[mid]:
            # 如果 目标值在 [0,mid) 之间，hight 向左移动
            if arr[mid] > value >= arr[0]:
                high = mid - 1
            # 否则 目标值应在存在于 (mid,n] low 向右移动
            else:
                low = mid + 1
        # 如果
        else:
            # 如果 目标值在 (mid,n] 之间，low 向右移动
            if arr[mid] < value <= arr[n]:
                low = mid + 1
            # 否则 目标值应在存在于 [0,mid) high 向右移动
            else:
                high = mid - 1
    return -1


if __name__ == '__main__':
    # print(binary_search([1, 3, 4, 5, 6, 7, 8, 9, 10], 9))

    # print(binary_search_last_LET_EQ([1, 3, 3, 5, 6, 7, 8, 9, 10], 3))
    print(binary_search([6, 5, 7, 1, 2], 1))
