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

camera = 0

controls = []

def toggleCam():
    global camera, scene
    if isSensorPositive():
        camera = not camera
        if camera:
            scene.active_camera = "CamOrtho"
        else:
            scene.active_camera = "CamPers"

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
    # accelx = intonaData['accel_x'] * 0.1
    # accely = intonaData['accel_y'] * 0.1
    # accelz = intonaData['accel_z'] * 0.1
    # if isSensorPositive():
    #     if intonaData['jab']:
    #         print("jab", [accelx, accely, accelz])
    #         force.worldLinearVelocity = [accelx, accely, accelz]
    if isSensorPositive():
        force.worldOrientation =  [
            math.radians(intonaData['roll']), 
            math.radians(intonaData['pitch']), 
            math.radians(intonaData['yaw'])
        ]

def randomForceMove():
    family = []
    updateContext()
    if isSensorPositive():
        # force = scene.objects['Forceer']
        # force.worldLinearVelocity = [(random()*1000) - 500, (random()*1000) - 500, (random()*1000) - 500]
        if len(controls) > 0:
            for c in controls:
                c.removeParent()
                c.isDynamic = False
            for c in controls:
                if 'Pipe' in c.group:
                    family.append(c)
            choices = randint(0, len(family))
            # for i in range(choices):
            #     control = randint(0, choices) 
            #     family[control].setParent("Forceer")
            #     family[control].isDynamic = True
            for f in family:
                f.setParent("Forceer")
                f.isDynamic = True

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
        sq.worldPosition = [(random() * 100) - 50, (random() * 100) + 20 , (random() * 0.01) - 1]
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
    #print("PipeLvalve poining at {} {}".format(pointingAt, screenPosition))

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
            controls.append(med)

def createAll():
    global valves
    name = None
    control = None
    oscurl = None
    ctrl = None
    color = None
    instrGroup = None
    if isSensorPositive():
        updateContext()
        for name, group in config.groups.items():
            instrGroup = name
            print("*****************", group)
            for instrument in group['instruments']:
                name = instrument
                for control in group['controls']:
                    control = control
                    oscurl = os.path.join("/", name, control)
                    print(oscurl)
                    if "valve" in control:
                        print("creating valve ", control)
                        ctrl = "valveController"
                        color = colors[0]
                    elif "speed" in control:
                        print("creating speed ", control)
                        ctrl = "speedController"
                        color = colors[1]
                    else:
                        print("creating controller ", control)
                        ctrl = "otherController"
                        color = colors[2]
                    med = Mediator(scene.addObject(ctrl, "Floor"))
                    med.oscurl = oscurl
                    med.id = name
                    med.control = control
                    med.group = instrGroup
                    med.stopDynamics()
                    # med.worldPosition = [(random() * 10) -5, (random() * 5) + 5, 1]
                    med.worldPosition.x = (random() * 20) -10
                    med.worldPosition.y = (random() * 20) -10
                    stackInstruments(med)
                    med.localScale = [0.6, 0.6, 0.3 + (random())]
                    med.color = color
                    controls.append(med)
                    
def stackInstruments(instrument):
    if "Pipe" in instrument.id:
        print("Found pipe!")
        instrument.worldPosition.z = 1
    elif "/" in instrument.id:
        print("Found Tele!")
        instrument.worldPosition.z = 2.5
    else:
        print("Found choir!")
        instrument.worldPosition.z = 3.5
            
        
def playRandomAction():
    chance = randint(0, len(controls))
    picked = controls[chance]
    if not picked.isPlayingAction():
        picked.playAction("PipeLvalveH", randint(0,100), randint(150, 250), speed=(random()*10))

def updatePositions():
    global valves
    if len(controls) > 0:
        for mediator in controls:
            mediator.sendPosition()
    # if len(controls) > 0:
    #     for i in controls:
    #         distance = i.getDistanceTo(scene.objects['Forceer'])
    #         if distance  < 3:
    #             print("{} is at {} from Forceer".format(i, distance))
    #             i.startDynamics()
    #         else:
    #             i.stopDynamics()
