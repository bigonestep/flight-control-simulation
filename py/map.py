""" 
* @Author: Wang.Zhihui  
* @Date: 2020-03-16 16:19:13  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-03-16 16:19:13  
* @function: 
"""


from requests import get, exceptions

from PyQt5 import QtCore, QtGui, QtWidgets

from configparser import ConfigParser

from PyQt5.QtWidgets import QVBoxLayout

# from PyQt5.QtGui import *

from PyQt5.QtCore import QUrl

from PyQt5.QtWebEngineWidgets import QWebEngineView


class baiduMap(object):
    def __init__(self, mapView, x, y):
        self.browser = None
        self.mapView = mapView
        self.x = x
        self.y = y
        self.baiduBrowser()
        self.getUrl()

    def getUrl(self):
        config = ConfigParser()
        config.read("projectPath.ini", encoding='utf-8')
        key = config["mapconfig"]["baidu_key"]
        self.html = """<!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
        <style type="text/css">
        body, html,#allmap {width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}
        </style>
        <script type="text/javascript" src="http://api.map.baidu.com/api?v=3.0&ak=""" + key + """/">

        </script>
        <title>轨迹动态展示</title>
        </head>
        <body>
        <div id="allmap"></div>
        </body>
        </html>
        <script type="text/javascript">
        //数据准备,  
        var points = [];//原始点信息数组  
        var bPoints = [];//百度化坐标数组。用于更新显示范围。
        //var city = "北京"
        var flag = true;
        var num = 0;
        // ###########################以下两行为26 27 不能动######################
        // var pointX = 116.404;
        // var pointY = 39.915;
        """ + "var pointX = " + self.x + "\n" + "var pointY = " + self.y + "\n" + """
        // var pointX = 114.34144592;
        // var pointY = 34.79705048;

        function init(){
            pointX = pointX
            pointY = pointY
        }
        // ###################################################################
        //创建标注点并添加到地图中
        function addMarker(points) {
            //循环建立标注点
            for(var i=0, pointsLen = points.length; i<pointsLen; i++) {

                var point = new BMap.Point(points[i].lng, points[i].lat); //将标注点转化成地图上的点
                var marker = new BMap.Marker(point); //将点转化成标注点
                if(num%50 == 0){
                    map.addOverlay(marker);  //将标注点添加到地图上
                    }
                num += 1;
                //添加监听事件
                (function() {
                    var thePoint = points[i];
                    marker.addEventListener("click",
                        function() {
                        showInfo(this,thePoint);
                    });
                 })();
            }
        }

        //添加线  
        function addLine(points){  

            var linePoints = [],pointsLen = points.length,i,polyline;  
            if(pointsLen == 0){  
                return;  
            }  
            // 创建标注对象并添加到地图     
            for(i = 0;i <pointsLen;i++){  
                linePoints.push(new BMap.Point(points[i].lng,points[i].lat));  
            }  

            polyline = new BMap.Polyline(linePoints, {strokeColor:"blue", strokeWeight:5, strokeOpacity:1});   //创建折线  
            map.addOverlay(polyline);   //增加折线  
        }

        // 随机生成新的点，加入到轨迹中
        function dynamicLine(x, y){
            var lng = pointX+x;
            var lat = pointY+y;


            var point = {"lng":lng,"lat":lat,"status":1,"id":15}  // 设置点
            var makerPoints = [];  
            var newLinePoints = [];  
            var len;  

            makerPoints.push(point);      // 每次添加一个点         
            addMarker(makerPoints);      //增加对应该的轨迹点
            points.push(point);           //加到总数组   
            bPoints.push(new BMap.Point(lng,lat));  //百度坐标数据也加一个
            len = points.length;  
            newLinePoints = points.slice(len-2, len);//最后两个点用来画线。  

            addLine(newLinePoints);//增加轨迹线
            if(flag){
            setZoom(bPoints);      //  更新地图的范围
                flag = false;
            }

            // setTimeout(dynamicLine, 1000);       // 每秒刷新一次
        }  


        //根据点信息实时更新地图显示范围，让轨迹完整显示。设置新的中心点和显示级别  
        function setZoom(bPoints){  
            var view = map.getViewport(eval(bPoints));  
            var mapZoom = view.zoom;   
            var centerPoint = view.center;   
            map.centerAndZoom(centerPoint,mapZoom);  
        }

        //创建地图
        var map = new BMap.Map("allmap");
        map.centerAndZoom(new BMap.Point(pointX, pointY), 19);  // 设置中心点
        // map.centerAndZoom(new BMap.Point(115.698399,37.7493), 11);
        // map.centerAndZoom( "衡阳");
        // map.setCurrentCity(city);          //默认为北京
        map.addControl(new BMap.MapTypeControl()); //可拖拽
        map.enableScrollWheelZoom(true);  //滚轮实现方法缩小
        </script>
        """
        with open(r"./map.html", "w", encoding="utf-8") as f:
            f.write(self.html)
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
        x = x * 0.00000899   # 经度转换米转换成gps坐标，误差很大
        y = y * 0.00001141   # 以北纬38度为基准
        jsFunction = "dynamicLine({0}, {1});".format(x, y)
        self.browser.page().runJavaScript(jsFunction)
        


class getCity(object):
    def __init__(self):
        self.MY_WEATHER_KEY = None
        self.url_now = None
        self.getUrl()

    def getUrl(self):
        config = ConfigParser()
        config.read("projectPath.ini", encoding='utf-8')

        self.url_now = r"https://free-api.heweather.net/s6/weather/now?location=auto_ip&" \
                       r"key={0}".format(config['mapconfig']["city_key"])

    def getLocal(self):
        try:
            self.log = get(self.url_now).json()
            now_APIcity = self.log['HeWeather6'][0]['basic']
            lat = now_APIcity['lat']
            lon = now_APIcity['lon']
        except (KeyError, exceptions.ConnectionError):
            lat = None
            lon = None
        return lon, lat





class baiduNotWeb(object):
    def __init__(self, mapView):
        self.browser = None
        self.mapView = mapView
        self.baiduBrowser()
        

    def baiduBrowser(self):
        self.browser = QWebEngineView(self.mapView)
        vv = QVBoxLayout()
        vv.setContentsMargins(0, 0, 0, 0)
        # 设置四周边界
        vv.addWidget(self.browser)
        self.mapView.setLayout(vv)
        # 指定打开界面的 URL
        url = r"file:///./404.html"
        self.browser.setUrl(QUrl(url))



class getCity(object):
    def __init__(self):
        self.MY_WEATHER_KEY = None
        self.url_now = None
        self.getUrl()

    def getUrl(self):
        config = ConfigParser()
        config.read("projectPath.ini", encoding='utf-8')

        self.url_now = r"https://free-api.heweather.net/s6/weather/now?location=auto_ip&" \
                       r"key={0}".format(config['mapconfig']["city_key"])

    def getLocal(self):
        try:
            self.log = get(self.url_now).json()
            now_APIcity = self.log['HeWeather6'][0]['basic']
            lat = now_APIcity['lat']
            lon = now_APIcity['lon']
        except (KeyError, exceptions.ConnectionError):
            lat = None
            lon = None
        return lon, lat






if __name__ == '__main__':
    new = getCity()
    loc = new.getLocal()
    print(loc)










