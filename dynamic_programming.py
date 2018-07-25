# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
"""
Basic Algorithms using DFS
"""


class DP(object):

    def dp(self, v, total):
        n = len(v)
        mat = np.zeros((n, total + 1), dtype=bool)

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
        mat = np.zeros((n, total + 1), dtype=bool)

        if total == 0 or v[0] == total:
            return True
        mat[0][0] = True
        if v[0] <= total:
            mat[0][v[0]] = True

        for i in range(1, n):
            mat[i][0] = True
            for j in range(total + 1 - v[i]):
                mat[i][j] = mat[i-1][j]
                if mat[i-1][j]:
                    if j + v[i] == total:
                        return True
                    else:
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

    arr = [1, 5, 11, 5]
    res = dp.canPartition(arr)
    print("Result of partition subsets: %s" % str(res))
