import math
from bge import logic
from random import random

cont = logic.getCurrentController()
scene = logic.getCurrentScene()

previousData = {}
amplitudes = {}

squares = []

def getIntonaData():
    return logic.globalDict['intonaData']
    
def rotateHoverBoard():
    intonaData = getIntonaData()
    hoverBoard = scene.objects['hoverBoard']
    accelx = scene.objects["accelx"]
    accely = scene.objects["accely"]
    accelz = scene.objects["accelz"]
    floor = scene.objects["Floor"]
    #print("Roll: {0}, Pitch: {1}, Yaw: {2}".format(intonaData['roll'], intonaData['pitch'], intonaData['yaw']))
    hoverBoard.worldOrientation = [math.radians(intonaData['roll']), math.radians(intonaData['pitch']), math.radians(intonaData['yaw'])]
    ax = accelx.worldScale
    #ay = accely.worldScale
    #az = accelz.worldScale
    #accelx.worldScale = [(ax[0]+intonaData['accel_x'])*0.01, ax[1], ax[2]]
    #accely.worldScale = [(ay[0]+intonaData['accel_y'])*0.01, ay[1], ay[2]]
    #accelz.worldScale = [(az[0]+intonaData['accel_z'])*0.01, az[1], az[2]]
    #floor.worldOrientation = [math.radians(intonaData['magnetom_x']), math.radians(intonaData['magnetom_y']), math.radians(intonaData['magnetom_z'])]
    #accelx.worldOrientation = [math.radians(intonaData['accel_x']), math.radians(intonaData['accel_y']), -math.radians(intonaData['accel_z'])]
        
def getAmplitudes():
    global previousData, amplitudes
    currentData = getIntonaData()
    amplitudes = currentData
    if len(previousData) < 1:
        previousData = getIntonaData()
    for i in previousData:
        amplitudes[i] = currentData[i] - previousData[i]
    previousData = currentData
    return amplitudes
    
def createSquare():
    #global squares
    intonaData = getIntonaData()
    if intonaData['jab']:
        sq = scene.addObject("CubePartHandle", "hoverBoard")
        sq.worldPosition = [(random()*10)-5, (random()*10)-5, random()*4]
        squares.append(sq)
        

