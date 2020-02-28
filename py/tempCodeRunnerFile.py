if __name__ == '__main__':
    i = 0
    dataList = []
    get = getShareMemData()
    get.openShareMem()
    data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    while(1):
        get = getShareMemData()
        ret= get.openShareMem()
        data = get.readAll()
        if ret == 0:
            for i in range(5):
                # print("%.2f      " % float(data[i]),end='')
            # print("")
            
        else:
            # print("打开失败")
        get.closeShareMem()