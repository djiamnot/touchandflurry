import bge
from mathutils import Vector

class Ticker(bge.types.KX_GameObject):
    def __init__(self, old_owner):
        self.cont = bge.logic.getCurrentController()
        self.obj = bge.logic.getCurrentController()
        #self.currentPosition = Vector((0.0, 0.0, 9.0))
        #self.localPosition = []

    # def updateContext(self):
    #     self.cont = bge.logic.getCurrentController()
    #     self.obj = self.cont.owner
    #     self.curScene = bge.logic.getCurrentScene()

    def moveTo(self, vector):
        print("-=-=-=-=- ticker going to {}".format(vector))
        self.localPosition = vector
        self.currentPosition = vector

    def step(self, offset):
        """
        Step somewhere
        Args:
        offset: a vector
        """
        self.localPosition += offset
        #self.moveTo(offset)
        #self.text = "{0:0.2%}".format(offset[0])

    def update(self):
        self.step(Vector((0.001, 0.0, 0.0)))
