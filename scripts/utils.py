from random import random


def scale (OldValue, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

def randomPosition():
    x = random() * 6 - 3
    y = random() * 6 - 3
    z = random() * 4
    return [x, y, z]

def smooth(x):
    x = x
    x = x * 0.95
    x += x
    x = x * 0.2
    return x

