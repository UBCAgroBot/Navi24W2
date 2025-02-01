import cv2
import numpy as np
from math import sin, cos

class Robot:

    def __init__(self, environment:np.array):
        
        self.environment = environment
        self.pos_x:int = 0
        self.pos_y:int = 0

        self.change_x:int = 0
        self.change_y:int = 0

        self.angle:int = 0

        self.width:int = 0
        self.height:int = 0

        self.points = {"topright":np.array(2),"topleft":np.array(2),"botright":np.array(2),"botleft":np.array(2)}

        
    
    def draw(self):
        rotation_matrix = [[cos(self.angle),-sin(self.angle)],[sin(self.angle), cos(self.angle)]]

        # self.points["topright"] = np.matmul(rotation_matrix,((self.pos_x + self.width/2),(self.pos_y - self.height/2)))
        # self.points["topleft"] = np.matmul(rotation_matrix,((self.pos_x - self.width/2),(self.pos_y - self.height/2)))

        # self.points["botright"] = np.matmul(rotation_matrix,((self.pos_x + self.width/2),(self.pos_y + self.height/2)))
        # self.points["botleft"] = np.matmul(rotation_matrix,((self.pos_x - self.width/2),(self.pos_y + self.height/2)))

        self.points["topright"] = np.matmul(rotation_matrix,((self.width/2),(-self.height/2)))
        self.points["topleft"] = np.matmul(rotation_matrix,((-self.width/2),(-self.height/2)))

        self.points["botright"] = np.matmul(rotation_matrix,((self.width/2),(self.height/2)))
        self.points["botleft"] = np.matmul(rotation_matrix,((-self.width/2),(self.height/2)))

        #readd points
        self.points["topright"][0] += self.pos_x
        self.points["topright"][1] += self.pos_y
        
        self.points["topleft"][0] += self.pos_x
        self.points["topleft"][1] += self.pos_y

        self.points["botleft"][0] += self.pos_x
        self.points["botleft"][1] += self.pos_y

        self.points["botright"][0] += self.pos_x
        self.points["botright"][1] += self.pos_y


        
    
        

        cv2.line(self.environment,self.points["topleft"].astype(np.int64),self.points["topright"].astype(np.int64),(255,0,0),20)
       # cv2.line(self.environment,self.points["topleft"].astype(np.int64),self.points["botleft"].astype(np.int64),(255,0,0),20)
       # cv2.line(self.environment,self.points["botleft"].astype(np.int64),self.points["botright"].astype(np.int64),(255,0,0),20)
        #cv2.line(self.environment,self.points["botright"].astype(np.int64),self.points["topright"].astype(np.int64),(255,0,0),20)


        

