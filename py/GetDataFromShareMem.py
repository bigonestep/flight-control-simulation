# -*- coding: utf-8 -*-
"""
* @Author: Wang.Zhihui
* @Date: 2020-02-26 01:35:22
* @Last Modified by:   Wang.Zhihui
* @Last Modified time: 2020-02-26 01:35:22
* @function: 获取数据
"""


from ctypes import CDLL, POINTER, c_double, c_int


data = {
    'X': 0, 'Y': 1, 'H': 2, 'alpha': 3, 'beta': 4, 'Vt': 5,
    'phi': 6, 'theta': 7, 'psi': 8, 'p': 9, 'q': 10, 'r': 11,
    # 'acceptState':13, 'programeControlState':14, 'send': 15
    'acceptFlightStatus': 13, 'acceptModel': 14, 'acceptEngineStatus': 15,
    'send': 16,
    'sedClimb1Theta': 20, 'setClimb2Theta': 21, 'setDecline1Theta': 22, 
    'setDecline2Theta': 23, 'setHight': 24, 'setTurnLeftPsi':25,
    'setTurnRightPsi':26
}


class getShareMemData(object):
    def __init__(self, szName):
        self.ret_int = 0
        self.szName = szName
        self.pylib = None
        self.get_double_array = None

    def openShareMem(self):
        self.pylib = CDLL(r'./getShareData.so')
        self.ret_int = self.pylib.getMem(self.szName)
        if self.ret_int == -1:
            # print("共享内存打开失败")
            return -1
        elif self.ret_int == -2:
            # print("共享内存指针错误")
            return -2
        else:
            # print("打开共享内存成功")
            return 0

    def closeShareMem(self):
        if self.ret_int == 0:
            self.pylib.closeMem()
            # print("释放成功")

    def readOrWriteData(self, key, n, *flag):  # x   double R(void);
        # '''
        # 参数：
        # key :   'X':0,'Y':1,'H':2,'alpha':3,'beta':4,'Vt':5,
        #         'phi':6,'theta':7,'psi':8,'p':9,'q':10,'r':11
        # n   : 'r' 读  'w': 写
        # *flag:  如果为'w',则该参数为写入的数据
        # 返回：
        # 'r': 返回读取的数据，或者错误代码
        # 'w': 返回错误代码
        # '''
        # # print("n:", n, 'key:',key)
        if (n not in ('r', 'w')) or key not in data.keys():
            # print("参数错误：not is 'r' or 'w' 或者 获取数据未在字典里面")
            return -1
        if n == 'r':
            double_ret = self.pylib.readData
            double_ret.restype = c_double     # 定义函数返回值
            x_double = double_ret(data[key])  # 读取数据

            if int(x_double) != -1:  # 说明读取失败
                return x_double
            else:
                # print("读取数据失败")
                return -1  
        elif n == 'w':

            flag_double = c_double(flag[0])
            double_ret = self.pylib.writeData
            # double_ret.restype = c_int            # 定义返回值，为整数则不用写
            double_ret.argtypes = [c_int, c_double]  # 定义函数参数
            ret_flag = double_ret(data[key], flag_double)

            # '''
            # ret_flag : 0 成功
            # ret_flag: -1 参数错误：not is 'r' or 'w' 或者 获取数据未在字典里面
            # ret_flag: -2 共享内存指针错误
            # '''

            if ret_flag != 0:
                print("写入数据失败")
            else:
                
                print("写入数据成功")
            return ret_flag
    
    def readAll(self):
        double_list = self.pylib.readAllParam
        self.get_double_array = POINTER(c_double)
        double_list.restype = POINTER(c_double)
        self.get_double_array = double_list()
        return self.get_double_array


# if __name__ == '__main__':
#     i = 0
#     dataList = []
#     get = getShareMemData()
#     get.openShareMem()
#     data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
#     while(1):
#         get = getShareMemData()
#         ret= get.openShareMem()
#         data = get.readAll()
#         if ret == 0:
#             for i in range(5):
#                 print("%.2f      " % float(data[i]),end='')
#             print("")
            
#         else:
#             print("打开失败")
#         get.closeShareMem()

