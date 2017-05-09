import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.signal import medfilt
from scipy.signal import wiener
import time

start_time = time.time()

x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100])
y = np.array([0,4,6,-4,9,-1,0,-8,3,1,-6,8,0,2,1,0,-3,10,15,9,13,16,7,9,18,6,19,23,25,12,20,15,19,25,15,34,33,20,26,19,31,33,20,26,28,30,21,14,23,19,20,18,25,8,21,19,17,9,12,-7,7,-8,3,5,5,-10,1,2,10,9,-7,-5,-8,-10,-1,8,-9,1,-5,1,0,-8,10,10,5,-3,6,7,-4,-4,2,-1,-9,-3,4,-6,1,2,5,0])

yf = medfilt(y,21)

#xs = np.linspace(x.min(),x.max(),1000)
#ys = spline(x,yf,xs)

yw = wiener(yf,11)

print("--- %s seconds ---" % (time.time() - start_time))
plt.plot(x,y)
plt.plot(x,yw)
plt.show()

