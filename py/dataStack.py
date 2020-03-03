# -*- coding: utf-8 -*-
from copy import deepcopy

class queue(object):
    # 为一个队列数据结构，先进后出
    def __init__(self, size, allLen):
        self.size = size
        self.queueList = [0] * size
        self.newNum = 0                 # 加入的新数据的数量
        self.allNum = size                 # 所有数列数据的数量
        self.allLen = allLen            # 满队列的数量

    def push(self, data):
        # 加入一个数据
        self.queueList.append(data)
        return data

    def pop(self):
        # 删除最前面的数据
        return self.queueList.pop(0)

    def len(self):
        # 返回长度
        return len(self.queueList)

    def updata(self, data):
        # 用于画图时，数据更新
        # 思路为： 如果队列长度不超过2000，则一直加入，不删除最前面的
        #        如果超过2000，则加入新的，删除最前面的
        if self.newNum < self.size:
            self.push(data)
            self.pop()
            self.newNum += 1
        else:
            if self.allNum > self.allLen:
                self.push(data)
                self.pop()
            else:
                self.push(data)
                self.allNum += 1
                # print("self.allNum", self.allNum)

    def redata(self, newListLen):
        # 功能，初始化队列，即把队列更新为0
        if self.len() > newListLen:
            del self.queueList
            self.queueList = [0]*newListLen
            
            self.allNum = newListLen
            self.newNum = 0


    def savaData(self, newListLen):
        # 功能： 截取原本队列的最后2个数值。为了画图时清空数据，和上面函数配合使用
        if self.len() > newListLen:
            self.queueList = self.queueList[-newListLen:]
            self.newNum = 0
            self.allNum = 0

    # def threeDDataUpdata(self, newListLen):
    #     if self.len() > newListLen:
    #         q = self.queueList[-newListLen:]
    #         num = self.len() - len(q)
    #         del self.queueList
    #         self.queueList = [0] * num
    #         self.queueList.extend(q)
    #         print(len(self.queueList))






"""
if __name__ == "__main__":
    num = queue(20)
    for i in range(100):
        num.fun(i)
        # print(num.queueList)
"""
