import numpy as np
class Solution(object):
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
    
    def findCircleNum(self, M):
        """
        :type M: List[List[int]]
        :rtype: int
        """
        # import pdb; pdb.set_trace()
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
    s = Solution()
    #arr = [[1,1,0],[1,1,0],[0,0,1]]
    arr = [[1,0,0,1],
           [0,1,1,0],
           [0,1,1,1],
           [1,0,1,1]]
    print s.findCircleNum(arr)
