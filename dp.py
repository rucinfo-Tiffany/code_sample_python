# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
"""
Basic Algorithms using DP Mind
经典0-1背包问题：假设山洞里共有a,b,c,d ,e这5件宝物（不是5种宝物），它们的重量分别是2,2,6,5,4，它们的价值分别是6,3,5,4,6，现在给你个承重为10的背包, 怎么装背包，可以才能带走最多的财富。
"""


class DP(object):

    def dp(self, v, total):
        n = len(v)
        mat = np.zeros((n, total + 1), dtype=np.bool_)

        mat[0][0] = True
        if v[0] <= total:
            mat[0][v[0]] = True

        for i in range(1, n):
            mat[i][0] = True
            for j in range(total + 1 - v[i]):
                mat[i][j] = mat[i-1][j]
                if mat[i-1][j] and j + v[i] <= total:
                    mat[i][j+v[i]] = True

        return mat[n-1][total]


    def dp_trim(self, v, total):
        n = len(v)
        mat = np.zeros((n, total + 1), dtype=bool)  # dtype=bool will throw error on leetcode!

        if total == 0 or v[0] == total:
            return True
        mat[0][0] = True
        if v[0] <= total:
            mat[0][v[0]] = True

        for i in range(1, n):
            mat[i][0] = True
            # import pdb; pdb.set_trace()
            for j in range(total):
                if mat[i-1][j]:  # i-1 can sum up to j
                    if j + v[i] == total:
                        return True
                    mat[i][j] = True
                    if j + v[i] < total:
                        mat[i][j+v[i]] = True

        return mat[n-1][total]

        
    def canPartition(self, nums):
        """
        leetcode 416: https://leetcode.com/problems/partition-equal-subset-sum/description/
        :type nums: List[int]
        :rtype: bool
        """
        if sum(nums) % 2 == 1:
            return False
        return self.dp_trim(nums, sum(nums)//2)



if __name__ == "__main__":

    dp = DP()

    arr = [1,1,1,1]
    res = dp.canPartition(arr)
    print("Result of partition subsets: %s" % str(res))

    k = 4
    res2 = dp.canPartitionKSubsets(arr, k)
    print("result of partition k subsets: %s" % str(res2))
