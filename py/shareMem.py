from ctypes import *

#windll.kernel32.SetLastError(-100)


dataDict = {
    'X':0,
    'Y':1,
    'H':2,
    'alpha':3,
    'beta':4,
    'Vt':5,
    'phi':6,
    'theta':7,
    'psi':8,
    'p':9,
    'q':10,
    'r':11,
    'acceptState':13,
    'programeControlState':14,
    'send': 15
}


FILE_MAP_ALL_ACCESS = 0xF001F    # 读写
class getShareMemData(object):
    def __init__(self, szName = "szName", sizeof = 1024):
        self.szName = szName   # 共享内存标识符，要与创建处保持一致，不然打不开
        self.size = sizeof    # 共享内存大小，可以不保持一致，但必须小于创建处
        self.ret = 0          # 全局错误代码，一般正确为0，出错为-1 -2
        self.get_double_array =None   # 接受共享内存数据的数组 其类型为 数列
        self.checkFunction()


    def checkFunction(self):
        '''
        测试winAPI是否可用
        可用返回0，不可用返回-1
        :return:
        '''
        checkResult = windll.kernel32.GetLastError()
        if checkResult == 0:
            self.ret = 0
            print("打开函数成功")
        else:
            self.ret = -1
            print("打开函数windll.kernel32失败")
            return -1

    def openShareMem(self):
        '''
        打开共享内存函数
        首先打开内存，若成功，则把内存映射成self.get_double_array（数据类型为列表）
        即self.get_double_array[0]为内存中第一个数据，self.get_double_array[1]为第二个，
        此时读内存数据，例如读第一个数据为a则直接为a = self.get_double_array[0]
        写入内存数据，例如写入第一个数据为 9 ， self.get_double_array[0] = 9
        :return:
        '''
        #getfunc = windll.kernel32.CreateFileMappingW     #调用创建内存的函数，测试发成错误。
        getfunc = windll.kernel32.OpenFileMappingW        # 调用打开共享内存的函数，以下使用getfunc，即为打开内存
        getfunc.restype = c_void_p                        #由于本身该函数返回值为viod* ， 则此处必须设置其返回值为c_void_p
        self.handle = getfunc(FILE_MAP_ALL_ACCESS,False, str(self.szName))
        if self.handle == None:
            self.ret = -1
            print("打开共享内存失败")
            return -1
        else:
            self.ret = 0
            print("打开共享内存成功")
            mapView = windll.kernel32.MapViewOfFile
            self.get_double_array = POINTER(c_double)
            mapView.restype = POINTER(c_double)
            self.get_double_array = mapView(self.handle, FILE_MAP_ALL_ACCESS, 0, 0, self.size)
            if self.get_double_array != None:
                self.ret = 0
                print("打开内存指针成功")
            else:
                self.ret = -2
                return -2


    def readOrWriteData(self,key, n, *flag):
        '''
                读入指定的一个数据或者写入在指定数据
                参数：
                key :   'X':0,'Y':1,'H':2,'alpha':3,'beta':4,'Vt':5,
                        'phi':6,'theta':7,'psi':8,'p':9,'q':10,'r':11
                n   : 'r' 读  'w': 写
                *flag:  如果为'w',则该参数为写入的数据
                返回：
                    如果为读取数据： 读取成功返回读取的数据 ，
                    如果为写入数据：返回0 代表读取成功
                '''

        if (n not in ('r','w')) or key not in dataDict.keys() :
            print("参数错误：not is 'r' or 'w' 或者 获取数据未在字典里面")
            return -1

        if n == 'r' and self.ret ==0 :

            x_double = self.get_double_array[dataDict[key]]  # 读取数据
            return x_double
        elif n == 'w':
            self.get_double_array[dataDict[key]] = flag[0]
            return 0

    def readAll(self):
        '''
            读取共享内存中所有的数据，不具有写入功能
            返回数据列表 若读取失败则返回 -1
        :return:
        '''
        if self.get_double_array != None:
            self.ret = 0
            print("打开内存指针成功")
            return self.get_double_array
        else:
            self.ret = -1
            return -1


    def closeShareMem(self):
        '''
        关闭共享内存，方法存疑
        '''
        if self.get_double_array != None:
            self.get_double_array = None
            print("释放指针成功")
        if self.handle !=None:
            self.handle = None

'''
if __name__ == '__main__':
    szName = 'szName'
    size = 1024
    mem = getShareMemData(szName,size)
    mem.openShareMem()
    data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    while(1):
        data = mem.readShareMem()
        if mem.ret == 0:
            for i in range(5):
                print("%.2f      " % float(data[i]),end='')
            print("")

if __name__ == '__main__':
    i = 0
    dataList = []
    szName = 'szName'
    size = 1024
    get = getShareMemData(szName,size)
    get.openShareMem()
    list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    while (1):
        ret = get.openShareMem()
        list = get.readAll()
        if ret == 0:
            for i in range(5):
                print("%.2f      " % float(list[i]), end='')
            print("")
            get.readOrWriteData('send', 'w', 1)

        else:
            print("打开失败")

        get.closeShareMem()
'''