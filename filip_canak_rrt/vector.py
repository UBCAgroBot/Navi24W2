from math import cos,sin,sqrt
from typing import Type


class Vector:

    def __init__(self, x:float = 0, y:float = 0):
        self.__x = x
        self.__y = y
    
    def norm(self)->float :
        sqrt(self.x**2 + self.y**2)
    
    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def set_x(self,new_x:float):
        self.__x = new_x
        
    def set_y(self,new_y:float):
        self.__y = new_y

    
    def get_as_array(self):
        return [self.__x,self.__y]
    
    def dot(self, vector2:"Vector")->float:
        return self.__x*vector2.get_x() + self.__y*vector2.get_y()

    # Operator overloading lets us do Vector + Vector
    def __add__(self, vector2:"Vector") -> "Vector":
        return Vector(self.__x + vector2.get_x(), self.__y + vector2.get_y())
    

    

    
    




    