"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-27 04:26:44  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-27 04:26:44  
* @function:   多线程
"""
# -*- coding: utf-8 -*-
import time
from PyQt5.QtCore import QThread, pyqtSignal
from GetDataFromShareMem import getShareMemData  # .so为底层
# from shareMem import getShareMemData              # py直接调用win的API作为底层
from ctypes import *


class getDataQThread(QThread):
    finished_signal = pyqtSignal(list)

    def __init__(self, rest, getShare, parent=None):
        super().__init__(parent)
        self._rest = rest
        self._getShare = getShare
        self.para = [0.1, 0.0, 0.0, 0.0]
        self.time1 = 0

    def run(self):
        while True:
            self.time2 = self.time1
            self.time1 = time.time()
            # print("进入线程1：%0.4f" % (self.time1 - self.time2))

            data = self._getShare.readAll()
            time.sleep(self._rest)
            self.finished_signal.emit(
                [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                 data[10], data[11], data[12], data[13], data[14], data[15]])


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
                # self.time1 = time.time()
                # print("进入线程2：%0.4f" % (self.time1 - self.time2))
                self.obj_ui.readData_UpFigure_UpState()
                # self.finished_signal.emit(True)
                time.sleep(self._rest)
            else:
                # print("子线程退出来了")
                break


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
                # self.time1 = time.time()
                # print("进入线程2：%0.4f" % (self.time1 - self.time2))
                self.obj_ui.updataMap()
                # self.finished_signal.emit(True)
                time.sleep(self._rest)
            else:
                # print("子线程退出来了")
                break
