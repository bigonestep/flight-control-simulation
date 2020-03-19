""" 
* @Author: Wang.Zhihui
* @Date: 2020-03-19 22:11:06
* @Last Modified by: Wang.Zhihui
* @Last Modified time: 2020-03-19 22:11:06
* @function: 欢迎界面
"""
# -*-coding:utf-8-*-
# cython: language_level=3
from time import sleep
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QSplashScreen
# from app import bdmaster_rc
class SplashPanel(QSplashScreen):
    def __init__(self):
        super(SplashPanel, self).__init__()
        message_font = QFont()
        message_font.setBold(True)
        message_font.setPointSize(20)
        message_font.setWeight(75)
        self.setFont(message_font)
        pixmap = QPixmap("aircraft1.jpg")
        self.setPixmap(pixmap)
        # self.showMessage('正在加载文件资源', alignment=Qt.AlignBottom, color=Qt.black)
        self.show()
        for i in range(1, 5):
            self.showMessage('正在加载文件资源{}'.format('.' * i), alignment=Qt.AlignBottom, color=Qt.black)
            sleep(0.5)
    def mousePressEvent(self, evt):
        pass
        # 重写鼠标点击事件，阻止点击后消失
    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象
    def enterEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象
    def mouseMoveEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象