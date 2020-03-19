# -*- coding: utf-8 -*-
"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-26 02:07:40  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-26 02:07:40  
* @function: 主界面
"""

import sys
from time import sleep
from os import path
from win32con import KEYEVENTF_KEYUP
from win32gui import (GetWindowText, SetForegroundWindow, 
                      IsWindowVisible, IsWindowEnabled,
                      EnumWindows)
from win32process import GetWindowThreadProcessId
from subprocess import Popen
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QPixmap, QFont
from PyQt5.QtCore import (pyqtSlot, pyqtSignal, Qt, QDir, 
                          QCoreApplication, QT_VERSION_STR)
from win32api import ShellExecute, keybd_event
from multiprocessing import Process, freeze_support

from myMainWindow import QmyMainWindow
from ui_MainWelcome import Ui_MainWelcome
from configparser import ConfigParser
from splashPanel import SplashPanel  #  主界面的等待界面


class QmyWidget(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui=Ui_MainWelcome()       # 创建UI对象
        self.ui.setupUi(self)     # 构造UI界面
        # 按钮设置
        self.ui.pycharmButton.setStyleSheet("background-color: #016cb4")
        self.ui.matlabButton.setStyleSheet("background-color: #016cb4")
        self.ui.mainSystemButton.setStyleSheet("background-color: #016cb4")
        self.ui.flightButton.setStyleSheet("background-color: #016cb4")

        self.pycharmPath = None
        self.pyProjectPath = None
        self.RhPath = None
        self.RhProjectPath = None
        self.RhapsodyPath = None
        self.RhapsodyProjectPath = None
        self.matlabPath = None
        self.matlabProjectPath = None
        self.rhapsody_project = False    # 默认rhapsody工程打开标志
        self.ini()

    def ini(self):
        config = ConfigParser()
        config.read("projectPath.ini", encoding='utf-8')
        paths = ["pycharmPath", "pyProjectPath", "RhapsodyPath", "RhapsodyProjectPath",
                "matlabPath", "RhapsodyProjectExePath"]
        name = ["pycharm软件路径", "pycharm项目的路径","Rhapsody软件路径",
                "Rhapsody项目的路径", "matlab软件路径", 
                "Rhapsody项目编译之后的可执行文件路径"]
        dictPath = dict(zip(paths, name))
        
        self.openRhapsodyTime = int(config['DEFAULT']['openRhapsodyTime'])
        self.openRhapsodyExeTime = int(config['DEFAULT']['openRhapsodyExeTime'])


        
        for path in paths:
            if path in config['DEFAULT']:
                setattr(self, path, config['DEFAULT'][path]) 
                # 利用反射给属性赋值
            else:
                dlgTitle = u"错误"
                strInfo = dictPath[path] + "设置错误, 请在projectPath.ini文件中设置"
                QMessageBox.critical(self, dlgTitle, strInfo)
                sys.exit(0)

    #  ==============自定义功能函数========================

    # style='line-height:70%'
    #  ==============event处理函数==========================

    def paintEvent(self, event):
        painter = QPainter(self)
        pic = QPixmap("J21.jpg")
        painter.drawPixmap(0, 0, self.width(), self.height(), pic)
        super().paintEvent(event)

    def closeEvent(self, event):
        dlgTitle = "警告"
        strInfo = "确定关闭多模态控制系统建模与仿真环境"
        defaultBtn = QMessageBox.NoButton

        result = QMessageBox.question(self, dlgTitle, strInfo,
                                      QMessageBox.Yes | QMessageBox.No,
                                      defaultBtn
                                      )

        if result == QMessageBox.Yes:
            event.accept()
            
        else:
            event.ignore()

    #  ==========由connectSlotsByName()自动连接的槽函数============
    @pyqtSlot()   # 指定函数为槽函数
    def on_pycharmButton_clicked(self):
        # 该函数为打开pycharm按键的槽函数，即按下按键会执行该函数

        u"""
         #判断文件是否存在，若存在则再判断，路径是否正确，方法判断路径里面是否含有"pycharm"，该方法不严谨，但基本够用，
         若无误则使用win32api.ShellExecute（）函数打开
         若不存在则调用打开文件窗口，选择程序打开,若选择的不是指定软件，则弹出警告窗口。需要重新选择
         以下三个按键都一个逻辑
        """
        if path.isfile(self.pycharmPath) and path.isdir(self.pyProjectPath):

            if "pycharm" in self.pycharmPath.lower():
                ShellExecute(0, 'open', self.pycharmPath, self.pyProjectPath, '', 1)
                # 其中前两个为固定，第三个为打开软件的路径，
                # 第四个是使用该软件打开该文件（或文件夹）
                # 若没有则放空字符 ''
                # print("打开PyCharm成功！！！")
        else:
            curPath = QDir.currentPath()
            dlgTitle = u"打开PyCharm软件"
            filt = u"执行程序(*.exe);;所有文件(*.*)"
            filename, _ = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
            if "pycharm" in filename.lower():
                ShellExecute(0, 'open', filename, '', '', 1)
            elif filename == '':
                pass
            else:
                dlgTitle = u"打开错误"
                strInfo = u"请打开PyCharm程序"
                QMessageBox.critical(self, dlgTitle, strInfo)

    @pyqtSlot()
    def on_matlabButton_clicked(self):
        if path.isfile(self.matlabPath):
            if "matlab" in self.matlabPath.lower():
                ShellExecute(0, 'open', self.matlabPath,'', '', 1)
                
        else:
            curPath = QDir.currentPath()
            dlgTitle = u"打开MatLab软件"
            filt = u"执行程序(*.exe);;所有文件(*.*)"
            filename, _ = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
            if "matlab" in filename.lower():
                ShellExecute(0, 'open', filename, '', '', 1)
            elif filename == '':
                pass
            else:
                dlgTitle = u"打开错误"
                strInfo = u"请打开MatLab程序"
                QMessageBox.critical(self, dlgTitle, strInfo)


    @pyqtSlot()
    def on_flightButton_clicked(self):
        # 项目打开成功了，然后打开主面板
        mainWindow = MainWindow("flightButton", None)
        mainWindow.start()
        sleep(5)
        # 打开控制界面的槽函数
        if path.isfile(self.RhapsodyProjectExePath):
            if  '.exe' in self.RhapsodyProjectExePath:
                ShellExecute(0, 'open', self.RhapsodyProjectExePath, "", '', 1)
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

    

    @pyqtSlot() # 
    def on_mainSystemButton_clicked(self):
        # 打开主面板
        # 打开rhapsody软件
        if path.isfile(self.RhapsodyPath) and path.isfile(self.RhapsodyProjectPath):
            if "rhapsody" in self.RhapsodyPath.lower() and '.rpy' in self.RhapsodyProjectPath:
                # win32api.ShellExecute(0, 'open', self.RhapsodyPath, self.RhapsodyProjectPath, '', 1)
                Rhapsody = Popen([self.RhapsodyPath, self.RhapsodyProjectPath])
                print(Rhapsody)
                # print("打开rhapsody成功！！！")
        else:
            curPath = QDir.currentPath()
            dlgTitle = u"打开Rhapsody软件"
            filt = u"执行程序(*.exe);;所有文件(*.*)"
            filename, _ = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
            if "sublime_text" in filename.lower():
                Rhapsody = Popen([filename])
            elif filename == '':
                pass
            else:
                dlgTitle = u"打开错误"
                strInfo = u"请打开Rhapsody程序"
                QMessageBox.critical(self, dlgTitle, strInfo)
        sleep(self.openRhapsodyTime)   # 5秒

        #打开工程编译的.exe文件
        if path.isfile(self.RhapsodyProjectExePath):
            if  '.exe' in self.RhapsodyProjectExePath:
                ShellExecute(0, 'open', self.RhapsodyProjectExePath, "", '', 1)
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
        sleep(self.openRhapsodyExeTime)  # 这个时间是等待Rhapsody加载工程
        # TODO: 模拟键盘发送一个F4, 问题怎么把软件的焦点防御rhapsody
        # 先获取焦点
        hand = None
        try:
            for hwnd in get_hwnds_for_pid(Rhapsody.pid):
                print(hwnd, "=>", GetWindowText (hwnd))
                keybd_event(13,0,0,0)
                hand = hwnd
                SetForegroundWindow(hwnd)
                sleep(0.1)
                # 按下快捷键
                keybd_event(115,0,0,0)  #F4键位码是115
                sleep(0.01)
                keybd_event(115,0,KEYEVENTF_KEYUP,0) #释放按键115
                break
        except UnboundLocalError:
            dlgTitle = u"打开错误"
            strInfo = u"打开Rhapsody程序打开错误"
            QMessageBox.critical(self, dlgTitle, strInfo)
        sleep(0.5)
        mainWindow = MainWindow("mainSystemButton", hand )
        mainWindow.start()
        

class MainWindow(Process):
    def __init__(self, flog, hand):
        Process.__init__(self)
        self.flog = flog
        self.hand = hand

    def run(self):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        mainapp = QApplication(sys.argv)  # 创建GUI应用程序
        mainform = QmyMainWindow(self.flog, self.hand)  # 创建窗体
        mainform.show()

        sys.exit(mainapp.exec_())


# 查找PID号
def get_hwnds_for_pid (pid):
    def callback (hwnd, hwnds):
        if IsWindowVisible (hwnd) and IsWindowEnabled (hwnd):
            _, found_pid = GetWindowThreadProcessId (hwnd)
            if found_pid == pid:
                hwnds.append (hwnd)
            return True
    hwnds = []
    EnumWindows (callback, hwnds)
    return hwnds


#  ============窗体测试程序 ================================


if __name__ == "__main__":  # 用于当前窗体测试
    freeze_support()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # 由于使用了多线程，使用pyinstaller打包的时候要加上这句
    app = 0  # 清除上次运行的残留
    app = QApplication(sys.argv)  # 创建GUI应用程序

    splash = SplashPanel()
    splash.show()
    app.processEvents()  # 防止进程卡死
    
    form = QmyWidget()  # 创建窗体
    form.show()

    splash.finish(form)  # 关闭欢迎界面
    splash.deleteLater()
    sys.exit(app.exec_())
