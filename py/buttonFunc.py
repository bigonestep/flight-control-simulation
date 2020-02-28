# -*- coding: utf-8 -*-
''' 
* @Author: Wang.Zhihui  
* @Date: 2020-02-25 14:37:49  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-25 14:37:49  
* @function: 按键的逻辑功能
'''

import os
import time
class buttonFunc(object):

# TODO: # print 全部被注释了

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
        new = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        filePath = "./curaeFile/"+new+"/"
        if not os.path.isdir(filePath):
            os.makedirs(filePath)
        ui_obj.ui.heightView.fig.savefig("./curaeFile/"+new+"/"+"Height.png")
        ui_obj.ui.thetaView.fig.savefig("./curaeFile/" + new + "/" + "theta.png")
        ui_obj.ui.phiView.fig.savefig("./curaeFile/" + new + "/" + "phi.png")
        ui_obj.ui.psiView.fig.savefig("./curaeFile/" + new + "/" + "psi.png")
        ui_obj.ui.threeDView.figure.savefig("./curaeFile/" + new + "/" + "threeDimensional.png")
        ui_obj.LabRightInfo.setText(u"保存图像成功！！！")



