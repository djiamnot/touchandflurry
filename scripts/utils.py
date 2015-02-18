from random import random

def scale (OldValue, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

def randomPosition():
    x = random() * 8 -4
    y = random() * 8 -4
    z = random() * 4
    return [x, y, z]
