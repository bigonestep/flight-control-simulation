# -*- coding: utf-8 -*-
''' 
* @Author: Wang.Zhihui  
* @Date: 2020-02-25 14:36:24  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-25 14:36:24  
* @function: 指示灯的控制
'''

ledFlightTuple = (
   'takeOffLed', 'landingLed', 'climb1Led', 
   'decline1Led', 'climb2Led', 'decline2Led',
   'turnLeftLed', 'turnRightLed', 'keepHeightLed',
   'keepDirectLed', 'stopLed','keepPostureLed'
)
ledFlightInfo = (
    u"起飞", u"着陆", u"爬升1", u"下滑1", u"爬升2",
    u"下滑2", u"左转", u"右转", u"定高平行", u"定向飞行", u"停止",
    u"姿态保持"
)
class ledFlightFunc(object):
    def __init__(self,ui_obj):
        self.ui_obj = ui_obj
        self.info = self.zipInfo()

    def zipInfo(self):
        return dict(zip(ledFlightTuple, ledFlightInfo))

    def ledFlight(self,led):
        for i in ledFlightTuple:
            if i == led:
                self.ui_obj.LabAircraftInfo.setText(u"当前飞机状态:"+self.info[i])
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'on'
                obj.repaint()
            elif led == "allLedOff":
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()
            else:
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()

# 发动机灯控制    灯有预停
ledEngineTuple = ('bigCartLed' ,'ratedLed', 'cruiseLed', 'slowTrainLed', 
                  'idlingLed', 'parkingLed')
ledEngineInfo = (u'大车', u'额定', u'巡航', u'慢车', u'怠速', u'停车')
class ledEngineFunc(object):    # TODO:   添加发动机灯   
    def __init__(self,ui_obj):
        self.ui_obj = ui_obj 
        self.info = self.zipInfo()

    def zipInfo(self):
        return dict(zip(ledEngineTuple, ledEngineInfo))  

   # 发动机灯互斥
    def ledEngine(self, led):
        for i in ledEngineTuple:
            if i == led:
                print(u"当前发动机状态:"+self.info[i])
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'on'
                obj.repaint()
            elif led == "allLedOff":
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()
            else:
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()

# 模式灯控制
ledModelTuple =('programeControlModelLed', "remoteControlModelLed",
                 "internalControlModelLed")
ledModelInfo = (u'程控', u'遥控', u'内控')
class ledModelFunc(object):         # TODO: 添加模式灯
    def __init__(self,ui_obj):
        self.ui_obj = ui_obj   
        self.info = self.zipInfo()

    def zipInfo(self):
        return dict(zip(ledModelTuple, ledModelInfo))  
    # 发动机灯互斥
    def ledModel(self, led):
        for i in ledModelTuple:
            if i == led:
                print(u"当前控制模式为:"+self.info[i])
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'on'
                obj.repaint()
            elif led == "allLedOff":
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()
            else:
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()
    


    

    