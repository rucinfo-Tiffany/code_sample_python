# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
import heapq
import random
"""
Basic Sort Algorithms - 经典排序苏算法
"""


class BasicSort(object):

    def quicksort(self, arr):
        # 快速排序
        arr = np.array(arr)  # in case of shallow copy
        self.qsort(arr, 0, arr.shape[0] - 1)
        return arr

    def qsort(self, arr, low, high):
        if low >= high:
            return
        pos = self.partition(arr, low, high)
        self.qsort(arr, low, pos - 1)
        self.qsort(arr, pos + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[low]
        while low < high:
            while low < high and arr[high] > pivot:
                high -= 1
            arr[high], arr[low] = arr[low], arr[high]
            while low < high and arr[low] < pivot:
                low += 1
            arr[high], arr[low] = arr[low], arr[high]
        return low

    def bubblesort(self, arr):
        # 冒泡排序
        arr = np.array(arr)
        len_arr = len(arr)
        for i in range(len_arr - 1):
            for j in range(i+1, len_arr):
                if arr[j] < arr[i]:
                    arr[i], arr[j] = arr[j], arr[i]
        return arr

    def selectsort(self, arr):
        # 最简单的选择排序
        arr = np.array(arr)
        len_arr = len(arr)
        for i in range(len_arr - 1):
            min_j, min_val = i, arr[i]
            for j in range(i + 1, len_arr):
                if arr[j] < min_val:
                    min_j, min_val = j, arr[j]
            arr[i], arr[min_j] = arr[min_j], arr[i]
        return arr

    def _merge(self, arr, left, right, mid):
        # 将left~mid, mid~right两部分merge成一个有序数组
        if left >= right:
            return
        print("merge\t\t", arr, left, right, mid)
        low, high = left, mid + 1
        cur = left
        new_arr = arr
        while low < high and low <= mid and high <= right:
            if arr[low] > arr[high]:
                new_arr[cur] = arr[high]
                high += 1
            else:  # low <= high
                new_arr[cur] = arr[low]
                low += 1
            cur += 1
        if low <= mid:
            for i in range(low, mid + 1):
                new_arr[cur] = arr[i]
                cur += 1
        if high <= right:
            for j in range(high, right + 1):
                new_arr[cur] = arr[i]
                cur += 1
        arr = new_arr
        return

    def _mergesort(self, arr, left, right):
        print("mergesort\t", arr, left, right)
        if left < right:
            mid = int((left + right)/2)
            self._mergesort(arr, left, mid)
            self._mergesort(arr, mid+1, right)
            self._merge(arr, left, right, mid)


    def mergesort(self, arr):
        # 归并排序
        arr = np.array(arr)
        self._mergesort(arr, 0, arr.shape[0]-1)
        return arr




if __name__ == "__main__":
    bs = BasicSort()
    arr = [random.randint(0, 100) for i in range(10)]
    print("Before Sort: \t", arr)

    print("After QuickSort: \t", bs.quicksort(arr))

    print("After BubbleSort: \t", bs.bubblesort(arr))

    print("After SelectSort: \t", bs.selectsort(arr))

    print("After MergeSort: \t", bs.mergesort(arr))



