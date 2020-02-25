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


    @staticmethod
    def takeOffButton(ui_obj):             
        print("takeOffButton is clicked")
        ui_obj.LabRightInfo.setText("起飞按钮按下")
        retu = ui_obj.sendOrder('takeOff')
        if retu == 0:
            print("指令发送成功！！！")
    @staticmethod
    def landingButton(ui_obj):
        print("landingButton is clicked")
        ui_obj.LabRightInfo.setText("着陆按钮按下")
        retu = ui_obj.sendOrder('landing')
        if retu == 0:
            print("指令发送成功！！！")

    @staticmethod
    def keepHeightButton(ui_obj):
        print("keepHeightButton is clicked")
        ui_obj.LabRightInfo.setText("定高飞行按钮按下")
        retu = ui_obj.sendOrder('keepHeight')
        if retu == 0:
            print("指令发送成功！！！")
    
    @staticmethod
    def climb1Button(ui_obj):
        print("climb1Button is clicked")
        ui_obj.LabRightInfo.setText("爬升1按钮按下")
        retu = ui_obj.sendOrder('climb1')
        if retu == 0:
            print("指令发送成功！！！")
    @staticmethod
    def climb2Button(ui_obj):
        print("climb2Button is clicked")
        ui_obj.LabRightInfo.setText("爬升2按钮按下")
        retu = ui_obj.sendOrder('climb2')
        if retu == 0:
            print("指令发送成功！！！")  

    @staticmethod
    def decline1Button(ui_obj):
        print("decline1Button is clicked")
        ui_obj.LabRightInfo.setText("下滑1按钮按下")
        retu = ui_obj.sendOrder('decline1')
        if retu == 0:
            print("指令发送成功！！！") 

    @staticmethod
    def decline2Button(ui_obj):
        print("decline2Button is clicked")
        ui_obj.LabRightInfo.setText("下滑2按钮按下")
        retu = ui_obj.sendOrder('decline2')
        if retu == 0:
            print("指令发送成功！！！")

    @staticmethod
    def turnLeftButton(ui_obj):
        print("turnLeftButton is clicked")
        ui_obj.LabRightInfo.setText("左转按钮按下")
        retu = ui_obj.sendOrder('turnLeft')
        if retu == 0:
            print("指令发送成功！！！")

    @staticmethod   
    def turnRightButton(ui_obj):
        print("turnRightButton is clicked")
        ui_obj.LabRightInfo.setText("右转按钮按下")
        retu = ui_obj.sendOrder('turnRight')
        if retu == 0:
            print("指令发送成功！！！")

    @staticmethod
    def keepDirectButton(ui_obj):
        print("keepDirectButton is clicked")
        ui_obj.LabRightInfo.setText("定向飞行按钮按下")
        retu = ui_obj.sendOrder('keepDirect')
        if retu == 0:
            print("指令发送成功！！！") 

    @staticmethod  #
    def programeControlModelButton(ui_obj):
        print("programeControl_clicked:")
        ui_obj.LabRightInfo.setText("程控飞行按钮按下")
        ui_obj.setProgrameControlOrder()

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
        ui_obj.LabRightInfo.setText("保存图像成功！！！")



