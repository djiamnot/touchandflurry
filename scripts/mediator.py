import bge
import liblo
from mathutils import Vector
from random import random

class Mediator(bge.types.KX_GameObject):
    def __init__ (self, old_owner):
        self.oscaddress = liblo.Address("192.168.0.20", 8188)
        #self.oscaddress = liblo.Address("localhost", 8188)
        self.startingPosition = Vector((0.0, 0.0, 0.0))
        self.cont = bge.logic.getCurrentController()
        self.obj = self.cont.owner
        self.curScene = None
        self.tagetPosition = None
        self.oscurl = None
        self.id = None
        self.control = None
        self.group = None
        self.isDynamic = False
        self.active = False
        self.alpha = self.color[3]
        self.moving = False
        self.chosen = False
        self.currentPosition = 0
        self.valveForce = 0
        self.toUpdate = []
        self.callbacks = {}
        self.speed = Vector((0.0, 0.0, 0.0))
        self.destination = Vector((0.0, 0.0, 0.0))
        self.positions = [
            Vector((4.468418121337891, -4.627209186553955, 3.5)),
            # self.startingPosition
        ]
    
    def setStartingPosition(self, vector):
        self.startingPosition = vector

    def nextPosition(self, speed):
        self.goTo(self.positions[self.currentPosition], speed )
        if self.currentPosition < len(self.positions) -1:
            self.currentPosition += 1
        else:
            self.currentPosition = 0

    def setAlpha(self, alpha):
        self.alpha = alpha
        self.color[3] = self.alpha

    def stopDynamics(self):
        # self.isDynamic = False
        self.suspendDynamics()

    def startDynamics(self):
        #self.isDynamic = True
        self.restoreDynamics()


    def updateContext(self):
        self.cont = bge.logic.getCurrentController()
        self.obj = self.cont.owner
        self.curScene = bge.logic.getCurrentScene()

    def getFloorPosition(self):
        if self.isDynamic and self.active:
            self.updateContext()
            position = self.worldPosition
            floorPosition = self.curScene.objects["Floor"].worldTransform
            invertedPosition = floorPosition.inverted()
            objPosition = invertedPosition * position
            return objPosition

    def sendPosition(self):
        if self.isDynamic and self.active:
            velocityVector = self.getLinearVelocity()
            veloSum = sum(velocityVector)
            position = self.getFloorPosition()
            #normalizedPosition = self.invert(abs(position.x)) * self.valveForce
            if 'C2' in self.oscurl:
                normalizedPosition = self.invert(abs(position.x)) * self.valveForce * 0.2
            else:
                normalizedPosition = self.invert(abs(position.x)) * self.valveForce
                self.setAlpha(normalizedPosition)
            #print("{}'s velocity: {}, normalized position: {}".format(self.oscurl, veloSum, normalizedPosition));
            if 'onoff' in self.control:
                onoff = 0
                if normalizedPosition > 0:
                    onoff = int(2)
                else:
                    onoff = 0
                liblo.send(self.oscaddress, self.oscurl, onoff)
            else: 
                liblo.send(self.oscaddress, self.oscurl, normalizedPosition)
        else:
            if 'valve' in self.control:
                liblo.send(self.oscaddress, self.oscurl, 0)
            elif 'onoff' in self.control:
                liblo.send(self.oscaddress, self.oscurl, 0)
            else:
                self.active = False

    def moveTo(self, vector):
        print("-=-=-=-=- moving {} to {}".format(self.id, vector))
        self.applyMovement(vector)

    def invert(self, f):
        ret = abs(f-1)
        return ret

    def goTo(self, destination=None, speed=None, local=False, update=False, callback=None, active=False):
        if not update:
            if destination is None or speed is None:
                return False

            if callback is not None:
                self.callbacks["goTo"] = callback
            elif self.callbacks.get("goTo") is not None:
                self.callbacks.pop("goTo")

            if not local:
                self.destination = destination
            else:
                self.destination = self.localPosition + destination

            trajectory = (self.destination - self.localPosition)
            if not trajectory.length == 0:
                self.speed = trajectory / trajectory.length * speed
            else:
                self.speed = Vector((0.0, 0.0, 0.0))

            if self.goTo not in self.toUpdate:
                self.toUpdate.append(self.goTo)
        else:
            frameSpeed = self.speed / 60.0
            if (self.localPosition - self.destination) > frameSpeed:
                self.localPosition += frameSpeed
                return True
            else:
                self.localPosition = self.destination
                if self.callbacks.get("goTo") is not None:
                    self.callbacks["goTo"]()
                return False

    def update(self):
        for func in self.toUpdate:
            if not func(update=True):
                self.toUpdate.remove(func)
        self.sendPosition()
