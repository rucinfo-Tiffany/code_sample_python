# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
"""
Basic Algorithms using DP Mind
回溯法，经典问题，N皇后问题
"""


class Backtrack(object):

    def canPartitionKSubsets(self, v, total):
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



if __name__ == "__main__":

    bt = Backtrack()

    arr = [1,1,1,1]
    res = bt.canPartitionKSubsets(arr, 4)
    print("Result of partition subsets: %s" % str(res))
