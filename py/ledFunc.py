ledTuple = (
   'takeOffLed',
   'landingLed',
   'keepHeightLed',
   'climb1Led',
   'climb2Led',
   'decline1Led',
   'decline2Led',
   'turnLeftLed',
   'turnRightLed',
   'keepDirectLed',
   'stopLed'
)

class ledFunc(object):
    def __init__(self,ui_obj):
        self.ui_obj = ui_obj

    def takeOffLed(self,led):
        for i in ledTuple:
            if i == led:
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
            
    