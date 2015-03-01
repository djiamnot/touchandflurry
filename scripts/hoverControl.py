import liblo
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
from ticker import Ticker
from mediator import Mediator
from control import Control
import utils

oneShotAddress = liblo.Address("localhost", 8188)

ticker = Ticker(context.scene.addObject("ticker", "tickerOrigin"))
ticker.localOrientation = [math.radians(90), math.radians(0), math.radians(0)]
ticker.localPosition = [-8.0, 0.0, 10.6]
ticker.localScale = [0.4, 0.4, 0.4]
#context.scene.objects["tickerOrigin"].worldPosition = [0.0, 0.0, 1.0]
sectionText = context.scene.addObject("sectionText", "tickerOrigin")
sectionText.localOrientation = [math.radians(90), math.radians(0), math.radians(0)]
sectionText.localPosition = [8.0, 0.0, 10.6]
sectionText.localScale = [0.4, 0.4, 0.4]
sectionText.color = [0.9, 0.3, 0.3, 0.5]
ENERGY = 0.2
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

def energyUp(x=0.1):
    global ENERGY
    ENERGY += x

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
        'randomvalve': events.ZKEY,
        'printPos': events.MKEY,
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
        #'randomvalve': playRandomValve,
        'randomvalve': tubeLengths,
        'printPos': printPositions
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

def printPositions():
    for o in context.scene.objects:
        print(o.name, o.localPosition)

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
                            if 'Pipe' in oscurl:
                                ctrl = "pipeValve"
                                color = colors[0]
                            else:
                                print("creating valve ", control)
                                ctrl = "valveController"
                                color = colors[0]
                        elif "speed" in control:
                            print("creating speed ", control)
                            ctrl = "speedController"
                            color = colors[1]
                        elif "roller" in control:
                            print("creating roller ", control)
                            ctrl = "rollerController"
                            color = colors[1]
                        elif "length" in control:
                            print("creating roller ", control)
                            ctrl = "lengthController"
                            color = colors[2]
                        elif "dur" in control:
                            print("creating roller ", control)
                            ctrl = "lengthController"
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
                        med.setStartingPosition(context.scene.objects[name].worldPosition)
                        controls.append(med)

def returnAllToOrigin():
    for collection in [pipes, choirs, telescopics]:
        if len(collection) > 0:
            vCtl = Control(collection)
            vCtl.returnToOrigin()

def allOut():
    global ENERGY
    for c in [choirs, pipes, telescopics]:
        ctl = Control(c)
        v = ctl.getControlsByType("valve")
        for valve in v:
            valve.removeParent()
            valve.stopDynamics()
            valve.goTo(Vector((-20, 0, 5)), speed=3, active=True, callback=energyZero)

def energyZero():
    global ENERGY
    ENERGY = 0
                
def getPositions():
    print([(c.oscurl, c.worldPosition) for c in controls])

def addPipeValves():
    vCtl = Control(pipes)
    vCtl.addControllers('Pipe', 'valve', "Forceer")
    #vCtl.addControllers('Pipe', 'roller', "Forceer")

def addChoirValves():
    vCtl = Control(choirs)
    vCtl.addControllers('Choir', 'open', "Forceer")
    vCtl.addControllers('Choir', 'onoff', "Forceer")

def addChoirOpenCtrls():
    vCtl = Control(choirs)
    vCtl.addControllers('Choir', 'speed', 'Forceer')
    vCtl.addControllers('Choir', 'dur', 'Forceer')
    #context.scene.objects["openCenter"].worldAngularVelocity = [0.2, 0.2, 2]
    #[x.goTo(Vector(0, 0.3 , 1)) for x in choirs if 'onoff' in x ]

def addTeleValves():
    vCtl = Control(telescopics)
    vCtl.addControllers('Tele', 'valve', "Forceer")

