
class buttonFunc(object):
    def __init__(self, ui_obj):
        self.ui_obj = ui_obj

    def takeOffButton(self):             
        print("takeOffButton is clicked")
        self.ui_obj.LabRightInfo.setText("起飞按钮按下")
        retu = self.ui_obj.sendOrder('takeOffLed')
        if retu == 0:
            print("指令发送成功！！！")

    def landingButton(self):
        print("landingButton is clicked")
        self.ui_obj.LabRightInfo.setText("着陆按钮按下")
        retu = self.ui_obj.sendOrder('landingLed')
        if retu == 0:
            print("指令发送成功！！！")
        
    def landingButto(self):
        print("landingButton is clicked")
        self.ui_obj.LabRightInfo.setText("着陆按钮按下")
        retu = self.ui_obj.sendOrder('landingLed')
        if retu == 0:
            print("指令发送成功！！！")

    def keepHeightButton(self):
        print("keepHeightButton is clicked")
        self.ui_obj.LabRightInfo.setText("定高飞行按钮按下")
        retu = self.ui_obj.sendOrder('keepHeightLed')
        if retu == 0:
            print("指令发送成功！！！")
    
    def climb1Button(self):
        print("climb1Button is clicked")
        self.ui_obj.LabRightInfo.setText("爬升1按钮按下")
        retu = self.ui_obj.sendOrder('climb1Led')
        if retu == 0:
            print("指令发送成功！！！")
    
    def climb2Button(self):
        print("climb2Button is clicked")
        self.ui_obj.LabRightInfo.setText("爬升2按钮按下")
        retu = self.ui_obj.sendOrder('climb2Led')
        if retu == 0:
            print("指令发送成功！！！")  

    def decline1Button(self):
        print("decline1Button is clicked")
        self.ui_obj.LabRightInfo.setText("下滑1按钮按下")
        retu = self.ui_obj.sendOrder('decline1Led')
        if retu == 0:
            print("指令发送成功！！！") 

    def decline2Button(self):
        print("decline2Button is clicked")
        self.ui_obj.LabRightInfo.setText("下滑2按钮按下")
        retu = self.ui_obj.sendOrder('decline2Led')
        if retu == 0:
            print("指令发送成功！！！")

    def turnLeftButton(self):
        print("turnLeftButton is clicked")
        self.ui_obj.LabRightInfo.setText("左转按钮按下")
        retu = self.ui_obj.sendOrder('turnLeftLed')
        if retu == 0:
            print("指令发送成功！！！")

    def turnRightButton(self):
        print("turnRightButton is clicked")
        self.ui_obj.LabRightInfo.setText("右转按钮按下")
        retu = self.ui_obj.sendOrder('turnRightLed')
        if retu == 0:
            print("指令发送成功！！！")

    def keepDirectButton(self):
        print("keepDirectButton is clicked")
        self.ui_obj.LabRightInfo.setText("定向飞行按钮按下")
        retu = self.ui_obj.sendOrder('keepDirectLed')
        if retu == 0:
            print("指令发送成功！！！")   



