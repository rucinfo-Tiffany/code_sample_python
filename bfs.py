# -*- coding: utf-8 -*-
from __future__ import print_function
import Queue
import numpy as np
import math
"""
Basic Algorithms using BFS
"""


class BFS(object):

    def find_shortest_path(self, arr, target_i, target_j):
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
    
    
    def num_squares(self, n):
        """
        return the least number of square number which sum up to n
        equals to: find the shortes path between 0 to n
        """
        sqr_list = self.gen_squares(n)
        queue = Queue.Queue()
        queue.put((0, 0))
        flag = np.zeros(n, dtype=bool)
    
        while not queue.empty():
            cur_pos = queue.get()
            cur_num, step = cur_pos[0], cur_pos[1]
            for sqr_num in sqr_list:
                new_num = cur_num + sqr_num
                if new_num == n:
                    return step + 1
                elif new_num > n:  # exceed target n, break for loop
                    break
                elif new_num < n and not flag[new_num]:
                    queue.put((new_num, step + 1))
                    flag[new_num] = True
        return "Error. No number n has no return"
    
    
    def gen_squares(self, n):
        """return all square number below n"""
        sqr_list = []
        i = 1
        while i * i <= n:
            sqr_list.append(i*i)
            i += 1
        return sqr_list


if __name__ == "__main__":
    # test find_shortest_path
    bfs = BFS()
    arr = np.array([[1, 1, 0, 1], [1, 0, 1, 0], [1, 1, 1, 1], [1, 0, 1, 1]])
    # import pdb;pdb.set_trace()
    step = bfs.find_shortest_path(arr, 3, 2)
    print('shorted steps: %d' % step)

    # test num_squares
    for i in range(100):
        print('%d\t%s' % (i, str(bfs.num_squares(i))))
