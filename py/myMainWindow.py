# -*- coding: utf-8 -*-
import sys, os

import sys
sys.path.append(r"./py")

import time
from PyQt5.QtWidgets import  (QApplication, QMainWindow,QLabel,QMessageBox)
from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt,QTimer,QMargins
import numpy as np
#import matplotlib as mpl
#import matplotlib.style as mplStyle  #一个模块
import matplotlib.image as img

#from QMyLed import QMyLed
from ui_MainRhapsody import Ui_MainRhapsody
from GetDataFromShareMem import getShareMemData   # .so为底层
#from shareMem import getShareMemData              # py直接调用win的API作为底层
#from myFigureCanvas import QmyFigureCanvas
from dataStack import queue
from buttonFunc import buttonFunc



orderDict = {
   'allLedOff':0,
   'takeOffLed':1,
   'landingLed':2,
   'keepHeightLed':9,
   'climb1Led':3,
   'climb2Led':5,
   'decline1Led':4,
   'decline2Led':6,
   'turnLeftLed':7,
   'turnRightLed':8,
   'keepDirectLed':10,
   'programeControlLed':11,
   'stopLed':12
}

class QmyMainWindow(QMainWindow): 
   mapChanged = pyqtSignal(str)   # 发送一个地图名称
   def __init__(self, parent=None):
      super().__init__(parent)   # 调用父类构造函数，创建窗体
      self.ui=Ui_MainRhapsody()    # 创建UI对象
      self.ui.setupUi(self)      # 构造UI界面
      self.setCentralWidget(self.ui.splitter)

      # 记录上一个状态是否为stop状态
      self.stopState = False
      ## ==================添加状态栏========================
      self.__buildUI()
      ## ==================按钮功能类初始化==================
      self.buttonFunction = buttonFunc(self)
      ## ==================打开共享内存模块=================
      self.ret = -1   # 打开共享内存标志位，若为0，则打开成功，若为-1 -2 则失败，一般读取内存中数据之前都要判断一下

      self.get = None
      self.ret = self.openMemory()       #打开共享内存，由于.so使用的为创建内存，则这里一定会成功，即不用失败调用定时器一直创建了。
      if self.ret == -1:
         print("打开内存失败！！！")
         self.LabRightInfo.setText("打开内存失败！！！")
         #self.openMemTimer.start()
      elif self.ret == -2:
         print("指针指向失败！！！")
         self.LabRightInfo.setText("指针指向失败！！！")
         #self.openMemTimer.start()
      else:  
         print("打开共享内存成功！！！")
         self.LabRightInfo.setText("打开共享内存成功！！！")
      #self.openMemTimer.start()
      #self.openMemTimer.timeout.connect(self.__ret)
