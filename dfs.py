# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import math
"""
Basic Algorithms using DFS
"""


class DFS(object):

    def dfs_2d(self, matrix, flag, i, j):
        direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        m, n = matrix.shape
        if 0 <= i < m and 0 <= j <n:
            for d in direction:
                if 0 <= i+d[0] < m and  0 <= j+d[1] < n:
                    if not flag[i+d[0]][j+d[1]] and matrix[i+d[0]][j+d[1]] >= matrix[i][j]:
                        flag[i+d[0]][j+d[1]]=1
                        self.dfs_2d(matrix, flag, i+d[0], j+d[1])
    
    
    def dfs_1d(self, arr, flag, cur_i, count):
        # implement by recursive way
        if flag[cur_i] > 0:  # already visit
            return flag
    
        flag[cur_i] = count
        for j in range(arr.shape[0]):
            if flag[j] or j == cur_i or not arr[cur_i][j]:
                continue
            flag = self.dfs_1d(arr, flag, j, count)  # dfs friend j
        return flag
    

    def pacificAtlantic(self, matrix):
       """
       :type matrix: List[List[int]]
       :rtype: List[List[int]]
       """
       if matrix==None or len(matrix)==0:
           return []
       matrix = np.array(matrix)
       m, n = matrix.shape
       pacificFlag = np.zeros((m, n), dtype=int)
       atlanticFlag = np.zeros((m, n), dtype=int)
       for i in range(m):
           pacificFlag[i][0] = 1
           atlanticFlag[i][n-1] = 1
           self.dfs_2d(matrix, pacificFlag, i, 0)
           self.dfs_2d(matrix, atlanticFlag, i, n-1)
       for j in range(n):
           pacificFlag[0][j] = 1
           atlanticFlag[m-1][j] = 1
           self.dfs_2d(matrix, pacificFlag, 0, j)
           self.dfs_2d(matrix, atlanticFlag, m-1, j)
           
       res = []
       for i in range(m):
           for j in range(n):
               if pacificFlag[i][j] and atlanticFlag[i][j]:
                   res.append([i, j])
       return res
                

    def findCircleNum(self, M):
        """
        :type M: List[List[int]]
        :rtype: int
        """
        # matrix.shape
        if not M:
            return 0
        arr = np.array(M)  # convert forcely
        flag = np.zeros(arr.shape[0], dtype=int)
        count = 0
        for i in range(arr.shape[0]):
            if flag[i] < 1:
                count += 1
            flag = self.dfs_1d(arr, flag, i, count)
    
        return count


if __name__ == "__main__":
    # test friend_circle
    # arr = [[1, 1, 0],
    #        [1, 1, 0],
    #        [0, 0, 1]]
    dfs = DFS()
    arr = [[]]
    res_circle = dfs.findCircleNum(arr)
    print('Result of find friend circles: %d' % res_circle)

    mat = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    res_pacific = dfs.pacificAtlantic(mat)
    print("Result of pacific atlantic: %s" % str(res_pacific))
