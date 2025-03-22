import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from math import sqrt, sin,cos,pi,atan2,tan


dest = (80,80)# final destination to reach

# starting coordinates
curr_x = 160
curr_y = 160

curr_theta = pi/4 # starting angle

L = 0.5 # The LENGTHWISE distance between the wheels
Kv = 0.05 # velocity coefficient 
Kt = 0.05 # turning coefficient
xa = [curr_x]# array to hold all x values during operation
ya = [curr_y]


v = lambda xs,ys,x,y,k: k*sqrt((xs-x)**2 + (ys-y)**2)#velocity

ts = lambda xs,ys,x,y: atan2((ys-y),(xs-x))# theta star

ad = lambda ts,t: ((ts-t + pi)%(2*pi)) - pi#angular difference

gamma = lambda k, ts, t: k*ad(ts,t) # gamma angle

for i in range(50):

    # Compute the angle we want to be at
    next_angle = ts(dest[0],dest[1],curr_x,curr_y)

    # Move the robot to the next point
    curr_x += v(dest[0],dest[1],curr_x,curr_y,Kv)*cos(curr_theta)
    curr_y += v(dest[0],dest[1],curr_x,curr_y,Kv)*sin(curr_theta)

    # Change the angle appropriately
    curr_theta += v(dest[0],dest[1],curr_x,curr_y,Kt)/L*tan(gamma(Kt,next_angle,curr_theta))

    # record the points in our movement history arrays
    xa.append(curr_x)
    ya.append(curr_y)
    

plt.scatter(xa, ya)
plt.show()
