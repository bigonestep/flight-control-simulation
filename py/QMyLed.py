# -*- coding: utf-8 -*-
''' 
* @Author: Wang.Zhihui  
* @Date: 2020-02-25 14:56:04  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-25 14:56:04  
* @function: LED灯控件
'''

from PyQt5.QtGui import (QPainter, QPen, QRadialGradient, QColor, QBrush)
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF

"""
该控件可以直接使用，不需要理解
使用方法在Qt Create界面中防止一个QWidget控件，然后点击右键，
提升为...,在弹出界面第一个格子里面填QMyLed，第二个格子默认即可。

控制亮灭的方法，设置亮:
self.state = 'on'
self.takeOffLed.repaint()
"""
allAttributes = ['colorOnBegin', 'colorOnEnd', 'colorOffBegin',
                 'colorOffEnd', 'colorBorderIn', 'colorBorderOut',
                 'radiusBorderOut', 'radiusBorderIn', 'radiusCircle']
allDefaultVal = [QColor(0, 240, 0), QColor(0, 160, 0), QColor(0, 68, 0),
                 QColor(0, 28, 0), QColor(140, 140, 140), QColor(100, 100, 100),
                 500, 450, 400]
allLabelNames = [u'灯亮圆心颜色：', u'灯亮边缘颜色：', u'灯灭圆心颜色：',
                 u'灯灭边缘颜色：', u'边框内测颜色：', u'边框外侧颜色：',
                 u'边框外侧半径：', u'边框内侧半径：', u'中间圆灯半径：']


class QMyLed(QWidget):
    def __init__(self, parent=None, state='off'):
        super(QMyLed, self).__init__(parent)
        self.initUI()
        self.state = state

    def initUI(self):
        self.setMinimumSize(24, 24)
        self.scaledSize = 1000.0  # 为方便计算，将窗口短边值映射为1000
        self.setLedDefaultOption()

    def setLedDefaultOption(self):
        for attr, val in zip(allAttributes, allDefaultVal):
            setattr(self, attr, val)
        self.update()

    def setLedOption(self, opt='colorOnBegin', val=QColor(0, 240, 0)):
        if hasattr(self, opt):
            setattr(self, opt, val)
            self.update()

    def resizeEvent(self, evt):
        self.update()

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(Qt.black, 1))

        realSize = min(self.width(), self.height())  # 窗口的短边
        painter.translate(self.width() / 2.0, self.height() / 2.0)  # 原点平移到窗口中心
        painter.scale(realSize / self.scaledSize, realSize / self.scaledSize)  # 缩放，窗口的短边值映射为self.scaledSize
        gradient = QRadialGradient(QPointF(0, 0), self.scaledSize / 2.0, QPointF(0, 0))  # 辐射渐变

        # 画边框外圈和内圈
        for color, radius in [(self.colorBorderOut, self.radiusBorderOut),  # 边框外圈
                              (self.colorBorderIn, self.radiusBorderIn)]:  # 边框内圈
            gradient.setColorAt(1, color)
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(QPointF(0, 0), radius, radius)

        # 画内圆
        if self.state == 'off':
            gradient.setColorAt(0, self.colorOffBegin)
            gradient.setColorAt(1, self.colorOffEnd)
        else:
            gradient.setColorAt(0, self.colorOnBegin)
            gradient.setColorAt(1, self.colorOnEnd)

        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), self.radiusCircle, self.radiusCircle)
