from serial import Serial
from bge import logic

s = Serial('/dev/ttyUSB0', '57600', timeout=2)
#s.open()

intonaData = {}

def readIntona():
    data = s.readline()
    d = data.decode()
    ch = d.split(',')
    if len(ch) < 17: # we mayhave caught stream midway, let's wait for next line
        pass
    else:
        intonaData = {
            "roll": float(ch[1]),
            "pitch": float(ch[2]),
            "yaw": float(ch[3]),
            "accel_x": float(ch[5]),
            "accel_y": float(ch[6]),
            "accel_z": float(ch[7]),
            "gyro_x": float(ch[8]),
            "gyro_y": float(ch[9]),
            "gyro_z": float(ch[10]),
            "magnetom_x": float(ch[11]),
            "magnetom_y": float(ch[12]),
            "magnetom_z": float(ch[13]),
            "magnetom_heading": float(ch[14].split(' ')[0]),
            "piezd": float(ch[14].split(' ')[2]),
            "piezm": float(ch[15].split(' ')[1]),
            "ir": float(ch[16].rstrip('\r\n').split(' ')[1])
        }
        logic.globalDict['intonaData'] = intonaData
        jabDetect()

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
        

