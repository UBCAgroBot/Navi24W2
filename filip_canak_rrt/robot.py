import cv2
import numpy as np
from math import sin, cos
from vector import Vector


class Robot:

    def __init__(self, environment:np.array,start_x:float = 0, start_y:float =0):
        
        self.environment = environment
       

        self.change_x:int = 0
        self.change_y:int = 0

        self.angle:int = 0

        self.width:int = 30
        self.height:int = 30

        self.position = Vector(start_x,start_y)

        self.velocity = Vector()

        self.points = {"topright":np.array(2),"topleft":np.array(2),"botright":np.array(2),"botleft":np.array(2)}

        
    
    def update(self):
        
        
        # might need to define this elsewhere if things get slow
        rotation_matrix = [[cos(self.angle),-sin(self.angle)],[sin(self.angle), cos(self.angle)]]

        # Apply the matrix rotation transformation with the assumption that the robot is at the origin (0,0) top right
        self.points["topright"] = np.matmul(rotation_matrix,((self.width/2),(-self.height/2)))
        self.points["topleft"] = np.matmul(rotation_matrix,((-self.width/2),(-self.height/2)))

        self.points["botright"] = np.matmul(rotation_matrix,((self.width/2),(self.height/2)))
        self.points["botleft"] = np.matmul(rotation_matrix,((-self.width/2),(self.height/2)))

        # Just move the robot back to its place so that its rotated and in the correct position
        self.points["topright"][0] += self.position.get_x()
        self.points["topright"][1] += self.position.get_y()
        
        self.points["topleft"][0] += self.position.get_x()
        self.points["topleft"][1] += self.position.get_y()

        self.points["botleft"][0] += self.position.get_x()
        self.points["botleft"][1] += self.position.get_y()

        self.points["botright"][0] += self.position.get_x()
        self.points["botright"][1] += self.position.get_y()

        self.position.set_x(self.position.get_x() + self.velocity.get_x()*cos(self.angle))
        self.position.set_y(self.position.get_y() + self.velocity.get_x()*sin(self.angle))