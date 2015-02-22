import bge
import time
from mathutils import Vector

class Ticker(bge.types.KX_FontObject):
    def __init__(self, old_owner):
        self.cont = bge.logic.getCurrentController()
        self.obj = bge.logic.getCurrentController()
        self.currentPosition = Vector((0.0, 0.0, 4.0))
        self.counter = 0
        self.signs = ['--', '\\', '|', '/']
        self.color = [0.9, 0.3, 0.3, 0.5]
        self.startTime = time.time()
        self.elapsedTime = 0.0
        #self.localPosition = []

    # def updateContext(self):
    #     self.cont = bge.logic.getCurrentController()
    #     self.obj = self.cont.owner
    #     self.curScene = bge.logic.getCurrentScene()

    def updateTime(self):
        self.elapsedTime = time.time() - self.startTime
        #return (self.elapsedTime)
        
    def moveTo(self, vector):
        #print("-=-=-=-=- ticker going to {}".format(vector))
        self.localPosition = vector
        self.currentPosition = vector

    def step(self, offset):
        """
        Step somewhere
        Args:
        offset: a vector
        """
        self.localPosition += offset
        self.currentPosition = self.localPosition
        #self.moveTo(offset)
        #self.text = "{0:0.3}".format(self.currentPosition[0])
        #self.text = self.updateSign()
        self.updateTime()
        self.text = "{:3.2f}".format(self.elapsedTime)
        
    def updateSign(self):
        # ret = None
        self.updateTime()
        # if self.counter < 4:
        #     ret = self.signs[self.counter]
        #     self.counter += 1
        # else:
        #     self.counter = 0
        # return (ret)
        
        
    def update(self):
        self.step(Vector((0.0001, 0, 0)))
        #print("----> current position", self.localPosition)