def addPipeMotors():
    vCtl = Control(pipes)
    vCtl.addControllers('Pipe', 'mute', "Forceer")
    vCtl.addControllers('Pipe', 'roller', "Forceer")
    vCtl.addControllers('Pipe', 'tirap', "Forceer")


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
                    elif "roller" in control:
                        print("creating speed ", control)
                        ctrl = "rollerController"
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
    global valves, ticker
    ticker.update()
    sequence()
    piezosAction()
    intonaData = ctl.getIntonaData()
    ir = intonaData['ir']
    #piezd = intonaData['piezd']
    #piezm = intonaData['piezm']
    # ir = utils.smooth(abs(intonaData['accel_x']))
    #print(" ---> ir", ir)
    #print(" ---> accel_x smooth", utils.smooth(ir))
    #context.scene.objects["Forceer"].worldPosition.z = ir*0.01
    #context.scene.lights["ShowerLight"].energy = utils.scale(ir*0.001,0.2, 0.8, 0.01, 1.99) 
    #context.scene.lights["ShowerLight"].energy = 0.99 
    if irTriggered:
        context.scene.lights["distanceLamp"].energy = 3.5
    else:
        context.scene.lights["distanceLamp"].energy = 0.0
    #context.scene.lights["ShowerLight"].color = [intonaData["accel_x"] * 0.01, 0,intonaData["accel_y"] * 0.01 ]
    #print("----------> ", context.scene.lights)
    #posCoeff = scalingFactor * 0.001
    for collection in [pipes, choirs, telescopics]:
        if len(collection) > 0:
            updateMediators(collection, ENERGY)
    
    # if len(controls) > 0:
    #     for i in controls:
    #         distance = i.getDistanceTo(scene.objects['Forceer'])
    #         if distance  < 3:
    #             print("{} is at {} from Forceer".format(i, distance))
    #             i.startDynamics()
    #         else:
    #             i.stopDynamics()

timeMarkers = [1.2, 4.3, 105.2, 250.7, 320.0, 400, 490.0, 530.0, 590.0, 670, 720.0]
#timeMarkers = [1.2, 2.3, 15.2, 25.7, 32.0, 40, 49.0, 53.0, 59.0, 67, 72.0]
event = 0
irTriggered = False

def zero():
    print("================= zero")
    #telescopicMotors()
def one():
    print("= ==== = ====== = =one")
    #telescopicMotorsControlsStop()
    addChoirs()
    flutesValvesAction()
def two():
    print(" = = == ======= == == ===== two")
    flutesMove()
    energyUp(0.05)
    #telescopicValves()
def three():
    print("======= ========= ========== {}".format(event))
    flutesMove()
    energyUp(0.05)
def four():
    print("======= ========= ========== {}".format(event))
    pipesStageOne()
    groupControlMovements(pipes, "mute", position=random(), speed=random()*10000)
    pipeTiraps(vertical=0.1, horizontal=0.1)
    energyUp(0.15)
def five():
    print("======= ========= ========== {}".format(event))        
    flutesValvesAction()
    energyUp(0.2)
def six():
    print("======= ========= ========== {}".format(event))
    pipesStageTwo()
    addTelescopics()
    telescopicValves()
    telescopicMotors(speed=0.1)
    energyUp(0.05)
def seven():
    print("======= ========= ========== {}".format(event))
    pipesStageThree()
    telescopicMotors(speed=1)
    pipeTiraps()
    energyUp(0.15)
def eight():
    print("======= ========= ========== {}".format(event))
    pipeTiraps(vertical=0.01, horizontal=0.5)
    telescopicMotors(speed=30)
    energyUp(0.1)
def nine():
    print("======= ========= ========== {}".format(event))
    pipeTiraps(vertical=0.99, horizontal=0.5)
    allOut()

def ten():
    print("======= ========= ========== {}".format(event))
    #endObjects(telescopics)
    #endObjects(pipes)
    #endObjects(choirs)

eventMap = {
    0: zero,
    1: one, 
    2: two,
    3: three,
    4: four,
    5: five,
    6: six,
    7: seven,
    8: eight,
    9: nine,
    10: ten,
}


def sequence():
    global event, sectionText
    t = context.scene.objects["ticker"].elapsedTime
    #print(" --> elapsed time", t)
    for idx, mark in enumerate(timeMarkers):
        if t > mark:
            #print("  |--> mark Passed", mark)
            #print("   event at index", idx, eventMap[idx])
            if idx == event:
                print("********** event {} *****************".format(event))
                eventMap[idx]()
                event += 1
                sectionText.text = "{}".format(event)

