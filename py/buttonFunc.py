# -*- coding: utf-8 -*-
"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-25 14:37:49  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-25 14:37:49  
* @function: 按键的逻辑功能
"""

import os
import time  
from mySetParameters import QsetParameters


ModelTuple = ('no', 'programeControlModelLed', "remoteControlModelLed",
              "internalControlModelLed")
ModelInfo = (u"无模式信息", u"程控", u"遥控", u"内控")

EngineTuple = ('no', 'bigCartLed', 'ratedLed', 'cruiseLed', 'slowTrainLed',
               'idlingLed', 'parkingLed')
EngineInfo = (u"无发动机状态", u"大车", u"额定", u"巡航", u"慢车", u"怠速", u"停车")

FlightTuple = ('no',
               'takeOffLed', 'landingLed', 'climb1Led',
               'decline1Led', 'climb2Led', 'decline2Led',
               'turnLeftLed', 'turnRightLed', 'keepHeightLed',
               'keepDirectLed', 'stopLed', 'keepPostureLed')

FlightInfo = (u"无飞行状态",
              u"起飞", u"着陆", u"爬升1", u"下滑1", u"爬升2",
              u"下滑2", u"左转", u"右转", u"定高平行", u"定向飞行", u"停止",
              u"姿态保持")

data = {
        'X': 0, 'Y': 1, 'H': 2, 'alpha': 3, 'beta': 4, 'Vt': 5,
        'phi': 6, 'theta': 7, 'psi': 8, 'p': 9, 'q': 10, 'r': 11}

dataInfo = (u"距离", u"侧位", u"高度", u"迎角",
            u"侧滑角", u"空速", u"滚转角", u"俯仰角",
            u"偏航角", u"滚转角速率", u"俯仰角速率", u"偏航角速率")


class buttonFunc(object):

    @staticmethod
    def takeOffButton(ui_obj):             
        print("takeOffButton is clicked")
        ui_obj.LabRightInfo.setText(u"起飞按钮按下")
        retu = ui_obj.sendOrder('takeOff')
        if retu == 0: 
            
            print("指令发送成功！！！")
    @staticmethod
    def landingButton(ui_obj):
        print("landingButton is clicked")
        ui_obj.LabRightInfo.setText(u"着陆按钮按下")
        retu = ui_obj.sendOrder('landing')
        if retu == 0: 
            
            print("指令发送成功！！！")

    @staticmethod
    def keepHeightButton(ui_obj):
        print("keepHeightButton is clicked")
        ui_obj.LabRightInfo.setText(u"定高飞行按钮按下")
        retu = ui_obj.sendOrder('keepHeight')
        if retu == 0: 
            
            print("指令发送成功！！！")
    
    @staticmethod
    def climb1Button(ui_obj):
        print("climb1Button is clicked")
        ui_obj.LabRightInfo.setText(u"爬升1按钮按下")
        retu = ui_obj.sendOrder('climb1')
        if retu == 0:
            
            print("指令发送成功！！！")
    @staticmethod
    def climb2Button(ui_obj):
        print("climb2Button is clicked")
        ui_obj.LabRightInfo.setText(u"爬升2按钮按下")
        retu = ui_obj.sendOrder('climb2')
        if retu == 0:
            
            print("指令发送成功！！！")  

    @staticmethod
    def decline1Button(ui_obj):
        print("decline1Button is clicked")
        ui_obj.LabRightInfo.setText(u"下滑1按钮按下")
        retu = ui_obj.sendOrder('decline1')
        if retu == 0:
            
            print("指令发送成功！！！") 

    @staticmethod
    def decline2Button(ui_obj):
        print("decline2Button is clicked")
        ui_obj.LabRightInfo.setText(u"下滑2按钮按下")
        retu = ui_obj.sendOrder('decline2')
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod
    def turnLeftButton(ui_obj):
        print("turnLeftButton is clicked")
        ui_obj.LabRightInfo.setText(u"左转按钮按下")
        retu = ui_obj.sendOrder('turnLeft')
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod   
    def turnRightButton(ui_obj):
        print("turnRightButton is clicked")
        ui_obj.LabRightInfo.setText(u"右转按钮按下")
        retu = ui_obj.sendOrder('turnRight')
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod
    def keepDirectButton(ui_obj):
        print("keepDirectButton is clicked")
        ui_obj.LabRightInfo.setText(u"定向飞行按钮按下")
        retu = ui_obj.sendOrder('keepDirect')
        if retu == 0:
            
            print("指令发送成功！！！") 

    @staticmethod  #
    def programeControlModelButton(ui_obj):
        print("programeControlButton is clicked")
        ui_obj.LabRightInfo.setText(u"程控飞行按钮按下")
        retu = ui_obj.sendOrder("programeControlModel")
        if retu == 0:
            
            print("指令发送成功！！！")
    
    @staticmethod
    def remoteControlModelButton(ui_obj):
        print("remoteControlModelButton is clicked")
        ui_obj.LabRightInfo.setText(u"遥控飞行按钮按下")
        retu = ui_obj.sendOrder("remoteControlModel")
        if retu == 0:
            
            print("指令发送成功！！！")
    
    @staticmethod
    def internalControlModelButton(ui_obj):
        print("internalControlModelButton is clicked")
        ui_obj.LabRightInfo.setText(u"内控飞行按钮按下")
        retu = ui_obj.sendOrder("internalControlModel")
        if retu == 0:
            
            print("指令发送成功！！！")

    # 发动机
    @staticmethod
    def bigCartButton(ui_obj):
        print("bigCartButton is clicked")
        ui_obj.LabRightInfo.setText(u"大车按钮按下")
        retu = ui_obj.sendOrder("bigCart")
        if retu == 0:
            
            print("指令发送成功！！！")
    @staticmethod
    def ratedButton(ui_obj):
        print("ratedButton is clicked")
        ui_obj.LabRightInfo.setText("额定按钮按下")
        retu = ui_obj.sendOrder("rated")
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod
    def cruiseButton(ui_obj):
        print("cruiseButton is clicked")
        ui_obj.LabRightInfo.setText(u"巡航按钮按下")
        retu = ui_obj.sendOrder("cruise")
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod
    def slowTrainButton(ui_obj):
        print("slowTrainButton is clicked")
        ui_obj.LabRightInfo.setText(u"慢车按钮按下")
        retu = ui_obj.sendOrder("slowTrain")
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod
    def idlingButton(ui_obj):
        print("idlingButton is clicked")
        ui_obj.LabRightInfo.setText(u"怠速按钮按下")
        retu = ui_obj.sendOrder("idling")
        if retu == 0: 
            
            print("指令发送成功！！！")

    @staticmethod
    def preStopButton(ui_obj):
        print("preStopButton is clicked")
        ui_obj.LabRightInfo.setText(u"预停按钮按下")
        retu = ui_obj.sendOrder("preStop")
        if retu == 0:
            print("指令发送成功！！！")

    @staticmethod
    def parkingButton(ui_obj):
        print("parkingButton is clicked")
        ui_obj.LabRightInfo.setText(u"停车按钮按下")
        retu = ui_obj.sendOrder("parking")
        if retu == 0:
            
            print("指令发送成功！！！")

    @staticmethod
    def saveFigButton(ui_obj):
        new = time.strftime("%m_%d_%H_%M_%S", time.localtime())
        filePath = "./curaeFile/"+new+"/"
        if not os.path.isdir(filePath):
            os.makedirs(filePath)
        ui_obj.ui.heightView.fig.savefig("./curaeFile/"+new+"/"+"Height.png")
        ui_obj.ui.thetaView.fig.savefig("./curaeFile/" + new + "/" + "theta.png")
        ui_obj.ui.phiView.fig.savefig("./curaeFile/" + new + "/" + "phi.png")
        ui_obj.ui.psiView.fig.savefig("./curaeFile/" + new + "/" + "psi.png")
        ui_obj.ui.threeDView.figure.savefig("./curaeFile/" + new + "/" + "threeDimensional.png")
        ui_obj.LabRightInfo.setText(u"保存图像成功")

    @staticmethod
    def saveConfButton(ui_obj, t):
        print("saveConfButton")
        new = time.strftime("%m_%d_%H_%M_%S", time.localtime())
        filePath = "./curaeFile/"
        if not os.path.isdir(filePath):
            os.makedirs(filePath)
        textPath = filePath + new+"AircraftParameters"+".txt"
        tt = "{:<}".format("飞行持续时间为"+":"+t+"\n")
        model = "{:<}".format("飞机飞行模式为")+":" + ModelInfo[ui_obj.ledModelState] + "\n"
        fight = "{:<}".format("飞机飞行状态为")+":"+FlightInfo[ui_obj.ledFlightState] + "\n"
        engine = "{:<}".format("飞机发动机状态为")+":"+EngineInfo[ui_obj.ledEngineState] + "\n"

        with open(textPath, 'w') as f:
            f.write(tt)
            f.write(model)
            f.write(fight)
            f.write(engine)
            f.write("\n")
            f.write(r"飞机状态各项参数为："+"\n")
            for i in data:
                f.write("{:<4}".format('')+"{:<}".format(dataInfo[data[i]]) +
                        "{:<}".format(i) + ":" + 
                        "{:.2f}".format(ui_obj.para[data[i]]) + "\n")
        ui_obj.LabRightInfo.setText(u"保存数据成功")
    


        