"""
* @Author: Wang.Zhihui
* @Date: 2020-03-16 17:22:26  
* @Last Modified by:   Wang.Zhihui
* @Last Modified time: 2020-03-16 17:22:26
* @function:
"""
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import  QApplication, QDialog, QMessageBox

from PyQt5.QtCore import  pyqtSlot, pyqtSignal,Qt, QCoreApplication

##from PyQt5.QtWidgets import

##from PyQt5.QtGui import

##from PyQt5.QtSql import

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import
from conf import (data) 
from ui_SetParameters import Ui_setParameter

paramsCheckBox = (
    "getClimb1Theta", "getClimb2Theta", "getDecline1Theta",
    "getDecline2Theta", "getHight", "getTurnLeftPsi","getTurnRightPsi"
)
paramsSpinBox = (
    "setClimb1Theta", "setClimb2Theta", "setDecline1Theta",
    "setDecline2Theta", "setHight", "setTurnLeftPsi", "setTurnRightPsi"
)

setParamTable = (
    'sedClimb1Theta', 'setClimb2Theta', 'setDecline1Theta', 
    'setDecline2Theta', 'setHight', 'setTurnLeftPsi',
    'setTurnRightPsi'
)

class QsetParameters(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui = Ui_setParameter()        # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.parent = parent
        self.parent_data = []
        self.savePrivData()     # 保存原始数据
        self.showPrivData()
        
        # 确定键关联槽函数
        self.ui.btnOK.clicked.connect(self.ok_button)
        # 取消键关联槽函数
        self.ui.btnCancel.clicked.connect(self.reject)
        # 重置键关联槽函数
        self.ui.btnReset.clicked.connect(self.reset_button)
        # 全选关联槽函数
        self.ui.getAll.stateChanged.connect(self.on_getAll_clicked)
##  ============自定义功能函数========================

    def savePrivData(self):
        for i in range(data['sedClimb1Theta'], data['setTurnRightPsi']+1):
            self.parent_data.append(self.parent.para[i])
            print("parent.para:",self.parent_data)
    
    # 初始化原始的数据
    def showPrivData(self):
        for i in range(len(paramsSpinBox)):
            getattr(self.ui, paramsSpinBox[i]).setValue(self.parent_data[i])

    # 全选
    @pyqtSlot()
    def on_getAll_clicked(self, ):
        if self.ui.getAll.isChecked():
            for i in range(0, len(paramsCheckBox)):
                getattr(self.ui, paramsCheckBox[i]).setChecked(True)
        else:
            for i in range(0, len(paramsCheckBox)):
                getattr(self.ui, paramsCheckBox[i]).setChecked(False)
    
    # 确定键 发送数据
    def ok_button(self):    
        print("ok_button(self)")
        for i in range(len(paramsCheckBox)):
            if getattr(self.ui,paramsCheckBox[i]).isChecked():
                self.parent.get.readOrWriteData(setParamTable[i], 'w', 
                                                getattr(self.ui,paramsSpinBox[i]).value())
                self.parent_data[i] = getattr(self.ui,paramsSpinBox[i]).value()
        dlgTitle = u"消息"                # 弹出警告窗
        strInfo = u"发送参数成功"
        QMessageBox.information(self, dlgTitle, strInfo)
                # 更新原始重置数据
        
            
    # 重置键重置数据
    @pyqtSlot()
    def reset_button(self):
        self.showPrivData()



    

##  ===========event处理函数==========================
        
        
##  ========由connectSlotsByName()自动连接的槽函数=========
        
        
##  ==========自定义槽函数===============================      


   
##  ============窗体测试程序 ============================
if  __name__ == "__main__":         #用于当前窗体测试
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)     #创建GUI应用程序
    form = QsetParameters()                 #创建窗体
    form.show()
    sys.exit(app.exec_())
