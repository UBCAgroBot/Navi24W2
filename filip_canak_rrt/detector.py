import numpy as np
from math import cos,sin
import robot as robot

class Detector:
    """A class acting as a camera or distance sensor or any kind of device
    that will help the robot to detect its surroundings"""
    def __init__(self,radius,robot:robot):
        # If we assume the detector is a trianle with the base oriented up
        self.points = np.zeros(2)

        self.robot = robot
        self.radius = radius
        
    
    def update(self):
        #rotation_matrix = [[cos(self.robot.angle),-sin(self.robot.angle)],[sin(self.robot.angle), cos(self.robot.angle)]]

        self.points[0] = self.robot.position.get_x() + (self.robot.width/2 + self.radius) * cos(self.robot.angle)
        self.points[1] = self.robot.position.get_y() + (self.robot.width/2 + self.radius) * sin(self.robot.angle)
        

        #self.points["right"] = matmul(rotation_matrix, (self.height/2, self.base/2))

        #self.points["base"][0] += self.robot.position.get_x() + self.robot.width/2
        #self.points["base"][1] += self.robot.position.get_y() + self.robot.height/2

        #self.points["left"][0] += self.robot.position.get_y() + self.robot.height/2
        #self.points["left"][1] += self.robot.position.get_y() + self.robot.height/2

        #self.points["right"][0] += self.robot.position.get_y() + self.robot.height/2
        #self.points["right"][1] += self.robot.position.get_y() + self.robot.height/2


