import math
import os
import sys

from bge import logic
from bge import events
from mathutils import Color
from mathutils import Vector
from random import random
from random import randint
KEYBOARD = logic.keyboard
ACTIVE = logic.KX_SENSOR_ACTIVE    

CURDIR = logic.expandPath('//')
SCRIPTS_PATH = os.path.join(CURDIR, 'scripts')
sys.path.append(SCRIPTS_PATH)

#print(os.path.join(logic.expandPath('//'), 'scripts'))
import config
import context
from mediator import Mediator
from control import Control
import utils


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
currentySelected = []

pipes = []
telescopics = []
choirs = []

ctl = Control(controls)

def keyboardCtrl():
    bindings = {
        'boo': events.BKEY,
        'doo': events.DKEY,
        'pvalves': events.FKEY,
        'cvalves': events.GKEY,
        'tvalves': events.HKEY,
        'pmotors': events.RKEY,
        'gpositions': events.OKEY,
        'addpipes': events.PKEY,
        'addteles': events.TKEY,
        'addchoirs': events.YKEY,
        'origins': events.QKEY,
    }
    mapping = {
        'boo': removeAllParents, 
        'doo': silenceAll,
        'pvalves': addPipeValves,
        'cvalves': addChoirValves,
        'tvalves': addTeleValves,
        'pmotors': addPipeMotors,
        'gpositions': getPositions,
        'addpipes': addPipes,
        'addteles': addTelescopics,
        'addchoirs': addChoirs,
        'origins': returnAllToOrigin,
        
    }
    activeKey = KEYBOARD.active_events
    print(activeKey)
    for k in activeKey:
        key_id = k
        state = activeKey[k]
    if state == 1:
        for k in bindings:
            for key_id in activeKey:
                if bindings[k] == key_id:
                    function = mapping[k]
                    function()

def toggleCam():

    global camera, scene
    if context.isSensorPositive():
        camera = not camera
        if camera:
            context.scene.active_camera = "CamOrtho"
        else:
            context.scene.active_camera = "CamPers"

    
def rotateHoverBoard():
    intonaData = ctl.getIntonaData()
    hoverBoard = context.scene.objects['hoverBoard']
    accelx = context.scene.objects["accelx"]
    accely = context.scene.objects["accely"]
    accelz = context.scene.objects["accelz"]
    floor = context.scene.objects["Floor"]
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
    intonaData = ctl.getIntonaData()
    force = context.scene.objects['Forceer']
    # accelx = intonaData['accel_x'] * 0.1
    # accely = intonaData['accel_y'] * 0.1
    # accelz = intonaData['accel_z'] * 0.1
    # if isSensorPositive():
    #     if intonaData['jab']:
    #         print("jab", [accelx, accely, accelz])
    #         force.worldLinearVelocity = [accelx, accely, accelz]
    if context.isSensorPositive():
        force.worldOrientation =  [
            math.radians(intonaData['roll']), 
            math.radians(intonaData['pitch']), 
            math.radians(intonaData['yaw'])
        ]

def removeAllParents():
    for collection in [pipes, choirs, telescopics]:
        if len(collection) > 0:
            ctl.removeParents(collection)

def silenceAll():
    for collection in [pipes, choirs, telescopics]:
        if len(collection) > 0:
            ctl.silence(collection)


def addPipes():
    global pipes
    print ("adding pipes")
    populateControls("Pipe", pipes)
    print("================ ", pipes)

def addTelescopics():
    global telescopics
    print ("adding telescopics")
    populateControls("Tele", telescopics)
    print("================ ", telescopics)

def addChoirs():
    global choirs
    print ("adding choirs")
    populateControls("Choir", choirs)
    print("================ ", choirs)


def populateControls(family, array):
    name = None
    control = None
    oscurl = None
    ctrl = None
    color = None
    instrGroup = None
    controls = array
    if context.isSensorPositive():
        context.updateContext()
        for name, group in config.groups.items():
            if family in name:
                instrGroup = name
                for instrument in group["instruments"]:
                    name = instrument
                    print("--> instrument", instrument)
                    for control in group["controls"]:
                        print("  --> control: ", control)
                        control = control
                        oscurl = os.path.join("/", name, control)
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
                        med = Mediator(context.scene.addObject(ctrl, name))
                        med.oscurl = oscurl
                        med.id = name
                        med.control = control
                        med.group = instrGroup
                        med.stopDynamics()
                        # med.worldPosition = [(random() * 10) -5, (random() * 5) + 5, 1]
                        #med.worldPosition.x = (random() * 20) -10
                        #med.worldPosition.y = (random() * 20) -10
                        stackInstruments(med)
                        med.localScale = [0.5, 0.5, 0.5 + (random())]
                        med.color = color
                        med.setStartingPosition(med.localPosition)
                        controls.append(med)

