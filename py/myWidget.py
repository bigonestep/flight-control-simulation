# -*- coding: utf-8 -*-

import sys,os

#import subprocess
from PyQt5.QtWidgets import  QApplication, QWidget,QMessageBox,QMainWindow,QFileDialog
#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter,QPixmap
from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt,QDir
import win32api


##from PyQt5.QtWidgets import  

from PyQt5.QtGui import QIcon

##from PyQt5.QtSql import 

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import



from myMainWindow import QmyMainWindow
from ui_MainWelcome import Ui_MainWelcome
class QmyWidget(QMainWindow): 

   def __init__(self, parent=None):
      super().__init__(parent)  #调用父类构造函数，创建窗体
      self.ui=Ui_MainWelcome()       #创建UI对象
      self.ui.setupUi(self)     #构造UI界面
      # 按钮设置
      self.ui.pycharmButton.setStyleSheet("background-color: #016cb4")
      self.ui.matlabButton.setStyleSheet("background-color: #016cb4")
      self.ui.mainSystemButton.setStyleSheet("background-color: #016cb4")
      self.ui.RhapsodyButton.setStyleSheet("background-color: #016cb4")
   

      self.pycharmPath = None
      self.pyProjectPath = None
      self.RhPath = None
      self.RhProjectPath = None
      self.ini()
      
     
      
   def ini(self):
      self.pycharmPath = r"D:\Program Files\JetBrains\PyCharm 2019.2.3\bin\pycharm64.exe"
      self.pyProjectPath = r"E:\project\py\py (4)"
      self.RhapsodyPath = r"C:\Program Files\IBM\Rational\Rhapsody\8.0.6\rhapsody.exe"
      self.RhapsodyProjectPath = r"E:\ZWYMav\CosimMAV\CosimMAV.rpy"
      self.matlabPath = r"D:\MATLAB\R2016b\bin\win64\MATLAB.exe"
      self.matlabProjectPath = r""

##  ==============自定义功能函数========================

##style='line-height:70%'
##  ==============event处理函数==========================
   
   def paintEvent(self,event):
      painter = QPainter(self)
      pic = QPixmap("J21.jpg")
      painter.drawPixmap(0,0,self.width(),self.height(),pic)
      super().paintEvent(event)   
   def closeEvent(self,event):
      dlgTitle = "警告"
      strInfo = "确定关闭多模态控制系统建模与仿真环境" 
      defaultBtn = QMessageBox.NoButton
      
      result=QMessageBox.question(self,dlgTitle,strInfo,
                                 QMessageBox.Yes|QMessageBox.No,
                                 defaultBtn
                                 )
                        
      if (result == QMessageBox.Yes):
         event.accept()
      else:
         event.ignore()
        
##  ==========由connectSlotsByName()自动连接的槽函数============   
   @pyqtSlot()   # 指定函数为槽函数
   def on_pycharmButton_clicked(self):
      # 该函数为打开pycharm按键的槽函数，即按下按键会执行该函数

      '''
       #判断文件是否存在，若存在则再判断，路径是否正确，方法判断路径里面是否含有"pycharm"，该方法不严谨，但基本够用，
       若无误则使用win32api.ShellExecute（）函数打开
       若不存在则调用打开文件窗口，选择程序打开,若选择的不是指定软件，则弹出警告窗口。需要重新选择
       以下三个按键都一个逻辑
      '''
      if os.path.isfile(self.pycharmPath) and os.path.isdir(self.pyProjectPath):

         if "pycharm" in self.pycharmPath.lower():
            win32api.ShellExecute(0, 'open', self.pycharmPath, self.pyProjectPath, '', 1)#其中前两个为固定，第三个为打开软件的路径，
                                                                                          # 第四个是使用该软件打开该文件（或文件夹）
                                                                                          # 若没有则放空字符 ''
            print("打开PyCharm成功！！！")
      else:
         curPath = QDir.currentPath()
         dlgTitle = "打开PyCharm软件"
         filt = "执行程序(*.exe);;所有文件(*.*)"
         filename,filtUsed=QFileDialog.getOpenFileName(self,dlgTitle,curPath,filt)
         if "pycharm" in filename.lower():
            win32api.ShellExecute(0, 'open', filename, '', '', 1)
         elif  filename == '':
            pass
         else:
            dlgTitle="打开错误"
            strInfo="请打开PyCharm程序"
            QMessageBox.critical(self, dlgTitle, strInfo)

            
         
   @pyqtSlot()
   def on_matlabButton_clicked(self):
      print("matlab")
      if os.path.isfile(self.matlabPath) and os.path.isdir(self.matlabProjectPath):
         print("os.path.isfile(self.matlabPath)")
         if "matlab" in self.matlabPath.lower():
            print("")
            win32api.ShellExecute(0, 'open', self.matlabPath, self.matlabProjectPath, '', 1)
            print("打开matlab成功！！！")
      else:
         curPath = QDir.currentPath()
         dlgTitle = "打开MatLab软件"
         filt = "执行程序(*.exe);;所有文件(*.*)"
         filename,filtUsed=QFileDialog.getOpenFileName(self,dlgTitle,curPath,filt)
         if "matlab" in filename.lower():
            win32api.ShellExecute(0, 'open', filename, '', '', 1)
         elif  filename == '':
            pass
         else:
            dlgTitle="打开错误"
            strInfo="请打开MatLab程序"
            QMessageBox.critical(self, dlgTitle, strInfo)

      

   @pyqtSlot()
   def on_RhapsodyButton_clicked(self):
      print("Rh")
      if os.path.isfile(self.RhapsodyPath) and os.path.isfile(self.RhapsodyProjectPath):
         if "rhapsody" in self.RhapsodyPath.lower() and '.rpy' in self.RhapsodyProjectPath:
            win32api.ShellExecute(0, 'open',self.RhapsodyPath, self.RhapsodyProjectPath, '', 1)
            print("打开rhapsody成功！！！")
      else:
         curPath = QDir.currentPath()
         dlgTitle = "打开Rhapsody软件"
         filt = "执行程序(*.exe);;所有文件(*.*)"
         filename,filtUsed=QFileDialog.getOpenFileName(self,dlgTitle,curPath,filt)
         if "rhapsody" in filename.lower():
            #os.system('"'+filename+'"')
            win32api.ShellExecute(0, 'open', filename, "", '', 1)
         elif  filename == '':
            pass
         else:
            dlgTitle="打开错误"
            strInfo="请打开Rhapsody程序"
            QMessageBox.critical(self, dlgTitle, strInfo)

   @pyqtSlot()
   def on_mainSystemButton_clicked(self):
      '''打开控制界面的槽函数'''
      #app = QApplication(sys.argv)    #创建GUI应用程序
      form=QmyMainWindow(self)            #创建窗体
      form.setAttribute(Qt.WA_DeleteOnClose)

      form.show()
      
      




        
##  =============自定义槽函数===============================        


   
##  ============窗体测试程序 ================================
if  __name__ == "__main__":        #用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序
   form=QmyWidget()                #创建窗体
   

   form.show()

   sys.exit(app.exec_())
