# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
"""
Basic Algorithms using DFS
"""


def dfs_2d(arr, flag, cur_i, cur_j, count):
    #  TODO: to implement
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    for drt in directions:
        i, j = cur_i + drt[0], cur_j + drt[1]
        if flag[i][j] > 0:  # already visit
            return
        if 0 <= i < arr.shape[0] and 0 <= j < arr.shape[1] and arr[i][j]:
            return


def dfs_1d(arr, flag, cur_i, count):
    if flag[cur_i] > 0:
        return flag
    stack = [cur_i]
    while len(stack) > 0:
        for j in range(arr.shape[0]):
            if flag[j] or not arr[cur_i][j]:
                continue
            flag[j] = count
            stack.append(j)
        stack = stack[1:]
    return flag


def find_friend_circles(arr):
    """
    [[1,1,0],
     [1,1,0],
    [0,0,1]]
    findout how many friend circles are there in the arr (direct friend or indirect)
    """
    arr = np.array(arr)  # convert forcely
    flag = np.zeros(arr.shape[0], dtype=int)
    count = 1
    stack = []
    stack.append(0)
    for i in range(arr.shape[0]):
        flag = dfs_1d(arr, flag, i, count)
        count += 1

    return count - 1


if __name__ == "__main__":
    # test friend_circle
    arr = [[1, 1, 0],
           [1, 1, 0],
           [0, 0, 1]]
    res_circle = find_friend_circles(arr)
    print('Result of find friend circles: %d' % res_circle)

