import numpy
from random import random
from random import randint

positions = [
    [-7.0000, -6.0000, 0.0000],
    [-6.0000, -6.0000, 0.0000],
    [-4.5000, -6.0000, 0.0000],
    [-3.0000, -6.0000, 0.0000],
    [-1.5000, -6.0000, 0.0000],
    [1.5000, -6.0000, 0.0000],
    [3.0000, -6.0000, 0.0000],
    [4.5000, -6.0000, 0.0000],
    [6.0000, -6.0000, 0.0000],
    [5.0000, -2.0000, 0.0000],
    [5.0000, -4.0000, 0.0000],
    [5.0000, -6.0000, 0.0000],
    [3.0000, -6.0000, 0.0000],
    [1.0000, -6.0000, 0.0000],
    [-1.0000, -6.0000, 0.0000],
    [-3.0000, -6.0000, 0.0000],
    [-5.0000, -6.0000, 0.0000],
    [-5.0000, -4.0000, 0.0000],
    [-5.0000, -2.0000, 0.0000],
    [5.0000, 2.0000, 0.0000],
    [5.0000, 4.0000, 0.0000],
    [5.0000, 6.0000, 0.0000],
    [3.0000, 6.0000, 0.0000],
    [1.0000, 6.0000, 0.0000],
    [-1.0000, 6.0000, 0.0000],
    [-3.0000, 6.0000, 0.0000],
    [-5.0000, 6.0000, 0.0000],
    [-5.0000, 4.0000, 0.0000],
    [-5.0000, 2.0000, 0.0000],
    [-2.9959, 0.4204, 1.0000],
    [0.1000, 0.0000, -4619.6812],
    [8.0000, -8.0000, 0.0000],
    [7.0000, -8.0000, 0.0000],
    [7.0000, 9.0000, 0.0000],
    [8.0000, 9.0000, 0.0000],
    [-8.0000, 9.0000, 0.0000],
    [-7.0000, 9.0000, 0.0000],
    [-7.0000, -8.0000, 0.0000],
    [-8.0000, -8.0000, 0.0000],
    [-4.0000, -7.0000, 0.0000],
    [4.0000, -7.0000, 0.0000],
    [0.0206, 9.8338, 19.9777],
    [1.0556, 12.3269, 1.8904],
    [0.1261, 14.0059, 3.0115],
    [-7.9172, -2.1522, 3.2324],
    [-7.1889, -3.3963, 0.2160],
    [-7.1898, -3.3969, 0.5122],
    [-7.1888, -3.3963, 0.8084],
    [9.3071, -1.8861, 0.0237],
    [8.1232, -1.2295, 0.0047],
    [8.0327, -2.4782, 0.0103],
    [8.1589, -3.4264, 0.0181],
    [8.4855, -1.9477, 0.0137],
    [8.8813, -2.1602, 0.0198],
    [8.6679, -2.4197, -0.0731],
    [-8.1985, -0.1651, 0.0403],
    [-6.4917, -7.5331, -0.1601],
    [-7.2138, -7.1972, -0.1576],
    [-6.8652, -6.7890, -0.1647],
    [-3.3746, 16.7017, 13.0592],
    [-1.5441, 9.6195, -0.1135],
    [7.0619, 7.4596, 0.0492],
    [7.5819, 7.1009, -0.0840],
    [-8.8780, -7.7632, 6.8282],
    [10.0233, -8.5183, 17.3529],
    [-9.1462, -13.0838, 16.8621],
    [1.4235, 12.0723, 3.5613],
    [0.1492, 0.4465, 9.7201],
    [-7.9716, 8.3711, 1.8569],
    [-7.3302, 8.5581, 0.6274],
    [-7.1474, 8.4731, 0.7523],
    [-6.6503, 8.5158, 1.8742],
    [-5.6778, 8.6490, 1.2510],
    [-6.6149, 9.3588, 0.0547],
    [7.5510, 9.2478, 2.0348],
    [7.5559, 9.2520, 1.7891],
    [7.5600, 9.2555, 1.5430],
    [6.1304, 6.3356, 1.1467],
    [7.5663, 9.2609, 0.0615],
    [7.1447, 0.2892, 20.7288],
    [-6.5507, 0.2892, 20.9611],
    [0.1626, 0.2892, -0.0466],
    [1.0861, -24.2277, 3.7442],
    [-8.1903, -1.9226, 9.7201],
    [0.0000, -28.7193, 4.8904],
    [1.1849, -6.9152, -0.5588],
    [-2.6112, 5.4503, -2.1680],
    [2.9681, -5.9948, -0.9184],
    [-4.8848, 8.4972, -0.3182],
    [-1.4746, -3.0349, -0.5800],
    [-4.7929, -1.4966, -0.5523],
    [-5.0327, 4.3073, 2.8367],
    [-4.4736, -1.0321, 0.3268],
    [4.1647, 11.6602, 0.1097],
    [-3.4725, -3.6983, 0.0619],
    [-1.0559, -8.6024, 2.1540],
    [2.1960, 0.4825, 1.9292],
    [7.7865, 4.5089, 2.1895],
    [8.2122, 3.0553, 3.0686],
    [-2.9843, -3.5288, 2.8148],
    [-2.6660, 6.0281, 3.7007],
    [6.3336, -6.3856, 4.0591],
    [-3.9961, -3.6927, 2.9864],
    [4.7808, 8.7254, 2.4445],
    [-1.4612, 1.5000, 3.2634],
    [1.5371, 3.3436, 1.3951],
    [1.9004, -3.0792, 3.0696],
    [-2.9157, -6.0855, 1.5334],
]

def scale (OldValue, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

def pickPosition():
    pick = randint(0, len(positions) - 1)
    choice = positions[pick]
    return choice

def randomPosition(coeff):
    x = (random() * coeff) - (coeff/2.)
    y = (random() * coeff) - (coeff/2.)
    z = random() * 4
    return [x, y, z]

def smooth(x):
    x = x
    x = x * 0.95
    x += x
    x = x * 0.2
    return x

# def smooth(x,window_len=11,window='hanning'):
#     """smooth the data using a window with requested size.
    
#     This method is based on the convolution of a scaled window with the signal.
#     The signal is prepared by introducing reflected copies of the signal 
#     (with the window size) in both ends so that transient parts are minimized
#     in the begining and end part of the output signal.
    
#     input:
#         x: the input signal 
#         window_len: the dimension of the smoothing window; should be an odd integer
#         window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
#             flat window will produce a moving average smoothing.

#     output:
#         the smoothed signal
        
#     example:

#     t=linspace(-2,2,0.1)
#     x=sin(t)+randn(len(t))*0.1
#     y=smooth(x)
    
#     see also: 
    
#     numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
#     scipy.signal.lfilter
 
#     TODO: the window parameter could be the window itself if an array instead of a string
#     NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
#     """

#     if x.ndim != 1:
#         raise ValueError, "smooth only accepts 1 dimension arrays."
        
#     if x.size < window_len:
#         raise ValueError, "Input vector needs to be bigger than window size."


#     if window_len<3:
#         return x


#     if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
#         raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


#     s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
#     #print(len(s))
#     if window == 'flat': #moving average
#         w=numpy.ones(window_len,'d')
#     else:
#         w=eval('numpy.'+window+'(window_len)')

#     y=numpy.convolve(w/w.sum(),s,mode='valid')
#     return y
