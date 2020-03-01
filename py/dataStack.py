# -*- coding: utf-8 -*-


class queue(object):
    # 为一个队列数据结构，先进后出
    def __init__(self, size):
        self.size = size
        self.queueList = [0] * size
        self.num = 0
        self.allNum = 0

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
        if self.num < self.size:
            self.push(data)
            self.pop()
            self.num += 1
            self.allNum += 1
        else:
            if self.allNum > 2000:
                self.push(data)
                self.pop()
                self.allNum += 1
            else:
                self.push(data)
                self.allNum += 1

    def redata(self):
        # 功能，初始化队列，即把队列更新为30个0
        del self.queueList
        self.queueList = [0] * self.size
        self.allNum = 30
        self.num = 0

    def savaData(self):
        # 功能： 截取原本队列的最后30个数值。为了画图时清空数据，和上面函数配合使用
        self.queueList = self.queueList[-self.size:]
        self.allNum = 30
        self.num = 0


"""
if __name__ == "__main__":
    num = queue(20)
    for i in range(100):
        num.fun(i)
        # print(num.queueList)
"""
