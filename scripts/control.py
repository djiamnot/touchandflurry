#!/usr/bin/env python

import context
from random import random
from random import randint
from mathutils import Vector
import utils

class Control:
    def __init__(self, controls):
        print("control class with", controls)
        self.context = context
        self.controls = controls

    def getIntonaData(self):
        return self.context.logic.globalDict['intonaData']        

    def addControllers(self,instrGroup, ctrlType, obj):
        """
        Add a controller to an object as a child.
        groups: Pipe, Tele, Choir
        control types: valve, roller, mute, tirapHoriz, tirapVert, speed, dur, length
        Arguments:
        instrGroup: string - name of the group
        ctrlTye: the type of control
        obj: a blender object to which a controller should be parented
        """
        family = []
        self.context.updateContext()
        if self.context.isSensorPositive():
            # force = scene.objects['Forceer']
            # force.worldLinearVelocity = [(random()*1000) - 500, (random()*1000) - 500, (random()*1000) - 500]
            if len(self.controls) > 0:
                for c in self.controls:
                    print("group", c.group)
                    print("controller", c.control)
                    # c.removeParent()
                    # c.stopDynamics()
                    # c.isDynamic = False
                    print("found this controller", c.control)
                    if ctrlType in c.control and instrGroup in c.group:
                        print("-=-=-= adding", c.group, c.control, c)
                        family.append(c)
                        c.chosen = True
                        c.stopDynamics()
                        # if 'Pipe' in c.group:
                        #     print("--- group", c.group)
                        #     print("--- controller ", c)
                        #     family.append(c)
                # choices = randint(0, len(family))
                # for i in range(choices):
                #     control = randint(0, choices) 
                #     family[control].setParent("Forceer")
                #     family[control].isDynamic = True
                for f in family:
                    f.setParent(obj)
                    f.isDynamic = True
                    f.active = True
                    if 'C2' in f.oscurl:
                        f.valveForce = 0.15
                    else:
                        f.valveForce = 0.5
                        
    def removeParents(self, collection):
        self.context.updateContext()
        intonaData = self.getIntonaData()
        if self.context.isSensorPositive():
            if len(collection) > 0:
                for c in collection:
                    print("removing parent of {} in {}".format(c, collection))
                    xpos = random() * 10 -5
                    ypos = random() * 10 -5
                    zpos = random() * 3
                    vel_x = intonaData['accel_x']*random()*0.01
                    vel_y = intonaData['accel_y']*random()*0.01
                    c.removeParent()
                    #c.worldLinearVelocity = [vel_x, vel_y, 0]
                    c.stopDynamics()
                    c.valveForce = 0.5
                    if c.chosen:
                        c.startDynamics()
                        if 'C2' in c.oscurl:
                            c.valveForce = 0.1
                        else:
                            c.valveForce = 0.5
                            c.goTo(Vector(utils.randomPosition()),speed=2, active=True)
                    else:
                        c.isDynamic = True
                        c.chosen = False
                        
                
    def silence(self, collection):
        self.context.updateContext()
        if self.context.isSensorPositive():
            if len(collection) > 0:
                [self.removeAndSilence(c) for c in collection]

    def removeAndSilence(self, obj):
        """
        Remove object from parent and reset its state to 0
        """
        obj.removeParent()
        obj.chosen = False
        obj.active = False
        obj.isDynamic = False
        obj.stopDynamics()
        if 'onoff' in obj.control :
            obj.valveForce = 0

    def returnToOrigin(self):
        self.context.updateContext()
        if self.context.isSensorPositive():
            if len(self.controls) > 0:
                for c in self.controls:
                    c.removeParent()
                    c.chosen = False
                    #c.active = True
                    c.stopDynamics()
                    print(" ~~~~~ returning to: ", c.startingPosition)
                    origin = c.startingPosition
                    c.goTo(origin, speed=1)

    def getControlsByType(self, ctlType):
        """
        @param: control type (valve, speed, length etc...)
        """
        valves = []
        self.context.updateContext()
        if self.context.isSensorPositive():
            if len(self.controls) > 0:
                for c in self.controls:
                    if ctlType in c.control:
                        print("Found valve", c.control)
                        valves.append(c)
        return valves
