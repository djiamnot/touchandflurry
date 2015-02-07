import bge
import liblo
from mathutils import Vector
from random import random

class Mediator(bge.types.KX_GameObject):
    def __init__ (self, old_owner):
        self.oscaddress = liblo.Address("192.168.0.20", 8188)
        self.cont = bge.logic.getCurrentController()
        self.obj = self.cont.owner
        self.curScene = None
        self.tagetPosition = None
        self.oscurl = None
        self.id = None
        self.control = None
        self.group = None
        self.isDynamic = False

    def stopDynamics(self):
        self.isDynamic = False
        self.suspendDynamics()

    def startDynamics(self):
        self.isDynamic = True
        self.restoreDynamics()


    def updateContext(self):
        self.cont = bge.logic.getCurrentController()
        self.obj = self.cont.owner
        self.curScene = bge.logic.getCurrentScene()

    def getFloorPosition(self):
        self.updateContext()
        position = self.worldPosition
        floorPosition = self.curScene.objects["Floor"].worldTransform
        invertedPosition = floorPosition.inverted()
        objPosition = invertedPosition * position
        return objPosition

    def sendPosition(self):
        velocityVector = self.getLinearVelocity()
        veloSum = sum(velocityVector)
        position = self.getFloorPosition()
        normalizedPosition = self.invert(abs(position.x))
        if self.isDynamic:
            #print("{}'s velocity: {}, normalized position: {}".format(self.oscurl, veloSum, normalizedPosition));
            liblo.send(self.oscaddress, self.oscurl, normalizedPosition)
        else:
            liblo.send(self.oscaddress, self.oscurl, 0)

    def invert(self, f):
        ret = abs(f-1)
        return ret
