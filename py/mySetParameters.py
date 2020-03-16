"""
* @Author: Wang.Zhihui
* @Date: 2020-03-16 17:22:26  
* @Last Modified by:   Wang.Zhihui
* @Last Modified time: 2020-03-16 17:22:26
* @function:
"""
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import  QApplication, QDialog

from PyQt5.QtCore import  pyqtSlot, pyqtSignal,Qt, QCoreApplication

##from PyQt5.QtWidgets import

##from PyQt5.QtGui import

##from PyQt5.QtSql import

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import

from ui_SetParameters import Ui_setParameter


class QmyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui = Ui_setParameter()        # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面

        self.ui.btnOK.clicked.connect(self.accept)
        self.ui.btnCancel.clicked.connect(self.reject)
##  ============自定义功能函数========================


##  ===========event处理函数==========================
        
        
##  ========由connectSlotsByName()自动连接的槽函数=========
        
        
##  ==========自定义槽函数===============================      


   
##  ============窗体测试程序 ============================
if  __name__ == "__main__":         #用于当前窗体测试
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)     #创建GUI应用程序
    form = QmyDialog()                 #创建窗体
    form.show()
    sys.exit(app.exec_())
