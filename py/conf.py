''' 
* @Author: Wang.Zhihui  
* @Date: 2020-02-26 01:36:18  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-26 01:36:18  
* @function: 各种接口参数
'''
updateTime= 100   #单位毫秒，经测试100最佳，不需要再调
# note: 指令有预停，灯无预停。
# 指令无保持姿态，灯有保持姿态
## 飞行状态指示灯

ledFlight = {     # 正确
            'allLedOff':0, 'takeOffLed':1, 'landingLed':2,
            'climb1Led':3, 'decline1Led':4, 'climb2Led':5,
            'decline2Led':6, 'turnLeftLed':7, 'turnRightLed':8,
            'keepHeightLed':9,'keepDirectLed':10,  # 无11
            'stopLed': 11,'keepPostureLed': 13
         }
#  发动机的指示灯
ledEngine = {   # tag: 发动机状态没有预停，但是指示有预停
            'allLedOff':0,
            'bigCartLed' : 1 ,'ratedLed':2, 'cruiseLed':3, 
            'slowTrainLed':4, 'idlingLed':5, 'parkingLed':6

         }   
# 模式指示灯
ledModel = {    # note: 和指令顺序不一样
            'allLedOff': 0,
            'programeControlModelLed':1,"remoteControlModelLed":2, "internalControlModelLed":3
            } 
## 指令   正确
orderDict = {          
            'noOrder':0,
            # 模式 
            'remoteControlModel': 1, 'programeControlModel': 2, 'internalControlModel': 3,
            # 飞行状态
            'takeOff':4, 'landing': 5,'climb1': 6, 'climb2': 7, 'decline1': 8, 
            'decline2':9, 'keepHeight': 10, 'turnLeft':11, 'turnRight': 12, 
            'keepDirect': 13,
            # 发动机状态
            'bigCart': 14,'rated': 15,'cruise': 16,'slowTrain': 17,
            'idling': 18, 'preStop': 19, 'parking': 20
            } 
## 文本数据显示框
orderInfo = (
            u"无指令",
            u"遥控",u"程控",u"内控",
            u"起飞", u"着陆",u"爬升1", u"爬升2", u"下滑1", 
            u"下滑2", u"定高平行", u"左转", u"右转", u"定向飞行", 
            u"大车", u"额定", u"巡航", u"慢车", u"怠速", u"预停", u"停车"
   )

edit = ('XEdit', 'YEdit', 'HEdit', 'alphaEdit', 'betaEdit', 
        'VtEdit', 'phiEdit', 'thetaEdit', 'psiEdit', 
        'pEdit', 'qEdit', 'rEdit')
# 接收数据
data = {
    'X':0, 'Y':1, 'H':2, 'alpha':3, 'beta':4, 'Vt':5,
    'phi':6, 'theta':7, 'psi':8, 'p':9, 'q':10, 'r':11,
    # 'acceptState':13, 'programeControlState':14, 'send': 15
    'acceptModel':13, 'acceptEngineStatus':14, 'acceptFlightStatus': 15,
    'send':16
}