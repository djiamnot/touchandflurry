#!/usr/bin/env python

from bge import logic

cont = logic.getCurrentController()
scene = logic.getCurrentScene()

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
