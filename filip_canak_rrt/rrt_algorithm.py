import numpy as np
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import time
import csv
from math import sin,cos
import robot
from time import time
import detector 

WIDTH = 500
HEIGHT = 500

ar = np.zeros((WIDTH, HEIGHT))

symbols = {1:(255,255,255),2:(0,255,0)}

for i in range(150):
    for j in range(150):
        ar[i][j] = 1


for i in range(150,300):
    for j in range(150,300):
        ar[i][j] = 2




def parse_symbols(symbol_table:dict) -> np.array:

    return_array = np.zeros((ar.shape[0],ar.shape[1],3),dtype = np.uint8)

    for i in range(ar.shape[0]):
        for j in range(ar.shape[1]):
            
            if ar[i][j] != 0:
                return_array[i][j] = symbol_table[ar[i][j]]

    return return_array



seconds = 10

FPS = 24


mod = 1


if __name__ == "__main__":


    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./noise.avi', fourcc, float(FPS), (WIDTH,HEIGHT))

    mycan = parse_symbols(symbols)

    r = robot.Robot(mycan,WIDTH/2, HEIGHT/2)
    #r.width = 100
    #r.height = 100

    r.pos_x = WIDTH/2
    r.pos_y = HEIGHT/2

    
    r.velocity.set_x(2)

    r.velocity.set_y(2)
    
    start_time = time()

    d = detector.Detector(40,r)
   
    for _ in range(FPS*seconds):
        
        r.update()
        d.update()
        mycan = parse_symbols(symbols)
        #drawing the robot
        cv2.line(mycan,r.points["topleft"].astype(np.int64),r.points["topright"].astype(np.int64),(255,0,0),5)
        cv2.line(mycan,r.points["topleft"].astype(np.int64),r.points["botleft"].astype(np.int64),(255,0,0),5)
        cv2.line(mycan,r.points["botleft"].astype(np.int64),r.points["botright"].astype(np.int64),(255,0,0),5)
        cv2.line(mycan,r.points["botright"].astype(np.int64),r.points["topright"].astype(np.int64),(255,0,255),5)
        
        cv2.circle(mycan,d.points.astype(np.int64),d.radius,(0,0,255),3)

        
        if r.angle >= 2*np.pi:
            r.angle = 0
            mod *= -1
        
        

        r.angle += np.pi/75*mod
        

        video.write(mycan)


    print(f"video rendered in {round(time() - start_time,2)} seconds")


    