import os
import sys

from bge import logic

CURDIR = logic.expandPath('//')
SCRIPTS_PATH = os.path.join(CURDIR, 'scripts')
sys.path.append(SCRIPTS_PATH)

import oscinterface as OSC
from serial import Serial

s = None
oscinterface = OSC.OSCinterface(logic)
try:
    s = Serial('/dev/ttyUSB0', '57600', timeout=0)
except:
    pass
#s.open()

intonaData = {}
logic.globalDict['intonaData'] = intonaData

def readIntona():
    if not s is None:
        data = s.readline()
        d = data.decode()
        print("**********>>>>>>>", d)
        ch = d.split(',')
        print("rpy: {} {} {}".format(ch[1], ch[2], ch[3]))
        intonaData = {
            "roll": makeFloat(ch[1]),
            "pitch": makeFloat(ch[2]),
            "yaw": makeFloat(ch[3]),
            "ir": makeFloat(ch[16].rstrip('\r\n').split(' ')[1])
        }
        # if len(ch) < 17: # we mayhave caught stream midway, let's wait for next line
        #     return
        # else:
        #     intonaData = {
        #         "roll": makeFloat(ch[1]),
        #         "pitch": makeFloat(ch[2]),
        #         "yaw": makeFloat(ch[3]),
        #         "accel_x": makeFloat(ch[5]),
        #         "accel_y": makeFloat(ch[6]),
        #         "accel_z": makeFloat(ch[7]),
        #         "gyro_x": makeFloat(ch[8]),
        #         "gyro_y": makeFloat(ch[9]),
        #         "gyro_z": makeFloat(ch[10]),
        #         "magnetom_x": makeFloat(ch[11]),
        #         "magnetom_y": makeFloat(ch[12]),
        #         "magnetom_z": makeFloat(ch[13]),
        #         "magnetom_heading": makeFloat(ch[14].split(' ')[0]),
        #         "piezd": makeFloat(ch[14].split(' ')[2]),
        #         "piezm": makeFloat(ch[15].split(' ')[1]),
        #         "ir": makeFloat(ch[16].rstrip('\r\n').split(' ')[1])
        #     }
        logic.globalDict['intonaData'] = intonaData
        print("intondata: {}".format(intonaData))
    else:
        oscinterface.recv(0)
    #print("************", logic.globalDict['intonaData'])
    #jabDetect()
    
def showType(x):
    print(" ---------> value: ", x, type(x), len(x))

def makeFloat(x):
    showType(x)
    try:
        return float(x)
    except:
        print(" ----- > bad value", x, type(x), len(x))
        newx = x.rstrip("\0x00")
        print(" +++ stripped to ", newx, type(newx), len(newx))
        newx = newx.split(' ')
        print(" +++ and split ", newx, type(newx), len(newx))
        return float(newx)

def jabDetect():
    """
    Detect a wide and fast movement in any direction
    """
    intonaData = logic.globalDict['intonaData']
    accelSum = abs(intonaData['accel_x']) + abs(intonaData['accel_y']) + abs(intonaData['accel_z'])
    if accelSum > 500:
        logic.globalDict['intonaData']["jab"] = True
    else:
        logic.globalDict['intonaData']["jab"] = False
        
