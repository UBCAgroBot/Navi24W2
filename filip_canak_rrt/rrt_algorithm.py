import numpy as np
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc

width = 1280
height = 720
FPS = 24
seconds = 10

valx = 0

if __name__ == "__main__":
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./noise.avi', fourcc, float(FPS), (width, height))

    for _ in range(FPS*seconds):
        frame = np.random.randint(0, 256, 
                              (height, width, 3), 
                              dtype=np.uint8)
        cv2.circle(frame,(valx, int(height/2)),100,(0,0,0),-1)
        valx+= 1
        video.write(frame)


    video.release()
    