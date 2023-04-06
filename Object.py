import numpy as np
import math


global Index_counter 
Index_counter=0

class Object:
    position_ = 0
    def __init__(self,position,aceleration,radius,color) -> None:
        global Index_counter
        self.position = position
        self.aceleration = aceleration
        self.last_position = self.position
        self.radius = radius
        self.color = color
        self.velocity = np.array([0,0])
        self.grid_pos = np.array([0,0])
        self.index = Index_counter
        Index_counter+=1
    
    def Updateposition(self,dt):
        self.velocity = self.position - self.last_position
        self.last_position = self.position

        self.position = self.position + self.velocity + self.aceleration * (dt**2)
        self.grid_pos = (self.position/self.radius).round()
        self.aceleration = np.array([0,0])
        
    
    def acelerate(self,acc):
        
        self.aceleration=self.aceleration+acc

    def getPosition(self):
        return self.position
    
    def setPosition(self,coord):
        self.position = coord
        
        
    
    def getInfo(self):
        return self.position.round() , self.aceleration.round() , self.velocity , self.grid_pos
        #self.last_position = coord