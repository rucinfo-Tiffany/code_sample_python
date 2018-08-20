# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
import heapq
import random
"""
Basic Algorithms using Heap
"""


class Heap(object):

    def find_k_largest(self, arr, k):
        heap = []
        for num in arr:
            heapq.heappush(num)
        return heapq.nlargest(k, heap)[-1]

    def find_k_smallest(self, arr, k):
        heap = []
        for num in arr:
            heapq.heappush(num)
        return heapq.nsmallest(k, heap)[-1]

    def find_k_largest_with_limit(self, arr, k):
        heap = []
        for num in arr:
            if len(heap) >= k:
                min_num = heapq.heappop(heap)
                heapq.heappush(max(min_num, num), heap)
            else:
                heapq.heappush(num, heap)
        return heapq.heappop(heap)


if __name__ == "__main__":

    hp = Heap()
    arr = [random.randint(0, 100) for i in range(15)]
    print(hp.find_k_largest_with_limit(arr, 5))
