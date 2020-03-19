"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-27 04:26:44  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-27 04:26:44  
* @function:   多线程
"""
# -*- coding: utf-8 -*-
from time import sleep, time
from PyQt5.QtCore import QThread, pyqtSignal
from GetDataFromShareMem import getShareMemData  # .so为底层
# from shareMem import getShareMemData              # py直接调用win的API作为底层


# 更新绘图线程
class FigQThread(QThread):
    finished_signal = pyqtSignal(bool)

    def __init__(self, rest, obj_ui, parent=None):
        super().__init__(parent)
        self.obj_ui = obj_ui
        self._rest = rest
        self.time1 = 0
        self.closeThread = False

    def run(self):
        while True:
            if self.closeThread == False:
                # self.time2 = self.time1
                # self.time1 = time()
                # print("进入线程2：%0.4f" % (self.time1 - self.time2))
                self.obj_ui.readData_UpFigure_UpState()
                # self.finished_signal.emit(True)
                sleep(self._rest)
            else:
                # print("子线程退出来了")
                break

# 更新地图线程
class MapQThread(QThread):
    finished_map_signal = pyqtSignal(bool)
    def __init__(self, rest, obj_ui, parent=None):
        super().__init__(parent)
        self.obj_ui = obj_ui
        self._rest = rest
        self.time1 = 0
        self.closeThread = False

    def run(self):
        while True:
            if self.closeThread == False:
                # self.time2 = self.time1
                # self.time1 = time()
                # print("进入线程2：%0.4f" % (self.time1 - self.time2))
                self.obj_ui.updataMap()
                # self.finished_signal.emit(True)
                sleep(self._rest)
            else:
                # print("子线程退出来了")
                break

