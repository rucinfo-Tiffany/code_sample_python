# -*- coding: utf-8 -*-
from __future__ import print_function
import Queue
import numpy as np
"""
Basic Algorithms using BFS
"""
def find_shortest_path(arr, target_i, target_j):
    """
    the shorted path from (0, 0) to (i, j)
        [[1,1,0,1],
        [1,0,1,0],
        [1,1,1,1],
        [1,0,1,1]]"""
    arr = np.array(arr)  # convert arr to an array
    flag = np.zeros(arr.shape, dtype=bool)
    direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    queue = Queue.Queue()
    queue.put((0, 0, 0))
    while not queue.empty():
        cur_pos = queue.get()
        for drt in direction:
            i, j, step = cur_pos[0] + drt[0], cur_pos[1] + drt[1], cur_pos[2] + 1
            if i == target_i and j == target_j:
                return step
            if (0 <= i < arr.shape[0]) and (0 <= j < arr.shape[1]) and not flag[i][j]:
                queue.put((i, j, step))
                flag[i][j] = True
    return -1

if __name__ == "__main__":
    arr = np.array([[1,1,0,1], [1,0,1,0],[1,1,1,1],[1,0,1,1]])
    # import pdb;pdb.set_trace()
    step = find_shortest_path(arr, 3, 2)
    print('shorted steps: %d' % step)