def piezosAction():
    global irTriggered
    triggerLevel = 600
    intonaData = ctl.getIntonaData()
    ir = intonaData['ir']
    #print("-=-=-=-=-=- > ir:{0:0.2f} ".format(ir))
    if event == 2:
        if ir > triggerLevel:
            print("!!!! Piezo spike", ir)
            if not irTriggered:
                flutesMove()
                irTriggered = True
            else:
                 flutesMove()
                 irTriggered = False
    if event == 4:
        if ir > triggerLevel:
            print("!!!! Piezo spike", ir)
            if not irTriggered:
                flutesValvesAction()
                irTriggered = True
            else:
                flutesValvesAction()
                irTriggered = False
    if event == 5:
        if ir > triggerLevel:
            print("!!!! Piezo spike", ir)
            if not irTriggered:
                flutesMove()
                groupControlMovements(pipes, "roller", position=random(), speed=random()*10000)
                pipeTiraps(vertical=0.1, horizontal=random())
                irTriggered = True
            else:
                groupControlMovements(pipes, "mute", position=random(), speed=random()*1000)
                pipeTiraps(vertical=0.05, horizontal=random())
                irTriggered = False
    if event == 6:
        if ir > triggerLevel:
            print("!!!! Piezo spike", ir)
            if not irTriggered:
                flutesMove()
                groupControlMovements(pipes, "roller", position=random(), speed=random()*10000)
                irTriggered = True
            else:
                groupControlMovements(pipes, "mute", position=random(), speed=random()*10000)
                irTriggered = False
    if event == 7:
        if ir > triggerLevel:
            print("!!!! Piezo spike", ir)
            if not irTriggered:
                flutesMove()
                groupControlMovements(pipes, "roller", position=random(), speed=random()*10000)
                irTriggered = True
            else:
                groupControlMovements(pipes, "mute", position=random(), speed=random()*10000)
                irTriggered = False

    if event == 7:
        if ir > triggerLevel:
            print("!!!! Piezo spike", ir)
            if not irTriggered:
                flutesMove()
                groupControlMovements(pipes, "roller", position=random(), speed=random()*10000)
                pipeTiraps(vertical=0.01, horizontal=0.01)
                irTriggered = True
            else:
                pipeTiraps(vertical=0.2, horizontal=0.2)
                groupControlMovements(pipes, "mute", position=random(), speed=random()*10000)
                irTriggered = False


def dynamicChoirSpeed():
    intonaData = ctl.getIntonaData()
    accelx = intonaData['accel_x'] * 0.001
    accely = intonaData['accel_y'] * 0.001
    accelz = intonaData['accel_z'] * 0.001
    c = Control(choirs)
    s = c.getControlsByType("speed")
    for speed in s:
        speed.active = True
        speed.isDynamic = True
        speed.forceAffected = False
        speed.removeParent()
        speed.startDynamics()
        speed.localLinearVelocity = [accelx, accely, accelz]

    
def removeChoirSpeedDynamics():
    global irTriggered
    intonaData = ctl.getIntonaData()
    c = Control(choirs)
    s = c.getControlsByType("speed")
    for speed in s:
        speed.stopDynamics()
        speed.setParent("Forceer")
        irTriggered = False
   
def pipesStageOne():
    addPipes()
    c = Control(pipes)
    c.addControllers("Pipe", "valve", "Forceer")
    valves = c.getControlsByType("valves")
    mutes = c.getControlsByType("mutes")
    rollers = c.getControlsByType("rollers")
    vert = c.getControlsByType("Vert")
    horiz = c.getControlsByType("Horiz")
    setAndGoTo(valves)
    setAndGoTo(rollers,x=1, speed=20)
    setAndGoTo(mutes, x=-1, speed=20)
    setAndGoTo(vert, x=1, speed=20), 
    setAndGoTo(horiz, x=-1, speed=20)
    stopObjects(rollers)
    stopObjects(mutes)
    stopObjects(vert)
    stopObjects(horiz)
    
def setAndGoTo(collection, x=1, coeff=6, speed=1, end=True):
    xpos = 100
    for c in collection:
        c.active = True
        c.isDynamic = True
        #position = utils.randomPosition(coeff)
        position = utils.pickPosition()
        if abs(x) > 99:
            xpos = position[0]
        else:
            xpos = x
        c.goTo(Vector((xpos, position[1]*3, position[2])), speed, active=True, callback=None)
        c.removeParent()

def stopObjects(collection):
    for c in collection:
        c.active = False
        c.isDynamic = False
        c.stopDynamics()

def pipesStageTwo():
    print("pipes stage 2")
    c = Control(pipes)
    c.addControllers("Pipe", "valve", "Forceer")
    roll = c.getControlsByType("roller")
    setAndGoTo(roll, x=2, speed=1)

