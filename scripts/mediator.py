import bge
from random import random

class Mediator(bge.types.KX_GameObject):
    def __init__ (self, old_owner):
        self.cont = bge.logic.getCurrentController()
        self.obj = self.cont.owner
        scene = bge.logic.getCurrentScene()


