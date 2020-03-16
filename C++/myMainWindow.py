# -*- coding: utf-8 -*-
import sys, os
import time
from PyQt5.QtWidgets import  (QApplication, QMainWindow,QLabel,QMessageBox)
from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt,QTimer,QMargins
import numpy as np
import matplotlib.image as img
from ui_MainRhapsody import Ui_MainRhapsody
from GetDataFromShareMem import getShareMemData   # .so为底层
#from shareMem import getShareMemData              # py直接调用win的API作为底层
#from myFigureCanvas import QmyFigureCanvas
from dataStack import queue
from buttonFunc import buttonFunc
from  ledFunc import ledFlightFunc

## 飞行状态指示灯
ledFlight = {     # 正确
            'allLedOff':0, 'takeOffLed':1, 'landingLed':2,
            'climb1Led':3, 'decline1Led':4, 'climb2Led':5,
            'decline2Led':6, 'turnLeftLed':7, 'turnRightLed':8,
            'keepHeightLed':9,'keepDirectLed':10,  # 无11
            'stopLed': 11,'keepPostureLed': 13
         }
#  发动机的指示灯
ledEngine = {   # 发动机状态没有预停，但是指示灯有预停
            'allLedOff':0,
            'bigCartLed' : 1 ,'ratedLed':2, 'cruiseLed':3, 
            'slowTrainLed':4, 'idlingLed':5,'preStopLed': 6, 'parkingLed':7

         }   
# 模式指示灯
ledModel = {    # 和指令顺序不一样
            'allLedOff': 0,
            'programeControlModelLed':1,"remoteControlModelLed":2, "internalControlModelLed":3
            } 
## 指令   正确
orderDict = {          
            'noOrder':0,
            # 模式 
            'remoteControlModel': 1, 'programeControl': 2, 'internalControlModel': 3,
            # 飞行状态
            'takeOff':4, 'landing': 5,'climb1': 6, 'decline1': 7, 'climb2': 8,
            'decline2':9, 'turnLeft':10, 'turnRight': 11,'keepHeight': 12, 
            'keepDirect': 13,
            # 发动机状态
            'bigCart': 14,'rated': 15,'cruise': 16,'slowTrain': 17,
            'idling': 18, 'preStop': 19, 'parking': 20
            } 
## 文本数据显示框
orderInfo = (
            u"无指令",
            u"遥控",u"程控",u"内控",
            u"起飞", u"着陆",u"爬升1", u"下滑1", u"爬升2",
            u"下滑2", u"左转", u"右转",u"定高平行", u"定向飞行", 
            u"大车", u"额定", u"巡航", u"慢车", u"怠速", u"预停", u"停车"
   )

edit = ('XEdit', 'YEdit', 'HEdit', 'alphaEdit', 'betaEdit', 
        'VtEdit', 'phiEdit', 'thetaEdit', 'psiEdit', 
        'pEdit', 'qEdit', 'rEdit')
