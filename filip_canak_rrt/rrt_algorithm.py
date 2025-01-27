import numpy as np
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import time
import csv
from math import sin,cos
import robot

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



posx = 0
posy = 0

seconds = 10

FPS = 24


mod = 1


if __name__ == "__main__":


    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./noise.avi', fourcc, float(FPS), (WIDTH,HEIGHT))

    mycan = parse_symbols(symbols)

    r = robot.Robot(mycan)
    r.width = 100
    r.height = 100

    r.pos_x = WIDTH/2
    r.pos_y = HEIGHT/2

    for _ in range(FPS*seconds):
        #frame = np.zeros((height,width,3),dtype =np.uint8)
        #frame = np.random.randint(0, 256, 
          #                     (height, width, 3), 
         #                      dtype=np.uint8)
        r.draw()
        mycan = parse_symbols(symbols)

        #drawing the robot
        cv2.line(mycan,r.points["topleft"].astype(np.int64),r.points["topright"].astype(np.int64),(255,0,0),5)
        cv2.line(mycan,r.points["topleft"].astype(np.int64),r.points["botleft"].astype(np.int64),(255,0,0),5)
        cv2.line(mycan,r.points["botleft"].astype(np.int64),r.points["botright"].astype(np.int64),(255,0,0),5)
        cv2.line(mycan,r.points["botright"].astype(np.int64),r.points["topright"].astype(np.int64),(255,0,255),5)
        
        r.change_x = 2
        r.change_y = 2


        r.pos_x += r.change_x*cos(r.angle)
        r.pos_y += r.change_y*sin(r.angle)


        if r.angle >= 2*np.pi:
            r.angle = 0
            mod *= -1
        
        

        r.angle += np.pi/75*mod
        

        # cv2.circle(frame,(valx, int(height/2)),100,(0,0,0),-1)
        # valx+= 1
        video.write(mycan)
    print("video finished")


    