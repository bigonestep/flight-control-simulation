# -*- coding: utf-8 -*-
"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-26 02:08:04  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-26 02:08:04  
* @function:  联合仿真界面
"""
from os import system, path
import sys
from time import time, sleep
from win32con import KEYEVENTF_KEYUP
from win32gui import SetForegroundWindow
from win32api import ShellExecute, keybd_event
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QMessageBox,
                             QInputDialog, QLineEdit, QFileDialog)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal, QTimer, QMargins, QCoreApplication,
                          Qt, QT_VERSION_STR, QVersionNumber, QMutex, QDir)
from PyQt5.QtGui import QFont, QPixmap
from numpy import linspace 
import matplotlib.image as img
from urllib.request import urlopen
from urllib.error import URLError
from ui_MainRhapsody import Ui_MainRhapsody
from GetDataFromShareMem import getShareMemData   # .so为底层
# from shareMem import getShareMemData              # py直接调用win的API作为底层
# from myFigureCanvas import QmyFigureCanvas
from dataStack import queue
from buttonFunc import buttonFunc
from ledFunc import (ledFlightFunc, ledEngineFunc, ledModelFunc)
from conf import (ledFlight, ledEngine, ledModel,
                  orderDict, orderInfo, edit, data,
                  updateTime)                  
from updataQTread import FigQThread, MapQThread
from map import baiduMap, getCity, baiduNotWeb 
from configparser import ConfigParser
from mySetParameters import QsetParameters
from splashPanel import SplashPanel




# TODO: 加一个清除键 0-27数据清零  参数装订清零     ok
# 默认值       ok
# 显示保存路径  ok
# 安装软件和安装的库文档
# 界面设计和注释         
# TAG: 加符号 暂时不加
# 飞行仿真 放第五个    ok
# 打开后端时，需要关闭后端    
# 优化打开前后端逻辑   ok
# TODO: 对比修改   ok
# 关闭 主界面要关闭黑框      ok
# 实验室logo               ok
# 参数左移                  ok
# 联合仿真改成  打开软件和界面，  飞行仿真只有前后端  去掉控制逻辑  ok


class QmyMainWindow(QMainWindow): 

    def __init__(self, flog,hand = None, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.flog = flog
        self.hand = hand
        self.ui = Ui_MainRhapsody()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.ui.splitter.setStretchFactor(0, 2)  # 设置参数控制区与图像区的比例
        self.ui.splitter.setStretchFactor(0, 5)
        self.setCentralWidget(self.ui.splitter) 
        
        # 记录上一个状态是否为stop状态
        self.stopState = False
        # ==================添加状态栏========================
        # self.ui.setParametersButton.clicked.connect(self.on_setParametersButton_clicked)
        self.__buildUI()
        # ==================按钮功能类初始化==================
        # self.buttonFunction = buttonFunc(self)  # 改用静态方法
        # ================飞行状态/发动机状态/模式状态 互斥灯======================
        self.ledFlightFunction = ledFlightFunc(self)
        self.ledEngineFunction = ledEngineFunc(self)
        self.ledModelFunction = ledModelFunc(self)
        # # ==================打开共享内存模块=================
        # self.key = None    # 打开内存密匙
        # self.ret = -1
        # # 打开共享内存标志位，若为0，则打开成功，若为-1 -2 则失败，一般读取内存中数据之前都要判断一下
        # self.get = None
        # self.ret = self.openMemory()
        # # 打开共享内存，由于.so使用的为创建内存，则这里一定会成功，即不用失败调用定时器一直创建了。

    # ==================以下为绘图区============================
        self.para = [0.0]    # 必须保留这句话，保证para参数为double型
        self.time1 = 0       # 用于debug时观察没画一个数据点的时间
        # 绘图数据初始化
        self.T = 0           # 初始化画图x轴坐标
        dotNum = 1           # 初始化图像队列初始值的个数
        # 获取的数据存放在队列里面，初始化为30个点
        self.allSize = 2000
        # 初始化几个参数
        self.H = queue(dotNum, self.allSize)    
        self.theta = queue(dotNum, self.allSize)
        self.phi = queue(dotNum, self.allSize)
        self.psi = queue(dotNum, self.allSize)
        view = ("heightView", "thetaView", "phiView", "psiView")
        # 反射语法    初始化最右边的图
        for i in view:
            getattr(self.ui, i).createFigure()
            getattr(self.ui, i).t = linspace(0, 10, dotNum)
            # linspace的含义为  0-10范围内均等取30个数

        self.ui.heightView.drawFig(u"高度", "t(s)", self.H.queueList)
        self.ui.thetaView.drawFig(u"俯仰角", "t(s)", self.theta.queueList)
        self.ui.phiView.drawFig(u"滚转角", "t(s)", self.phi.queueList)
        self.ui.psiView.drawFig(u"偏航角", "t(s)", self.psi.queueList)
        # 设置小图边距
        # 设置边距   范围为（0-1）其中右上越大越靠边，左下越小越靠边
        for i in view:
            getattr(self.ui, i).fig.subplots_adjust(right=1, left=0.17, 
                                                    top=1, bottom=0.2)

        # =========================绘制 3维曲线初始化 ==========================
        self.X = queue(dotNum, self.allSize)
        self.Y = queue(dotNum, self.allSize)

        self.ui.threeDView.createThreeDFigure()     # 初始化三维画布
        self.ui.threeDView.iniThreeDFigure()        # 对某些属性进行设置
        self.ui.threeDView.drawThreeFig(self.X.queueList, self.Y.queueList, self.H.queueList)
       
        # ==================打开共享内存模块=================
        self.key = None    # 打开内存密匙
        self.ret = -1
        # 打开共享内存标志位，若为0，则打开成功，若为-1 -2 则失败，一般读取内存中数据之前都要判断一下
        self.get = None
        self.ret = self.openMemory()
        # 打开共享内存，由于.so使用的为创建内存，则这里一定会成功，即不用失败调用定时器一直创建了。

       
       
        # =================打开绘图进程================================
        self.qmut = QMutex()  # 线程锁
        self.FigThread = FigQThread(rest=0.1, obj_ui=self)
        # self.FigThread.daemon=True     # 设置线程为守护线程，即主线程关闭，子线程也关闭
        # 这里不用设置守护进程，因为子进程手动关闭了
        self.FigThread.start()

        # #################################################################
        # ================指示灯模块初始化=====================
        self.ledFlightState = 0
        self.ledModelState = 0        # 程控灯的状态为灭的
        self.ledEngineState = 0
        self.programeControlLed_clicked = False
        self.readData_UpFigure_UpState()
        # ================== 定时更新状态灯======================
        self.LedTimer = QTimer()
        self.LedTimer.stop()
        self.LedTimer.setInterval(updateTime)   # 100ms
        self.LedTimer.start()
        self.LedTimer.timeout.connect(self.upLedState)  # 刷新指示灯状态

        # ####################################################################
        # =========================绘制地图曲线初始化 ===========================
        # 提高响应速度，用多线程加载
        self.is_web = False
        self.cityInfo = None
        self.map = None
        self.cityInfo = None
        # 判断是否有网
        self.check_network()    # 如果有网那么为True
        self.__buildMap()
        # ================记录飞行时间================
        self.beginRunTime = None 

    # 检查网络
    def check_network(self):
        # 检查网络是否可用
        # exit_code = system('ping www.baidu.com')
        try:
            status = urlopen('https://www.baidu.com/')
            self.is_web = True
        # if exit_code:
        except URLError:
            dlgTitle = u"警告"                # 弹出警告窗
            strInfo = u"无网络,地图服务不可用！！！"
            QMessageBox.information(self, dlgTitle, strInfo)
            self.is_web = False
        # else:
        #     self.is_web = True

    # ===================地图初始化======================
    def __buildMap(self):
        
        if self.is_web:
            config = ConfigParser()
            config.read("projectPath.ini", encoding='utf-8')
            city = getCity()     # 实体化获取城市类
            # 获取城市ip，注意这里获取的str类型
            self.cityInfo = city.getLocal()
             # 经度转换米转换成gps坐标，有误差，以北纬38度为基准            
            gps_x = self.para[data['X']] * 0.00000899   
            gps_y = self.para[data['Y']] * 0.00001141     
            if self.cityInfo[0] != None and self.cityInfo[1] != None:
                
                self.map = baiduMap(self.ui.mapView,
                                    "{0}".format(float(self.cityInfo[0]) + gps_x),
                                    "{0}".format(float(self.cityInfo[1]) + gps_y)
                                    )
            else:
                self.map = baiduMap(self.ui.mapView,
                                    "{0}".format(float(config['mapconfig']["default_gps_x"])+gps_x),
                                    "{0}".format(float(config['mapconfig']["default_gps_y"])+gps_y)
                                    )
            
            # 前两个是起始点，后两个为系统打开无人机的坐标
            # 地图的线程
            self.mapThread = MapQThread(rest=1, obj_ui=self)
            self.mapThread.start()
        else:
            # 添加没有网时候的界面
            baiduNotWeb(self.ui.mapView)     # 没有网络则加载 404
            
                 
    # ===================状态栏============================
    def __buildUI(self):
        # 最左边状态栏
        font_size = QFont()
        font_size.setPointSize(15)
        self.LabAircraftInfo = QLabel(self)
        self.LabAircraftInfo.setFont(font_size)     # 设置字体

        self.LabAircraftInfo.setMinimumWidth(300)   # 设置宽度
        self.LabAircraftInfo.setText(u"当前飞机状态：")
        self.ui.statusbar.addWidget(self.LabAircraftInfo)
        
        self.__Lab = QLabel(self)          # 中间的信息
        self.__Lab.setFont(font_size)
        # self.__Lab.setMinimumWidth(300)
        self.__Lab.setText(u"发送指令：")
        self.ui.statusbar.addWidget(self.__Lab)

        self.__LabInfo = QLabel(self)    # 飞机状态信息
        set_font = QFont()
        set_font.setPointSize(15)
        set_font.setFamily("微软雅黑")
        set_font.setBold(True)
        self.__LabInfo.setStyleSheet("color:red")
        self.__LabInfo.setFont(set_font)
        self.__LabInfo.setMinimumWidth(300)
        self.__LabInfo.setText(u"")
        self.ui.statusbar.addWidget(self.__LabInfo)

        # 最右侧时状态栏信息
        self.LabRightInfo = QLabel(self)
        self.LabRightInfo.setFont(font_size)

        self.LabRightInfo.setText(u"")
        self.ui.statusbar.addPermanentWidget(self.LabRightInfo)
    

    # ====================高度图等四个图============================
    def drawFigure(self):
        self.H_min, self.H_max = self.set_Axis(self.H.queueList)
        theta_min, theta_max = self.set_Axis(self.theta.queueList)
        phi_min, phi_max = self.set_Axis(self.phi.queueList)
        psi_min, psi_max = self.set_Axis(self.psi.queueList)

        print(len(self.H.queueList))
        # self.time2 = self.time1
        # self.time1 = time()
        # print("%.4f" % (self.time1-self.time2))
        self.ui.heightView.updateFig(self.H.queueList, self.H_min,
                                     self.H_max, self.T, self.T+10)
        self.ui.thetaView.updateFig(self.theta.queueList, theta_min,
                                    theta_max, self.T, self.T+10)
        self.ui.phiView.updateFig(self.phi.queueList, phi_min,
                                  phi_max, self.T, self.T+10)
        self.ui.psiView.updateFig(self.psi.queueList, psi_min,
                                  psi_max, self.T, self.T+10)
    # ===============坐标轴处理=============================
    @staticmethod     # 静态函数
    def set_Axis(set_list):
        max_axis = max(set_list)
        min_axis = min(set_list)
        if max_axis - min_axis < 20:
            max_axis = max_axis + 1
            min_axis = min_axis - 0.5
        else:
            min_axis -= 5
            max_axis += 5

        return min_axis, max_axis
    # ================= 三维曲线更新======================
    def drawThreeDFigure(self):
        self.xmin, self.xmax = self.set_Axis(self.X.queueList)
        self.ymin, self.ymax = self.set_Axis(self.Y.queueList)

        self.ui.threeDView.updataThreeFig(self.X.queueList, self.Y.queueList, self.H.queueList,
                                          self.xmin, self.xmax, self.ymin, self.ymax,
                                          self.H_min, self.H_max)

    # ==============event处理函数==========================
    # 窗口关闭的事件重写
    def closeEvent(self, event):
        dlgTitle = u"警告"
        strInfo = u"是否退出联合仿真系统？"
        defaultBtn = QMessageBox.NoButton
        result = QMessageBox.question(self, dlgTitle, strInfo,
                                      QMessageBox.Yes | QMessageBox.No, defaultBtn)
        if result == QMessageBox.Yes:
            if self.key:  #这里要判断一下是否获取了打开内存的密匙，如果没有，则不存在下面的一切对象
                self.FigThread.closeThread = True
                if self.is_web:    # 如果没网络，则地图服务不启动继而没有该对象
                    self.mapThread.closeThread = True
                sleep(0.6) # 等待进入线程中关闭线程
                self.get.closeShareMem()
                print("关闭共享内存成功")
                # self.LabRightInfo.setText(u"关闭联合仿真成功")
                self.end_program("Test.exe")
                sleep(0.1)  # 关闭仿真后端
            event.accept()
        else:
            event.ignore()

    # ==========由connectSlotsByName()自动连接的槽函数============
    def on_takeOffButton_clicked(self):
        # 起飞按钮，发送命令，并且还是记录飞机飞行时间
        self.beginRunTime = time()  
        buttonFunc.takeOffButton(self)

    def on_landingButton_clicked(self):
        # 着陆按钮
        buttonFunc.landingButton(self)

    def on_keepHeightButton_clicked(self):
        # 定高平飞
        buttonFunc.keepHeightButton(self)

    def on_climb1Button_clicked(self):
        # 爬升1
        buttonFunc.climb1Button(self)
        
    def on_climb2Button_clicked(self):
        # 下滑1
        buttonFunc.climb2Button(self)

    def on_decline1Button_clicked(self):
        # 爬升2
        buttonFunc.decline1Button(self)

    def on_decline2Button_clicked(self):
        # 下滑2
        buttonFunc.decline2Button(self)

    def on_turnLeftButton_clicked(self):
        # 左转
        buttonFunc.turnLeftButton(self)

    def on_turnRightButton_clicked(self):
        # 右转
        buttonFunc.turnRightButton(self)

    def on_keepDirectButton_clicked(self):
        # 定向
        buttonFunc.keepDirectButton(self)

        #  模式三个按键
    def on_programeControlModelButton_clicked(self):
        # 程控按钮
        buttonFunc.programeControlModelButton(self)

    def on_remoteControlModelButton_clicked(self):
        # 遥控按钮
        buttonFunc.remoteControlModelButton(self)

    def on_internalControlModelButton_clicked(self):
        # 内控按钮
        buttonFunc.internalControlModelButton(self)
    
    # 发动机
    def on_bigCartButton_clicked(self):
        buttonFunc.bigCartButton(self)

    def on_ratedButton_clicked(self):
        buttonFunc.ratedButton(self)

    def on_cruiseButton_clicked(self):
        buttonFunc.cruiseButton(self)

    def on_slowTrainButton_clicked(self):
        buttonFunc.slowTrainButton(self)

    def on_idlingButton_clicked(self):
        buttonFunc.idlingButton(self)

    def on_preStopButton_clicked(self):
        buttonFunc.preStopButton(self)

    def on_parkingButton_clicked(self):
        buttonFunc.parkingButton(self)

    # 保存图片按钮
    @pyqtSlot()
    def on_saveFigButton_clicked(self):
        buttonFunc.saveFigButton(self)
    
    # 保存数据
    @pyqtSlot()
    def on_saveConfButton_clicked(self):
        print("on_saveConfButton_clicked")
        if self.beginRunTime:
            self.newRunTime = time()
            t = self.newRunTime - self.beginRunTime
            buttonFunc.saveConfButton(self, "%.2f" % t)
        else:
            self.LabRightInfo.setText(u"飞机尚未起飞")
    
    @pyqtSlot()
    def on_setParametersButton_clicked(self):
        
        setParame = QsetParameters(self)
        setParame.setAttribute(Qt.WA_DeleteOnClose)
        # self.setParame.show()
        setParame.exec()
            
    # 清除所有信息，包括内存、绘图、地图、状态
    @pyqtSlot()
    def on_zeroingButton_clicked(self):
        if self.flog == "flightButton":
            self.end_program("Test.exe")
            sleep(0.1)
            self.begin_program()
            sleep(0.1)
            # queue
            n = 2
            tempList = [self.X, self.Y, self.H, self.psi, self.phi, self.theta]
            for i in tempList:
                getattr(i, "zeroingData")(n)    # 反射     Y-theta都为零
            self.updateTime()
            for i in range(0, len(data)):      # 内存中的数也都为零
                self.para[i] = 0.0
            if self.is_web:                    # 重新加载地图
                self.map.openURL()

        elif self.flog == "mainSystemButton":
            self.end_program("Test.exe")
            sleep(0.1)
            self.begin_program()
            sleep(0.1)
            # queue
            n = 2
            tempList = [self.X, self.Y, self.H, self.psi, self.phi, self.theta]
            for i in tempList:
                getattr(i, "zeroingData")(n)  # 反射     Y-theta都为零
            self.updateTime()
            for i in range(0, len(data)):  # 内存中的数也都为零
                self.para[i] = 0.0
            if self.is_web:  # 重新加载地图
                self.map.openURL()

            # 获取焦点
            try:
                keybd_event(13, 0, 0, 0)
                SetForegroundWindow(self.hand)
                sleep(0.5)
                # 按下快捷键
                keybd_event(115, 0, 0, 0)  # F4键位码是115
                sleep(0.01)
                keybd_event(115, 0, KEYEVENTF_KEYUP, 0)  # 释放按键115

            except UnboundLocalError:
                dlgTitle = u"打开错误"
                strInfo = u"打开Rhapsody程序打开错误"
                QMessageBox.critical(self, dlgTitle, strInfo)







    @staticmethod
    def end_program(pro_name):
        system("%s%s" % ("taskkill /F /IM ", pro_name))


    def begin_program(self):
        config = ConfigParser()
        config.read("projectPath.ini", encoding='utf-8')
        RhapsodyProjectExePath = config['DEFAULT']["RhapsodyProjectExePath"]
        if path.isfile(RhapsodyProjectExePath):
            if '.exe' in RhapsodyProjectExePath:
                ShellExecute(0, 'open', RhapsodyProjectExePath, "", '', 1)
                # print("打开rhapsody成功！！！")
        else:
            curPath = QDir.currentPath()
            dlgTitle = u"打开Rhapsody项目编译之后可执行文件"
            filt = u"执行程序(*.exe);;所有文件(*.*)"
            filename, _ = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
            if ".exe" in filename.lower():
                ShellExecute(0, 'open', filename, "", '', 1)

            elif filename == '':
                pass
            else:
                dlgTitle = u"打开错误"
                strInfo = u"打开Rhapsody项目编译之后可执行文件"
                QMessageBox.critical(self, dlgTitle, strInfo)

# ==============自定义函数===============================
    # 设置指示灯的互斥，某一瞬间一个模块只有一个亮的
    def ledFlightStateMutex(self, clickled):
        self.ledFlightFunction.ledFlight(clickled)

    # 更新飞行状态指示灯
    def updataLedFilghtState(self):
        # 先读取目前的飞行状态
        newFlightStatus = int(self.get.readOrWriteData('acceptFlightStatus', 'r'))
        # 如果状态改变了，进行更新状态灯
        if self.ledFlightState != newFlightStatus:
            self.ledFlightState = newFlightStatus
            # 首先判断是否为停止状态，改状态单独拿出来是因为，该状态是程控时最后一个状态，
            # 当到达该状态之后，再进入其他飞翔状态，则会清空绘图信息
            if newFlightStatus == ledFlight['stopLed']:
                self.ledFlightStateMutex('stopLed')
                self.stopState = True
            # allLedOff 状态是最开始的初始状态，即没有任何飞行状态
            elif newFlightStatus == ledFlight['allLedOff']:
                self.ledFlightStateMutex('allLedOff')
            else:
                # 根据状态更新指示灯
                newDict = {v: k for k, v in ledFlight.items()}
                self.ledFlightStateMutex(newDict[newFlightStatus])
                # 下面的判断即为如果上一个是停止，那么再按其他按钮则清空数据
                if self.stopState:
                    print("stopState", self.stopState)
                    self.stopState = False
                    self.qmut.lock()
                    self.reFig()
                    self.qmut.unlock()
    
    # 使X、Y、H画图的数据截取到后二个
    def reFig(self):
        n = 2
        tempList = [self.X, self.Y, self.H, self.psi, self.phi, self.theta]
        for i in tempList:
            getattr(i, "savaData")(n)    # 反射
        self.updateTime()
    
    # 发动机等互斥
    def ledEngineStateMutex(self, Engine):
        self.ledEngineFunction.ledEngine(Engine)
    # 更新发动机灯
    def updataEngineState(self):
        newEngineState = int(self.get.readOrWriteData('acceptEngineStatus', 'r'))
        if self.ledEngineState != newEngineState:
            self.ledEngineState = newEngineState
            if newEngineState == ledEngine['allLedOff']:
                self.ledEngineStateMutex('allLedOff')
            else:
                newDict = {v: k for k, v in ledEngine.items()}
                self.ledEngineStateMutex(newDict[newEngineState])

    # 模式灯互斥
    def ledModelStateMutex(self, clickled):
        self.ledModelFunction.ledModel(clickled)
    # 更新模式灯
    def updateLedModelState(self):
        newModelState = int(self.get.readOrWriteData('acceptModel', 'r'))
        if self.ledModelState != newModelState:
            self.ledModelState = newModelState
            if newModelState == ledModel['allLedOff']:
                self.ledModelStateMutex('allLedOff')
            else:
                newDict = {v: k for k, v in ledModel.items()}
                self.ledModelStateMutex(newDict[newModelState])

    # ==================更新显示数据（界面左上角的数据显示区）====================
    def dataShow(self):
        for i, enum in enumerate(edit):
            func = getattr(self.ui, enum).setText
            func("%.2f" % self.para[i])

    # =======================更新绘图、地图相关======================================

    # 定制更新指示灯和界面数据
    # 该函数定时执行
    def upLedState(self):
        # 显示数据
        self.dataShow()
        self.updataLedFilghtState()
        self.updateLedModelState()
        self.updataEngineState()

    # 更新界面最右侧图的横坐标（时间）
    def updateTime(self):
        self.ui.heightView.t = linspace(self.T, self.T + 10, len(self.H.queueList))
        self.ui.thetaView.t = linspace(self.T, self.T + 10, len(self.theta.queueList))
        self.ui.phiView.t = linspace(self.T, self.T + 10, len(self.phi.queueList))
        self.ui.psiView.t = linspace(self.T, self.T + 10, len(self.psi.queueList))
        self.T += 0.1
    
     # =============地图更新=====================
    def updataMap(self):
        self.map.autoShow(self.para[data['X']], self.para[data['Y']])

    # 读取内存数据  更新绘图   更新状态灯   该函数单独线程
    def readData_UpFigure_UpState(self):
        if self.ret == 0:
            self.para = self.get.readAll()
            # 小图获取数据
            self.X.updata(self.para[data['X']])
            self.Y.updata(self.para[data['Y']])
            self.H.updata(self.para[data['H']])
            self.theta.updata(self.para[data['theta']])
            self.phi.updata(self.para[data['phi']])
            self.psi.updata(self.para[data['psi']])
            self.updateTime()
            self.drawFigure()
            # ===========3维数据更新====================
            self.drawThreeDFigure()
            retu = 0
        else:
            retu = -1
        return retu

    # ======================发送命令相关================

    # 该函数为判断发出的为什么指令，然后把该指令更新到状态栏
    def judgeOrder(self, state):
        for i in range(1, len(orderInfo)):
            if state == i:
                self.__LabInfo.setText(orderInfo[i])
    
    # 发送命令函数
    def sendOrder(self, order):
        if self.ret == 0:
            self.get.readOrWriteData('send', 'w', orderDict[order])
            self.judgeOrder(orderDict[order])
            print("写入指令：%d :" % int(self.get.readOrWriteData('send', 'r')) + order)
            retu = 0
        else:
            retu = -1
        return retu
    
    # =================打开内存相关================
    # 获取打开内存的密匙
    def keyInputWindow(self):
        f = QFont()
        f.setPointSize(50)
        dlgTitle = u"请输入联合系统密匙"
        txtLable = u"请仔细检查填写的密匙, 如未能取得正确数据,\n请关闭系统，然后重新填写密匙。"
        defautInput = u"szName"

        echoMode = QLineEdit.Normal
        key, ok = QInputDialog.getText(self, dlgTitle, txtLable, echoMode, defautInput)
        if ok:
            print("key:", key)
            return key.encode("utf-8")
        else: 
            sys.exit(0)   # 如果点击为界面的取消则关闭整个系统

    # 打开内存，在最前面执行
    def openMemory(self):
        while not self.key:
            self.key = self.keyInputWindow()
            if not self.key:
                dlgTitle = u"警告"
                strInfo = u"密匙不能为空！！！"
                QMessageBox.information(self, dlgTitle, strInfo)
        self.get = getShareMemData(self.key)
        self.ret = self.get.openShareMem()
        if self.ret == -1:
            print("打开内存失败！！！")
            self.LabRightInfo.setText(u"启动联合仿真失败")
        elif self.ret == -2:
            self.LabRightInfo.setText(u"启动联合仿真失败")
            print("指针指向失败！！！")
        else:
            self.ret = 0
            print("打开共享内存成功！！！")
            self.LabRightInfo.setText(u"已启动联合仿真")
        return self.ret 




#  ============窗体测试程序 ================================
if __name__ == "__main__":
    app = 0     # 清除上次运行的残留
    v_compare = QVersionNumber(5, 6, 0)
    v_current, _ = QVersionNumber.fromString(QT_VERSION_STR)  # 获取当前Qt版本
    if QVersionNumber.compare(v_current, v_compare) >= 0:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Qt从5.6.0开始，支持High-DPI
        app = QApplication(sys.argv)  #
    else:
        app = QApplication(sys.argv)
        font = QFont("宋体")
        pointSize = font.pointSize()
        font.setPixelSize(pointSize*90/72)
        app.setFont(font)

    
    splash = SplashPanel()
    app.processEvents()  # 防止进程卡死

    myMainWin = QmyMainWindow("flightButton", None)
    myMainWin.show()

    splash.finish(myMainWin)  # 关闭欢迎界面
    splash.deleteLater()

    sys.exit(app.exec())