def returnAllToOrigin():
    for collection in [pipes, choirs, telescopics]:
        if len(collection) > 0:
            vCtl = Control(collection)
            vCtl.returnToOrigin()
                
def getPositions():
    print([(c.oscurl, c.worldPosition) for c in controls])

def addPipeValves():
    vCtl = Control(pipes)
    vCtl.addControllers('Pipe', 'valve')

def addChoirValves():
    vCtl = Control(choirs)
    vCtl.addControllers('Choir', 'valve')

def addTeleValves():
    vCtl = Control(telescopics)
    vCtl.addControllers('Tele', 'valve')

def addPipeMotors():
    ctl.addControllers('Pipe', 'mute')
    ctl.addControllers('Pipe', 'roller')
    ctl.addControllers('Pipe', 'tirap')


def getAmplitudes():
    global previousData, amplitudes
    currentData = ctl.getIntonaData()
    amplitudes = currentData
    if len(previousData) < 1:
        previousData = ctl.getIntonaData()
    for i in previousData:
        amplitudes[i] = currentData[i] - previousData[i]
    previousData = currentData
    return amplitudes
    
def createSquare():
    #global squares
    intonaData = ctl.getIntonaData()
    if context.isSensorPositive():
        if intonaData['jab']:
            sq = context.scene.addObject("CubePartHandle", "hoverBoard")
            accelx = intonaData['accel_x']*0.01
            accely = intonaData['accel_y']*0.01
            accelz = intonaData['accel_z']* 0.01
            sq.children[0].localPosition = [ accelx, accely, accelz]
            sq.localAngularVelocity = [accelx, accely, accelz]
            sq.worldPosition = [ accelx, accely, accelz]
            squares.append(sq)

def createSquares():
    dummy = context.scene.objects["Plane.001"]
    # dummy.playAction("PipeLvalveH", 0 , 250)
    for i in range(100):
        sq = context.scene.addObject("CubePart", "hoverBoard")
        sq.worldPosition = [(random() * 100) - 50, (random() * 100) + 20 , (random() * 0.01) - 1]
        sq.worldScale = [(random() * 10), (random() * 10) , (random() * 10)]
        sq.color = colors[randint(0,3)]

def hoverBoardRay():
    context.updateContext()
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
    PipeRay = context.cont.sensors["PipeLValve"]
    pointingAt = PipeRay.hitObject
    hitpos = PipeRay.hitPosition
    hitVector = Vector(hitpos)
    screenPosition = pointingAt.worldTransform
    screenInverted = screenPosition.inverted()
    screenPosition = screenInverted * hitVector
    #print("PipeLvalve poining at {} {}".format(pointingAt, screenPosition))




def createMediator():
    if context.isSensorPositive():
        context.updateContext()
        for valve in config.valves:
            print(" ** Creating ", valve)
            med = Mediator(context.scene.addObject("valveController", "Floor"))
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
    if context.isSensorPositive():
        context.updateContext()
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
                    med = Mediator(context.scene.addObject(ctrl, "Floor"))
                    med.oscurl = oscurl
                    med.id = name
                    med.control = control
                    med.group = instrGroup
                    med.stopDynamics()
                    # med.worldPosition = [(random() * 10) -5, (random() * 5) + 5, 1]
                    med.worldPosition.x = (random() * 20) -10
                    med.worldPosition.y = (random() * 20) -10
                    stackInstruments(med)
                    med.localScale = [0.5, 0.5, 0.5 + (random())]
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
    intonaData = ctl.getIntonaData()
    #print("--------------->     piezd:{}      pizm:{}      ir:{}".format(intonaData["piezd"], intonaData["piezm"], intonaData["ir"]))
    ir = intonaData['ir']
    #context.scene.objects["Forceer"].worldPosition.z = ir*0.01
    context.scene.lights["ShowerLight"].energy = utils.scale(ir*0.001,0.2, 0.8, 0.01, 0.99) 
    #context.scene.lights["ShowerLight"].color = [intonaData["accel_x"] * 0.01, 0,intonaData["accel_y"] * 0.01 ]
    #print("----------> ", context.scene.lights)
    #posCoeff = scalingFactor * 0.001
    for collection in [pipes, choirs, telescopics]:
        if len(collection) > 0:
            updateMediators(collection, ir)
    
    # if len(controls) > 0:
    #     for i in controls:
    #         distance = i.getDistanceTo(scene.objects['Forceer'])
    #         if distance  < 3:
    #             print("{} is at {} from Forceer".format(i, distance))
    #             i.startDynamics()
    #         else:
    #             i.stopDynamics()

def updateMediators(collection, ir):
    for mediator in collection:
        mediator.update()
        mediator.valveForce = utils.scale(ir*0.001,0.2, 0.8, 0.01, 0.99) 