## ==================图============================
      self.para = [0.0,0.0,0.0,0.0]    # 必须保留这句话，保证para参数为double型
      self.time1 = 0
      # 绘图数据初始化
      self.T = 0
      dotNum = 2
      # 获取的数据存放在队列里面，初始化为30个点
      self.H = queue(dotNum)
      self.theta = queue(dotNum)
      self.phi = queue(dotNum)
      self.psi = queue(dotNum)
      self.ui.heightView.createFigure()
      self.ui.thetaView.createFigure()
      self.ui.phiView.createFigure()
      self.ui.psiView.createFigure()
      self.ui.heightView.t = np.linspace(0, 10, dotNum)   #np.linspace的含义为  0-10范围内均等取30个数
      self.ui.thetaView.t = np.linspace(0, 10, dotNum)
      self.ui.phiView.t = np.linspace(0, 10, dotNum)
      self.ui.psiView.t = np.linspace(0,10,dotNum)

      self.ui.heightView.drawFig("高度","t(s)",self.H.queueList )
      self.ui.thetaView.drawFig("俯仰角","t(s)",self.theta.queueList)
      self.ui.phiView.drawFig("滚转角","t(s)",self.phi.queueList)
      self.ui.psiView.drawFig("偏航角","t(s)",self.psi.queueList)
      
      # 设置小图边距
      self.ui.heightView.fig.subplots_adjust(right=1, left=0.17)# 设置边距   范围为（0-1）其中右越大越靠边，左越小越靠边
      self.ui.thetaView.fig.subplots_adjust(right=1, left=0.17)
      self.ui.phiView.fig.subplots_adjust(right=1, left=0.17)
      self.ui.psiView.fig.subplots_adjust(right=1, left=0.17)
      # =========================绘制 3维曲线 ==========================
      self.X = queue(dotNum)
      self.Y = queue(dotNum)

      self.ui.threeDView.createThreeDFigure()     #初始化三维画布
      self.ui.threeDView.iniThreeDFigure()        #对某些属性进行设置
      self.ui.threeDView.drawThreeFig(self.X.queueList,self.Y.queueList,self.H.queueList)


      #=========================绘制地图曲线 ===========================
      self.lastMapName = '1.png'
      self.ui.mapView.createMapFigure()
      self.ui.mapView.drawMapFig(self.X.queueList,[-i for i in self.Y.queueList])
      self.mapChanged.connect(self.do_mapChange)


      ## ================指示灯模块初始化=====================
      self.LedState = 0
      self.LedProgrameControlState = 0
      self.programeControlLed_clicked = False
      self.readData_UpFigure_UpState()
      self.LedTimer = QTimer()
      self.LedTimer.stop()
      self.LedTimer.setInterval(70)   # 200ms
      self.LedTimer.start()
      self.LedTimer.timeout.connect(self.readData_UpFigure_UpState)  # 刷新指示灯状态 刷新绘图


   # ===================状态栏============================
   def __buildUI(self):
      self.__LabAircraftInfo = QLabel(self)
      self.__LabAircraftInfo.setMinimumWidth(300)
      self.__LabAircraftInfo.setText("当前飞机状态：")
      self.ui.statusbar.addWidget(self.__LabAircraftInfo)
      
      self.__LabInfo = QLabel(self)
      self.__LabInfo.setMinimumWidth(300)
      self.__LabInfo.setText("指令发送：")
      self.ui.statusbar.addWidget(self.__LabInfo)

      # 最右侧1050
      self.LabRightInfo = QLabel(self)
      self.LabRightInfo.setText("")
      self.ui.statusbar.addPermanentWidget(self.LabRightInfo)

   #====================高度图等四个图============================
   def drawFigure(self):
      self.H_min, self.H_max = self.axis(self.H.queueList)
      theta_min,theta_max = self.axis(self.theta.queueList)
      phi_min,phi_max = self.axis(self.phi.queueList)
      psi_min,psi_max = self.axis(self.psi.queueList)
      print(len(self.H.queueList))
      self.time2 = self.time1
      self.time1 = time.time()
      print("%.4f" % (self.time1-self.time2))
      '''
      self.ui.heightView.drawFig("高度","t(s)",self.H.queueList,self.H_min,self.H_max, self.T,self.T+10)
      self.ui.thetaView.drawFig("俯仰角","t(s)",self.theta.queueList,theta_min,theta_max, self.T,self.T+10)
      self.ui.phiView.drawFig("滚转角","t(s)",self.phi.queueList,phi_min,phi_max, self.T,self.T+10)
      self.ui.psiView.drawFig("偏航角","t(s)",self.psi.queueList,psi_min,psi_max, self.T,self.T+10)
      '''
      self.ui.heightView.updateFig(self.H.queueList,self.H_min,self.H_max, self.T,self.T+10)
      self.ui.thetaView.updateFig(self.theta.queueList,theta_min,theta_max, self.T,self.T+10)
      self.ui.phiView.updateFig(self.phi.queueList,phi_min,phi_max, self.T,self.T+10)
      self.ui.psiView.updateFig(self.psi.queueList,psi_min,psi_max, self.T,self.T+10)
   # ===============坐标轴处理=============================
   def axis(self,list):
      max_axis = max(list)
      min_axis = min(list)
      if max_axis - min_axis < 20:
         max_axis = max_axis + 1
         min_axis = min_axis -0.5
      else:
         min_axis -= 5
         max_axis += 5

      return min_axis   , max_axis 
   # ================= 三维曲线更新======================
   def drawThreeDFigure(self):
      self.xmin,self.xmax = self.axis(self.X.queueList)
      self.ymin,self.ymax = self.axis(self.Y.queueList)
      #Hmin, Hmax = self.y_axis(self.H.queueList)

      self.ui.threeDView.updataThreeFig(self.X.queueList,self.Y.queueList,self.H.queueList,
                                   self.xmin,self.xmax,self.ymin,self.ymax,self.H_min, self.H_max )

   # ====================地图曲线========================
   def mapAxis(self,list):
      max_axis = max(list)
      min_axis = min(list)
      if max_axis < 500:
         min_axis = 0
         max_axis = 600
         self.mapChanged.emit('./map/1.png')
      elif max_axis < 1000:
         self.mapChanged.emit('./map/2.png')
         max_axis = 1000
         min_axis = 400
      elif max_axis < 1500:
         max_axis = 1500
         min_axis = 900
         self.mapChanged.emit('./map/3.png')
      elif max_axis <2000:
         max_axis = 2000
         min_axis = 1400
         self.mapChanged.emit('./map/4.png')
      elif max_axis < 2500:
         max_axis = 2500
         min_axis = 1900
         self.mapChanged.emit('./map/5.png')
      elif max_axis <3000:
         max_axis = 3000
         min_axis = 2400
         self.mapChanged.emit('./map/6.png')
      elif max_axis <3500:
         max_axis = 3500
         min_axis = 2900
         self.mapChanged.emit('./map/7.png')
      elif max_axis <4000:
         max_axis = 4000
         min_axis = 3400
         self.mapChanged.emit('./map/8.png')
      else:
         max_axis += 500
         min_axis = 3900
      return min_axis,max_axis
   # 更新地图的槽函数
   @pyqtSlot(str)
   def do_mapChange(self,mapName):
      if mapName != self.lastMapName:
         self.lastMapName = mapName
         self.ui.mapView.bgimg = img.imread(mapName)
         self.ui.mapView.figure.figimage(self.ui.mapView.bgimg)

   def drawMapFigure(self):
      xmin, xmax = self.mapAxis(self.X.queueList)
      tep = max(abs(self.ymin),abs(self.ymax))
      ymin = -tep
      ymax = tep

      self.ui.mapView.updataMapFig(self.X.queueList,[-i for i in self.Y.queueList],
                                 xmin,xmax,ymin,ymax)