def pipesStageThree():
    print("pipes stage 2")
    c = Control(pipes)
    c.addControllers("Pipe", "valve", "Forceer")
    mute = c.getControlsByType("mute")
    setAndGoTo(mute, x=9, speed=30)

def pipeTiraps(vertical=0.1, horizontal=0.1):
    c = Control(pipes)
    # c.addControllers("Tele", "speed", "Forceer")
    horiz = c.getControlsByType("tirapVert")
    for h in horiz:
        liblo.send(oneShotAddress, h.oscurl, vertical)
    vert = c.getControlsByType("tirapHoriz")
    for v in vert:
        liblo.send(oneShotAddress, v.oscurl, horizontal)

def groupControlMovements(collection, control, position=2, speed=10):
    c = Control(collection)
    c.addControllers("Pipe", control, "Forceer")
    d = c.getControlsByType("control")
    setAndGoTo(d, position, speed)
        
# first event
def telescopicMotors(speed=0.3):
    c = Control(telescopics)
    # c.addControllers("Tele", "speed", "Forceer")
    s = c.getControlsByType("speed")
    for sp in s:
        liblo.send(oneShotAddress, sp.oscurl, 0.3)
    l = c.getControlsByType("length")
    for length in l:
        rLen = random()
        liblo.send(oneShotAddress, length.oscurl, rLen)
    # for speed in s:
    #     #controller.worldPosition = [random()* 0.2 - 0.5, random(), random()]
    #     speed.active = True
    #     speed.isDynamic = True
    #     speed.forceAffected = False
    #     position = utils.randomPosition()
    #     speed.goTo(Vector((position[0]*0.1, position[1], position[2])), speed=1, active=True)
    # c.addControllers("Tele", "length", "Forceer")
    # ln = c.getControlsByType("length")
    # for l in ln:
    #     l.forceAffected = False

def telescopicMotorsControlsStop():
    c = Control(telescopics)
    s = c.getControlsByType("speed")
    l = c.getControlsByType("length")
    #print("********* >", s)
    #print("********* >", l)
    for ctl in s:
        ctl.active = False
        ctl.isDynamic = False
        ctl.removeParent()
    for ctl in l:
        ctl.active = False
        ctl.isDynamic = False
        ctl.removeParent()

def telescopicValves():
    c = Control(telescopics)
    c.addControllers("Tele", "valve", "Forceer")

def flutesValvesAction():
    c = Control(choirs)
    c.addControllers("Choir", "valve", "Forceer")
    s = c.getControlsByType("valve")
    for speed in s:
        choose = randint(0, 4)
        if choose is 0:
            speed.active = True
            speed.isDynamic = True
            speed.forceAffected = True
            speed.stopDynamics()
            position = utils.pickPosition()
            speed.goTo(Vector((position[0]*10-5, position[1]*10-5, position[2])), speed=5, active=True)

def flutesMove():
    c = Control(choirs)
    s = c.getControlsByType("valve")
    for valve in s:
        position = utils.pickPosition()
        valve.goTo(Vector((position[0], position[1], position[2])), speed=1, active=True)

def endObjects(obj):
    [o.endObject() for o in obj]
    
            
def playRandomValve():
    vCtl = Control(choirs)
    v = vCtl.getControlsByType("valve");
    rand = randint(0, len(v))
    v[rand].isActive = True
    v[rand].isDynamic = True
    v[rand].goTo(Vector(utils.pickPosition()),speed=2, active=True)

def tubeLengths():
    vCtl = Control(telescopics)
    lenghts = vCtl.getControlsByType("length")
    print("[] lengths", lenghts)
    for i in lenghts:
        i.goTo(Vector(utils.pickPosition()),speed=60, active=True)
        i.isActive = True
        i.isDynamic = True

def updateMediators(collection, ir):
    [handleMediator(mediator, ir) for mediator in collection]
    # for mediator in collection:
    #     mediator.update()
    #     mediator.valveForce = utils.scale(ir*0.001,0.2, 0.8, 0.01, 0.99) 

def handleMediator(obj, ir):
    obj.update()
    #obj.valveForce = utils.scale(ir*0.001,0.2, 0.8, 0.01, 0.99) 
    obj.valveForce = ir

def goTocb(ctl):
    print("goto callback", ctl)
    ctl.isActive = False
    ctl.isDynamic = False
