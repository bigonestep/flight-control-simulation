"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-26 01:35:47  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-26 01:35:47  
* @function:   绘制二维三维曲线
"""

# 自定义类 QmyFigureCanvas，父类QWidget
# 创建了FigureCanvas和NavigationToolbar，组成一个整体
# 便于可视化设计

import sys
from numpy import array
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QTimer, QMargins
from PyQt5.QtWidgets import QWidget
from matplotlib import rcParams
import matplotlib.figure as figure
from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.style as mplStyle  # 一个模块

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D  # 一定不能注释

from PyQt5.QtWidgets import QVBoxLayout

import matplotlib.image as img


class QmyFigureCanvas(QWidget):
    mapChanged = pyqtSignal(str)  # 发送一个地图名称

    def __init__(self, parent=None, toolbarVisible=True, showHint=False):

        # 类初始化

        super().__init__(parent)
        mplStyle.use("classic")  # 使用样式，必须在绘图之前调用,修改字体后才可显示汉字

        rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']  # 显示汉字为 楷体， 汉字不支持 粗体，斜体等设置
        rcParams['font.size'] = 15
        rcParams['axes.unicode_minus'] = False  # 减号unicode编码
        self.xmajorFormatter = FormatStrFormatter('%1.1f')

        self.fig = None  # 二维图的画图对象
        self.axMap = None  # 地图的画图对象
        self.ax3D = None  # 三维画图的对象

        self.bgimg = img.imread(r'./map/1.png')  # 地图的画图的背景

        self.t = None  # 二维图的x轴序列

    #  ==============自定义功能函数========================
    def createFigure(self):
        """

        创建二维画图的画布 ，一般都是这个步骤
        先得到一个mpl.figure.Figure对象 fig
        然后把该对象加入到 Qt留出来的空白画图区
        设置画图为 1 幅
        """
        self.fig = figure.Figure(dpi=80)
        figCanvas = FigureCanvas(self.fig)  # 创建FigureCanvas对象，必须传递一个Figure对象
        # self.fig.subplots_adjust(bottom=0.17)

        self.ax1 = self.fig.add_subplot(1, 1, 1)
        # (1,1,1)代表为横着为1幅竖着为1幅，第1幅  若是竖着两个子图的第一幅 则为（2，1，1）

        # self.fig.subplots_adjust(right=1, left=0.17)  # 设置边距   范围为（0-1）其中右越大越靠边，左越小越靠边

        # 设置坐标轴标签的格式这里  self.xmajorFormatter = FormatStrFormatter('%1.1f')，必须这样
        self.ax1.xaxis.set_major_formatter(self.xmajorFormatter)
        self.ax1.yaxis.set_major_formatter(self.xmajorFormatter)

        layout = QVBoxLayout(self)
        layout.addWidget(figCanvas)  # 添加FigureCanvas对象到空白处
        layout.setContentsMargins(0, 0, 0, 0)  # 这个一般都这么写
        layout.setSpacing(0)

    # 绘制二维曲线
    def drawFig(self, name, x_name, y):  ##初始化绘图
        self.ax1.cla()  # 动态图，更新图要删除上一幅，必须
        self.lineFig = self.ax1.plot(self.t, y, '-', label="height", linewidth=1)[0]  # 绘制一条曲线
        self.ax1.set_xlabel(x_name)  # X轴标题
        self.ax1.set_ylabel(name)  # Y轴标题

        self.fig.canvas.draw()

    def updateFig(self, y, y_min, y_max, x_min, x_max):
        self.lineFig.set_xdata(self.t)
        self.lineFig.set_ydata(y)
        self.ax1.set_xlim([x_min, x_max])  # X轴坐标范围
        self.ax1.set_ylim([y_min, y_max])  # Y轴坐标范围
        self.fig.canvas.draw()

    # 以下画三维，画地图都大同小异
    # 创建三维曲线
    def createThreeDFigure(self):

        self.figure = figure.Figure(dpi=80)
        figCanvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(figCanvas)  # 添加FigureCanvas对象
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    # 3维曲线初始设置
    def iniThreeDFigure(self):
        self.figure.clear()
        self.figure.subplots_adjust(bottom=0, right=1, top=1, left=0)
        self.ax3D = self.figure.add_subplot(1, 1, 1, projection='3d', label="plot3D")

    # 绘制三维图
    def drawThreeFig(self, x, y, z):
        self.ax3D.cla()
        self.threeFigLine = self.ax3D.plot3D(x, y, z, '-')[0]
        self.ax3D.set_xlabel("X")
        self.ax3D.set_ylabel("Y")
        self.ax3D.set_zlabel("H")
        self.figure.canvas.draw()

    def updataThreeFig(self, x, y, z, xmin, xmax, ymin, ymax, zmin, zmax):
        # ============================注意=======================
        # set_data_3d函数 只有再matplotlib版本大于3.1.2才有
        x = array(x)
        y = array(y)
        z = array(z)
        self.threeFigLine.set_data_3d(x, y, z)

        self.ax3D.set_xlim([xmin, xmax])
        self.ax3D.set_ylim([ymin, ymax])
        self.ax3D.set_zlim([zmin, zmax])
        self.figure.canvas.draw()

    # 创建地图二维图的画布
    def createMapFigure(self):

        self.figure = figure.Figure(dpi=80)
        self.figure.clear()
        self.figure.figimage(self.bgimg, zorder=10)

        figCanvas = FigureCanvas(self.figure)
        # self.figure.subplots_adjust(bottom=0,right=1, top=1, left=0)   #x y轴都不显示
        # self.figure.subplots_adjust(bottom=0.08, right=1, top=1, left=0)
        self.figure.subplots_adjust(bottom=0, right=1, top=1, left=0)
        self.axMap = self.figure.add_subplot(1, 1, 1, label="map", zorder=20)

        self.axMap.set_axis_off()
        layout = QVBoxLayout(self)
        layout.addWidget(figCanvas)  # 添加FigureCanvas对象
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.lastMapName = '1.png'
        self.mapChanged.connect(self.do_mapChange)  # 绑定地图改变函数

    # 绘制地图
    def drawMapFig(self, x, y):
        self.axMap.cla()
        self.axMap.patch.set_alpha(0)
        self.mapFigLine = self.axMap.plot(x, y, '-', linewidth=3, color='r')[0]
        self.axMap.set_xlabel("X")
        self.axMap.set_ylabel("Y")
        self.figure.canvas.draw()

    # 更新地图数据
    def updataMapFig(self, x, y, xmin, xmax, ymin, ymax):
        self.mapFigLine.set_xdata(x)
        self.mapFigLine.set_ydata(y)
        self.axMap.set_xlim([xmin, xmax])
        self.axMap.set_ylim([ymin, ymax])
        self.figure.canvas.draw()

    # 更换地图背景的信号
    # 思想为根据x轴的距离来更换
    @staticmethod
    def mapAxis(lt):
        max_axis = max(lt)
        # min_axis = min(lt)
        if max_axis < 500:
            min_axis = 0
            max_axis = 600
            # self.mapChanged.emit('./map/1.png')
        elif max_axis < 1000:
            # self.mapChanged.emit('./map/2.png')
            max_axis = 1000
            min_axis = 400
        elif max_axis < 1500:
            max_axis = 1500
            min_axis = 900
            # self.mapChanged.emit('./map/3.png')
        elif max_axis < 2000:
            max_axis = 2000
            min_axis = 1400
            # self.mapChanged.emit('./map/4.png')
        elif max_axis < 2500:
            max_axis = 2500
            min_axis = 1900
            # self.mapChanged.emit('./map/5.png')
        elif max_axis < 3000:
            max_axis = 3000
            min_axis = 2400
            # self.mapChanged.emit('./map/6.png')
        elif max_axis < 3500:
            max_axis = 3500
            min_axis = 2900
            # self.mapChanged.emit('./map/7.png')
        elif max_axis < 4000:
            max_axis = 4000
            min_axis = 3400
            # self.mapChanged.emit('./map/8.png')
        else:
            max_axis += 500
            min_axis = 3900
        return min_axis, max_axis

    # 更换地图背景的槽函数
    @pyqtSlot(str)
    def do_mapChange(self, mapName):
        if mapName != self.lastMapName:
            self.lastMapName = mapName
            self.bgimg = img.imread(mapName)
            self.figure.figimage(self.bgimg, zorder=10)
