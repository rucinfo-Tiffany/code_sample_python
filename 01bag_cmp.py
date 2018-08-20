#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:24:20 2018

@author: zhangyaxuan

Basic Algorithms using backtrack
经典0-1背包问题：假设山洞里共有a,b,c,d ,e这5件宝物（不是5种宝物），它们的重量分别是2,2,6,5,4，它们的价值分别是6,3,5,4,6，现在给你个承重为10的背包, 怎么装背包，可以才能带走最多的财富。
"""

bestV=0
curW=0
curV=0
bestx=None

def backtrack_01bag(i):
    """01背包问题（回溯法，注意全局变量）"""
    global bestV,curW,curV,x,bestx
    if i>=n:
        if bestV<curV:
            bestV=curV
            bestx=x[:]
    else:
        if curW+w[i]<=c:
            x[i]=True
            curW+=w[i]
            curV+=v[i]
            backtrack_01bag(i+1)
            curW-=w[i]
            curV-=v[i]
        x[i]=False
        backtrack_01bag(i+1)

def dp_01bag(n,c,w,v):
    """01背包问题（动态规划）"""
    res=[[-1 for j in range(c+1)] for i in range(n+1)]
    for j in range(c+1):
        res[0][j]=0
    for i in range(1,n+1):
        for j in range(1,c+1):
            res[i][j]=res[i-1][j]
            if j>=w[i-1] and res[i][j]<res[i-1][j-w[i-1]]+v[i-1]:
                res[i][j]=res[i-1][j-w[i-1]]+v[i-1]
    return res


if __name__=='__main__':
    n=5
    c=10
    w=[2,2,6,5,4]
    v=[6,3,5,4,6]
    x=[False for i in range(n)]
    backtrack_01bag(0)
    print(bestV)
    print(bestx)

    """01背包"""
    res = dp_01bag(n,c,w,v)
    print(res)