##  ==============event处理函数==========================
   # 窗口关闭的事件重写
   def closeEvent(self,event):
      dlgTitle = "警告"
      strInfo = "是否退出联合仿真系统？"
      defaultBtn = QMessageBox.NoButton
      result = QMessageBox.question(self,dlgTitle, strInfo, 
      QMessageBox.Yes|QMessageBox.No,defaultBtn)
      if (result == QMessageBox.Yes):
         self.get.closeShareMem()
         print("关闭共享内存成功")
         self.LabRightInfo.setText("关闭共享内存成功")
         event.accept()
      else:
         event.ignore()

   # 窗口大小改变事件重写
   '''
   def resizeEvent(self,event):

      self.ui.mapView.bgimg = img.imread('./timg.jpg')

      self.ui.mapView.figure.figimage(self.ui.mapView.bgimg)

   '''

##  ==========由connectSlotsByName()自动连接的槽函数============ 

   def on_takeOffButton_clicked(self):
      # print("takeOffButton is clicked")
      # self.LabRightInfo.setText("起飞按钮按下")
      # retu = self.sendOrder('takeOffLed')
      # if retu == 0:
      #    print("指令发送成功！！！")
      self.buttonFunction.takeOffButton()

         
   def on_landingButton_clicked(self):
      self.buttonFunction.landingButton()

   def on_keepHeightButton_clicked(self):
      self.buttonFunction.keepHeightButton()

   def on_climb1Button_clicked(self):
      self.buttonFunction.climb1Button()
      
   def on_climb2Button_clicked(self):
      self.buttonFunction.climb2Button()

   def on_decline1Button_clicked(self):
      self.buttonFunction.decline1Button()

   def on_decline2Button_clicked(self):
      self.buttonFunction.decline2Button()

   def on_turnLeftButton_clicked(self):
      self.buttonFunction.turnLeftButton()

   def on_turnRightButton_clicked(self):
      self.buttonFunction.turnRightButton()

   def on_keepDirectButton_clicked(self):
      self.buttonFunction.keepDirectButton()


   def on_programmedControlButton_clicked(self):
      print("self.programeControlLed_clicked:")
      self.LabRightInfo.setText("程控飞行按钮按下")
      self.setprogrameControlOrder()

   # 保存图片按钮
   @pyqtSlot()
   def on_saveFigButton_clicked(self):
      new = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
      filePath = "./curaeFile/"+new+"/"
      if not os.path.isdir(filePath):
         os.makedirs(filePath)
      self.ui.heightView.fig.savefig("./curaeFile/"+new+"/"+"Height.png")
      self.ui.thetaView.fig.savefig("./curaeFile/" + new + "/" + "theta.png")
      self.ui.phiView.fig.savefig("./curaeFile/" + new + "/" + "phi.png")
      self.ui.psiView.fig.savefig("./curaeFile/" + new + "/" + "psi.png")
      self.ui.threeDView.figure.savefig("./curaeFile/" + new + "/" + "threeDimensional.png")


