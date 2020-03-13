import sys, os, requests
from PyQt5 import QtWidgets, QtCore, QtGui
from configparser import ConfigParser

# TODO: 简化导入
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from time import sleep


class baiduMap(object):
    def __init__(self, mapView, x ,y ):
        self.browser = None
        self.mapView = mapView
        self.x = x
        self.y = y
        self.baiduBrowser()

    def baiduBrowser(self):
        self.browser = QWebEngineView(self.mapView)
        vv = QVBoxLayout()
        vv.setContentsMargins(0, 0, 0, 0)
        # 设置四周边界
        vv.addWidget(self.browser)
        self.mapView.setLayout(vv)
        # 指定打开界面的 URL

        url = r"file:///./map.html"
        self.browser.setUrl(QUrl(url))
        jsFunction = "init({0}, {1});".format(self.x, self.y)
        self.browser.page().runJavaScript(jsFunction)

    def autoShow(self, x, y):
        # TODO: 错误
        x = x * 0.00000899   # 经度转换米转换成gps坐标，误差很大
        y = y * 0.00001141   # 以北纬38度为基准
        print("x, y", x, y)
        jsFunction = "dynamicLine({0}, {1});".format(x, y)
        self.browser.page().runJavaScript(jsFunction)
        print(jsFunction)




class getCity(object):
    def __init__(self):
        self.MY_WEATHER_KEY = None
        self.url_now = None
        self.getUrl()

    def getUrl(self):
        config = ConfigParser()
        config.read("projectPath.ini", encoding='utf-8')

        self.url_now = r"https://free-api.heweather.net/s6/weather/now?location=auto_ip&" \
                       r"key={0}".format(config['mapconfig']["key"])

    def getLocal(self):
        # TODO:处理一下错误信息
        self.log = requests.get(self.url_now).json()
        now_APIcity = self.log['HeWeather6'][0]['basic']
        lat = now_APIcity['lat']
        lon = now_APIcity['lon']
        return lon, lat


if __name__ == '__main__':
    new = getCity()
    loc = new.getLocal()
    print(loc)










