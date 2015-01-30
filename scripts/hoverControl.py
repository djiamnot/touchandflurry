import math
import os
import sys

from bge import logic
from mathutils import Color
from mathutils import Vector
from random import random
from random import randint

CURDIR = logic.expandPath('//')
SCRIPTS_PATH = os.path.join(CURDIR, 'scripts')
sys.path.append(SCRIPTS_PATH)

#print(os.path.join(logic.expandPath('//'), 'scripts'))
import config
from mediator import Mediator

cont = logic.getCurrentController()
scene = logic.getCurrentScene()

ALPHA = 1.0

colors = [
    [0.443, 0.616, 0.635, ALPHA],
    [1.0, 0.949, 0.694, ALPHA],
    [0.71, 0.302, 0.325, ALPHA],
    [0.533, 0.463, 0.11, ALPHA],
]
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

def intonaForce():
    intonaData = getIntonaData()
    force = scene.objects['Forceer']
    accelx = intonaData['accel_x'] * 0.1
    accely = intonaData['accel_y'] * 0.1
    accelz = intonaData['accel_z'] * 0.1
    if isSensorPositive():
        if intonaData['jab']:
            print("jab", [accelx, accely, accelz])
            force.worldLinearVelocity = [accelx, accely, accelz]

def randomForceMove():
    updateContext()
    if isSensorPositive():
        force = scene.objects['Forceer']
        force.worldLinearVelocity = [(random()*1000) - 500, (random()*1000) - 500, (random()*1000)]
        
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
    if isSensorPositive():
        if intonaData['jab']:
            sq = scene.addObject("CubePartHandle", "hoverBoard")
            accelx = intonaData['accel_x']*0.01
            accely = intonaData['accel_y']*0.01
            accelz = intonaData['accel_z']* 0.01
            sq.children[0].localPosition = [ accelx, accely, accelz]
            sq.localAngularVelocity = [accelx, accely, accelz]
            sq.worldPosition = [ accelx, accely, accelz]
            squares.append(sq)

def createSquares():
    dummy = scene.objects["Plane.001"]
    # dummy.playAction("PipeLvalveH", 0 , 250)
    for i in range(100):
        sq = sq = scene.addObject("CubePart", "hoverBoard")
        sq.worldPosition = [(random() * 100) - 50, (random() * 100) + 50 , (random() * 0.01) - 3]
        sq.worldScale = [(random() * 10), (random() * 10) , (random() * 10)]
        sq.color = colors[randint(0,3)]

def hoverBoardRay():
    updateContext()
    # ray = cont.sensors["Ray"]
    # pointingAt = ray.hitObject
    # hitpos = ray.hitPosition
    # hitVector = Vector(hitpos)
    # screenPosition = pointingAt.worldTransform
    # screenInverted = screenPosition.inverted()
    # screenPosition = screenInverted * hitVector
    # print("hover poining at {} {}".format(pointingAt, screenPosition))
    # if ray.hitObject is not None:
    #     pointingAt = ray.hitObject
    #     print("hit: {} at {}".format(pointingAt, ray.hitPosition))
    #     hitVector = Vector(ray.hitPosition)
    #     screenPosition = pointingAt.worldTransform
    #     screenInverted = screenPosition.inverted()
    #     screenPosition = screenInverted * hitVector
    #     print(screenPosition)
    # else:
    #     pointingAt= None
    PipeRay = cont.sensors["PipeLValve"]
    pointingAt = PipeRay.hitObject
    hitpos = PipeRay.hitPosition
    hitVector = Vector(hitpos)
    screenPosition = pointingAt.worldTransform
    screenInverted = screenPosition.inverted()
    screenPosition = screenInverted * hitVector
    print("PipeLvalve poining at {} {}".format(pointingAt, screenPosition))

def updateContext():
    global cont, obj, scene
    cont = logic.getCurrentController()
    obj = cont.owner
    scene = logic.getCurrentScene()  

def isSensorPositive():
    from bge import logic
    cont = logic.getCurrentController()
    for sensor in cont.sensors:
        if sensor.positive:
            return True
    return False

valves = []

def createMediator():
    if isSensorPositive():
        updateContext()
        for valve in config.valves:
            print(" ** Creating ", valve)
            med = Mediator(scene.addObject("valveController", "Floor"))
            med.oscurl = valve
            med.suspendDynamics()
            # med.worldPosition = [(random() * 10) -5, (random() * 5) + 5, 1]
            med.worldPosition.x = (random() * 20) -10
            med.worldPosition.y = (random() * 20) -10
            med.localScale = [0.7, 0.7, 0.7 + (random() * 3)]
            valves.append(med)

def playRandomAction():
    chance = randint(0, len(valves))
    picked = valves[chance]
    if not picked.isPlayingAction():
        picked.playAction("PipeLvalveH", randint(0,100), randint(150, 250), speed=(random()*10))

def updatePositions():
    global valves
    for mediator in valves:
        mediator.sendPosition()