##  =============自定义槽函数===============================        

## ==============自定义函数===============================
   # 设置指示灯的互斥，某一瞬间只有一个亮的
   def ledStateMutex(self,clickled):
      if clickled == "takeOffLed":
         self.__LabAircraftInfo.setText("当前飞机状态：起飞")
         self.ui.takeOffLed.state = 'on'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "landingLed":
         self.__LabAircraftInfo.setText("当前飞机状态：着陆")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'on'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "keepHeightLed":
         self.__LabAircraftInfo.setText("当前飞机状态：定高飞行")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'on'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()
 
      elif clickled == "climb1Led":
         self.__LabAircraftInfo.setText("当前飞机状态：爬升1")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'on'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "climb2Led":
         self.__LabAircraftInfo.setText("当前飞机状态：爬升2")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'on'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "decline1Led":
         self.__LabAircraftInfo.setText("当前飞机状态：下滑1")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'on'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "decline2Led":
         self.__LabAircraftInfo.setText("当前飞机状态：下滑2")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'on'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "turnLeftLed":
         self.__LabAircraftInfo.setText("当前飞机状态：左转")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'on'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "turnRightLed":
         self.__LabAircraftInfo.setText("当前飞机状态：右转")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'on'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()

      elif clickled == "keepDirectLed":
         self.__LabAircraftInfo.setText("当前飞机状态：定向飞行")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'on'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.stopLed.repaint()
      
      elif clickled == 'stopLed':
         self.__LabAircraftInfo.setText("当前飞机状态：停止")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'on'
         self.ui.stopLed.repaint()

      elif clickled == "allLedOff":
         self.__LabAircraftInfo.setText("当前飞机状态：等待")
         self.ui.takeOffLed.state = 'off'
         self.ui.takeOffLed.repaint()
         self.ui.landingLed.state = 'off'
         self.ui.landingLed.repaint()
         self.ui.keepHeightLed.state = 'off'
         self.ui.keepHeightLed.repaint()
         self.ui.climb1Led.state = 'off'
         self.ui.climb1Led.repaint()
         self.ui.climb2Led.state = 'off'
         self.ui.climb2Led.repaint()
         self.ui.decline1Led.state = 'off'
         self.ui.decline1Led.repaint()
         self.ui.decline2Led.state = 'off'
         self.ui.decline2Led.repaint()
         self.ui.turnLeftLed.state = 'off'
         self.ui.turnLeftLed.repaint()
         self.ui.turnRightLed.state = 'off'
         self.ui.turnRightLed.repaint()
         self.ui.keepDirectLed.state = 'off'
         self.ui.keepDirectLed.repaint()
         self.ui.stopLed.state = 'off'
         self.ui.keepDirectLed.repaint() 

   # 读取内存数据  更新绘图   更新状态灯   该函数为定时执行函数
   def readData_UpFigure_UpState(self):
      if self.ret == 0:
         self.para = self.get.readAll()
         # 小图获取数据
         self.H.updata(self.para[2])
         self.theta.updata(self.para[7])
         self.phi.updata(self.para[6])
         self.psi.updata(self.para[8])
         self.ui.heightView.t = np.linspace(self.T, self.T + 10,  len(self.H.queueList))
         self.ui.thetaView.t = np.linspace(self.T, self.T + 10, len(self.theta.queueList))
         self.ui.phiView.t = np.linspace(self.T, self.T + 10, len(self.phi.queueList))
         self.ui.psiView.t = np.linspace(self.T, self.T + 10, len(self.psi.queueList))
         self.drawFigure()
         self.T += 0.1
         # 显示数据
         self.ui.XEdit.setText("%.2f"%self.para[0])
         self.ui.YEdit.setText("%.2f" % self.para[1])
         self.ui.HEdit.setText("%.2f"%self.para[2])
         self.ui.alphaEdit.setText("%.2f" % self.para[3])
         self.ui.betaEdit.setText("%.2f" % self.para[4])
         self.ui.VtEdit.setText("%.2f" % self.para[5])
         self.ui.phiEdit.setText("%.2f" % self.para[6])
         self.ui.thetaEdit.setText("%.2f" % self.para[7])
         self.ui.psiEdit.setText("%.2f" % self.para[8])
         self.ui.pEdit.setText("%.2f" % self.para[9])
         self.ui.qEdit.setText("%.2f" % self.para[10])
         self.ui.rEdit.setText("%.2f" % self.para[11])

         #===========3维数据更新====================
         self.X.updata(self.para[0])
         self.Y.updata(self.para[1])
         self.drawThreeDFigure()

         # =============地图更新=====================
         self.drawMapFigure()
         
         # ===============更新状态灯=============================
         newState = int(self.get.readOrWriteData('acceptState','r'))
         newProgrameControlState = int(self.get.readOrWriteData('programeControlState', 'r'))

         if (self.LedState != newState):
            self.LedState = newState
         
            if newState == 1:
               self.ledStateMutex('takeOffLed')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 2:
               self.ledStateMutex('landingLed')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 9:
               self.ledStateMutex('keepHeightLed')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 3:
               self.ledStateMutex('climb1Led')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 5:
               self.ledStateMutex('climb2Led')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 4:
               self.ledStateMutex('decline1Led')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 6:
               self.ledStateMutex('decline2Led')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 7:
               self.ledStateMutex('turnLeftLed')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 8:
               self.ledStateMutex('turnRightLed')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 10:
               self.ledStateMutex('keepDirectLed')
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
            elif newState == 12:
               self.ledStateMutex('stopLed')
               self.stopState = True
            else:
               self.ledStateMutex('allLedOff')

         if  self.LedProgrameControlState != newProgrameControlState:
            self.LedProgrameControlState = newProgrameControlState
            if newProgrameControlState == 1:
               print("程控灯打开")

               self.ui.programeControlLed.state = 'on'
               self.ui.programeControlLed.repaint()
            else:
               print("程控灯关闭")

               self.ui.programeControlLed.state = 'off'
               self.ui.programeControlLed.repaint()
         retu = 0
      else:
         retu = -1
      return retu

   def judgeAircraftState(self, state):
         if state == 1:
            self.__LabInfo.setText("发送指令：起飞")
         elif state == 2:
            self.__LabInfo.setText("发送指令：着陆")
         elif state == 3:
            self.__LabInfo.setText("发送指令：爬升1")
         elif state == 4:
            self.__LabInfo.setText("发送指令：下滑1")
         elif state == 5:
            self.__LabInfo.setText("发送指令：爬升2")
         elif state == 6:
            self.__LabInfo.setText("发送指令：下滑2")
         elif state == 7:
            self.__LabInfo.setText("发送指令：左转")
         elif state == 8:
            self.__LabInfo.setText("发送指令：右转")
         elif state == 9:
            self.__LabInfo.setText("发送指令：定高飞行")
         elif state == 10:
            self.__LabInfo.setText("发送指令：定向飞行")
         elif state == 11:
            self.__LabInfo.setText("发送指令：程控飞行")

   def sendOrder(self, order):
      if self.ret == 0:
         self.get.readOrWriteData('send','w',orderDict[order])
         self.judgeAircraftState(orderDict[order])
         print("写入指令：%d :"% int(self.get.readOrWriteData('send','r'))+ order)
         #self.LabRightInfo.setText("写入指令：%d :"% int(self.get.readOrWriteData('send','r'))+ order)

         retu = 0
      else:
         retu = -1
      return retu

   def setprogrameControlOrder(self):
      if self.ret == 0:
         if int(self.get.readOrWriteData('programeControlState','r')) != 1:
            retu = self.get.readOrWriteData('send','w',11)
            if retu == 0:
               self.judgeAircraftState(11)
               print("程控指令发送成功！！！")
               self.LabRightInfo.setText("程控指令发送成功！！！")
         else:
            retu = -1
      else:
         retu = 0
      return retu

   # 打开内存，在最前面执行
   def openMemory(self):
      self.get = getShareMemData()
      self.ret = self.get.openShareMem()
      if self.ret == -1:
         print("打开内存失败！！！")
         self.LabRightInfo.setText("打开内存失败！！！")
      elif self.ret == -2:
         self.LabRightInfo.setText("指针指向失败！！！")
         print("指针指向失败！！！")
      else:
         self.ret = 0
      return self.ret

   def __ret(self):
      if self.ret != 0:
         self.ret = self.openMemory()

   # 使X、Y、H画图的数据截取到后三十个
   def reFig(self):
      self.X.savaData()
      self.Y.savaData()
      self.H.redata()




##  ============窗体测试程序 ================================

if  __name__ == "__main__":        #用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序
   form=QmyMainWindow()            #创建窗体
   form.show()
   sys.exit(app.exec_())