# 接收数据
data = {
    'X':0, 'Y':1, 'H':2, 'alpha':3, 'beta':4, 'Vt':5,
    'phi':6, 'theta':7, 'psi':8, 'p':9, 'q':10, 'r':11,
    # 'acceptState':13, 'programeControlState':14, 'send': 15
    'acceptModel':13, 'acceptEngineStatus':14, 'acceptFlightStatus': 15,
    'send':16
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
      # self.buttonFunction = buttonFunc(self)  # 改用静态方法
      ## ================飞行状态互斥灯============================
      self.ledFlightFunction = ledFlightFunc(self)
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
      self.ui.heightView.fig.subplots_adjust(right=1, left=0.1)# 设置边距   范围为（0-1）其中右越大越靠边，左越小越靠边
      self.ui.thetaView.fig.subplots_adjust(right=1, left=0.1)
      self.ui.phiView.fig.subplots_adjust(right=1, left=0.1)
      self.ui.psiView.fig.subplots_adjust(right=1, left=0.1)
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
      self.LedFlightState = 0
      self.LedProgrameControlState = 0        ## 程控灯的状态为灭的
      self.programeControlLed_clicked = False
      self.readData_UpFigure_UpState()
      self.LedTimer = QTimer()
      self.LedTimer.stop()
      self.LedTimer.setInterval(70)   # 200ms
      self.LedTimer.start()
      self.LedTimer.timeout.connect(self.readData_UpFigure_UpState)  # 刷新指示灯状态 刷新绘图


   # ===================状态栏============================
   def __buildUI(self):
      self.LabAircraftInfo = QLabel(self)
      self.LabAircraftInfo.setMinimumWidth(300)
      self.LabAircraftInfo.setText("当前飞机状态：")
      self.ui.statusbar.addWidget(self.LabAircraftInfo)
      
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


##  ==========由connectSlotsByName()自动连接的槽函数============ 

   def on_takeOffButton_clicked(self):
      buttonFunc.takeOffButton(self)
 

   def on_landingButton_clicked(self):
      buttonFunc.landingButton(self)


   def on_keepHeightButton_clicked(self):
      buttonFunc.keepHeightButton(self)


   def on_climb1Button_clicked(self):
      buttonFunc.climb1Button(self)
      
   def on_climb2Button_clicked(self):
      buttonFunc.climb2Button(self)

   def on_decline1Button_clicked(self):
      buttonFunc.decline1Button(self)

   def on_decline2Button_clicked(self):
      buttonFunc.decline2Button(self)

   def on_turnLeftButton_clicked(self):
      buttonFunc.turnLeftButton(self)

   def on_turnRightButton_clicked(self):
      buttonFunc.turnRightButton(self)

   def on_keepDirectButton_clicked(self):
      buttonFunc.keepDirectButton(self)


   def on_programmedControlButton_clicked(self):
      buttonFunc.programmedControlButton(self)

   # 保存图片按钮
   @pyqtSlot()
   def on_saveFigButton_clicked(self):
      buttonFunc.saveFigButton(self)



##  =============自定义槽函数===============================        

## ==============自定义函数===============================
   # 设置指示灯的互斥，某一瞬间只有一个亮的
   def ledFlightStateMutex(self,clickled):
      self.ledFlightFunction.ledFlightState(clickled)

   #显示数据
   def dataShown(self):
         for i, enum in enumerate(edit):
            func = getattr(self.ui, enum).setText
            func("%.2f"%self.para[i])


   # 读取内存数据  更新绘图   更新状态灯   该函数为定时执行函数
   def readData_UpFigure_UpState(self):     # 多线程分解
      if self.ret == 0:
         self.para = self.get.readAll()
         # 小图获取数据
         self.H.updata(self.para[data['H']])
         self.theta.updata(self.para[data['theta']])
         self.phi.updata(self.para[data['phi']])
         self.psi.updata(self.para[data['psi']])
         self.ui.heightView.t = np.linspace(self.T, self.T + 10,  len(self.H.queueList))
         self.ui.thetaView.t = np.linspace(self.T, self.T + 10, len(self.theta.queueList))
         self.ui.phiView.t = np.linspace(self.T, self.T + 10, len(self.phi.queueList))
         self.ui.psiView.t = np.linspace(self.T, self.T + 10, len(self.psi.queueList))
         self.drawFigure()
         self.T += 0.1
         # 显示数据
         self.dataShown()
         #===========3维数据更新====================
         self.X.updata(self.para[data['X']])
         self.Y.updata(self.para[data['Y']])
         self.drawThreeDFigure()

         # =============地图更新=====================
         self.drawMapFigure()
         
         # ===============更新飞行状态灯=============================
         newFlightStatus = int(self.get.readOrWriteData('acceptFlightStatus','r'))
         newProgrameControlState = int(self.get.readOrWriteData('acceptModel', 'r'))

         if (self.LedFlightState != newFlightStatus):
            self.LedFlightState = newFlightStatus
            if newFlightStatus == 12:
                  self.ledFlightStateMutex('stopLed')
                  self.stopState = True
            elif newFlightStatus == 0:
               self.ledFlightStateMutex('allLedOff')
            else:
               newdict = {v: k for k, v in ledFlight.items()}  
               self.ledFlightStateMutex(newdict[newFlightStatus])
               if self.stopState == True:
                  self.stopState = False
                  self.reFig()
   
         if  self.LedProgrameControlState != newProgrameControlState:
            self.LedProgrameControlState = newProgrameControlState
            if newProgrameControlState == 1:
               print("程控灯打开")       # 这地方要改成模式集体控制
               self.ui.programeControlModelLed.state = 'on'
               self.ui.programeControlModelLed.repaint()
            else:
               print("程控灯关闭")
               self.ui.programeControlModelLed.state = 'off'
               self.ui.programeControlModelLed.repaint()
         retu = 0
      else:
         retu = -1
      return retu

   def judgeFlightState(self, state):
      for i in range(1, len(orderInfo)):
         if state == i:
            self.__LabInfo.setText("发送指令:"+orderInfo[i])

         
   def sendOrder(self, order):
      if self.ret == 0:
         self.get.readOrWriteData('send','w',orderDict[order])
         self.judgeFlightState(orderDict[order])
         print("写入指令：%d :"% int(self.get.readOrWriteData('send','r'))+ order)
         retu = 0
      else:
         retu = -1
      return retu

   def setProgrameControlOrder(self):
      if self.ret == 0:
         if int(self.get.readOrWriteData('acceptModel','r')) != 1:
            retu = self.get.readOrWriteData('send','w',orderDict['programeControl'])   
            if retu == 0:  
               self.judgeFlightState(orderDict['programeControl'])  
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

   # 使X、Y、H画图的数据截取到后二个
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
