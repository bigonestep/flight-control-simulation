ledTuple = (
   'takeOffLed', 'landingLed', 'keepHeightLed', 
   'climb1Led', 'climb2Led', 'decline1Led',
   'decline2Led', 'turnLeftLed', 'turnRightLed',
   'keepDirectLed', 'stopLed'
)
ledInfo = (
    u"起飞", u"着陆", u"定高飞行", u"爬升1", u"爬升2", u"下滑1",
    u"下滑2", u"左转", u"右转", u"定向飞行", u"停止", u"等待"
)


    


class ledFunc(object):
    def __init__(self,ui_obj):
        self.ui_obj = ui_obj
        self.info = self.zipInfo()

    def zipInfo(self):
        return dict(zip(ledTuple, ledInfo))

    def ledState(self,led):
        for i in ledTuple:
            if i == led:
                self.ui_obj.LabAircraftInfo.setText(u"当前飞机状态:"+self.info[i])
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'on'
                obj.repaint()
            elif led == "allLed":
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()
            else:
                obj = getattr(self.ui_obj.ui, i)
                obj.state = 'off'
                obj.repaint()

    

    