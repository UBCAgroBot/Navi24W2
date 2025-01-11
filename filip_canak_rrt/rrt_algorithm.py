import numpy as np
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc

width = 1280
height = 720
FPS = 24
seconds = 10

valx = 0

frame =  np.genfromtxt("map1.csv", delimiter= ",")
canvas = np.zeros((300,300,3))

for row_ind, row in enumerate(frame):
    for col_ind,col in enumerate(row):
        if col == 0:
            for ind, color in enumerate(canvas[row_ind][col_ind]):
                canvas[row_ind][col_ind][ind] = 0

        else:
            for ind, color in enumerate(canvas[row_ind][col_ind]):
                canvas[row_ind][col_ind][ind] = 256



if __name__ == "__main__":
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./noise.avi', fourcc, float(FPS), (300,300))


    for _ in range(FPS*seconds):
        #frame = np.zeros((height,width,3),dtype =np.uint8)
        #frame = np.random.randint(0, 256, 
          #                     (height, width, 3), 
         #                      dtype=np.uint8)
        
        
        # cv2.circle(frame,(valx, int(height/2)),100,(0,0,0),-1)
        # valx+= 1
        video.write(canvas)


    video.release()
    print("video done")
    