import numpy as np    

import itertools

class Solver:
    


    
    def __init__(self,object_list,radius) -> None:
        self.gravity = np.array([0,98])
        self.object_list = object_list
        

        self.radiusGrid =radius
        self.grid = np.empty((round(1920/self.radiusGrid), round(1080/self.radiusGrid)), dtype=object)
        for i in range(round(1920/self.radiusGrid)):
            for j in range(round(1080/self.radiusGrid)):
                self.grid[i][j] = []


            
    def update(self,dt):
        

        Sub_steps = 8
        sub_dt = dt/Sub_steps
        for i in range(Sub_steps):

            self.applyGrativty()
            self.ApplyConstraint()
            #self.updateGrid()
            #self.findCollisionsV2()
            self.solverCollisionsV3() 
            self.updatePosition(sub_dt)
            
            
            
            #self.clearGrid()
            
            
            
       
        
    def clearGrid(self):
        self.grid = np.empty((round(1920/self.radiusGrid), round(1080/self.radiusGrid)), dtype=object)
        for i in range(round(1920/self.radiusGrid)):
            for j in range(round(1080/self.radiusGrid)):
                self.grid[i][j] = []

    def updatePosition(self,dt):
        for i in self.object_list:
            i.Updateposition(dt)

    def updateGrid(self):
        for i in self.object_list:
            grid_pos = (i.position/i.radius).round()
            
            if i.position[0] != None:
                self.grid[int(grid_pos[0])][int(grid_pos[1])].append(i)
        #print(self.grid)

    def applyGrativty(self):
        for i in self.object_list:
            i.acelerate(self.gravity)
    
    def ApplyConstraint(self):
        position = np.array([500,500])
        radius = 400
        for i in self.object_list:
            positioned_vec = i.position-position
            #distance = math.sqrt((positioned_vec[0]**2)+(positioned_vec[1]**2))
            distance = np.linalg.norm(positioned_vec)
            if(distance > radius-i.radius):
                normal_vec = positioned_vec / distance
                
                pos = (position+normal_vec*(radius-i.radius))
                i.position=pos

    def infoGet(self):
        i = self.object_list
        return i[0].getInfo() 
    
    #@jit()                        
    def solverCollisions(self):
        for i in self.object_list:
            Object1 = i
            for k in self.object_list:
                Object2 = k
              
                if Object1 != Object2:
                    position_vec = Object1.position - Object2.position
                    #distance = math.sqrt((position_vec[0]**2) + (position_vec[1]**2))
                    distance = np.linalg.norm(position_vec)
                    radiusCo = (Object2.radius)+(Object1.radius)
                    if distance < radiusCo:
                        
                        normal_vec = position_vec / distance
                        delta = radiusCo-distance

                        Object1.position += 0.5 * delta * normal_vec
                        Object2.position -= 0.5 * delta * normal_vec

    def solverCollisionsV3(self):
        moved_objects = set()
        
        for Object1, Object2 in itertools.combinations(self.object_list, 2):
            if (Object1, Object2) not in moved_objects and (Object2, Object1) not in moved_objects:
                position_vec = Object1.position - Object2.position
                distance = np.linalg.norm(position_vec)
                radiusCo = (Object2.radius) + (Object1.radius)
                if distance < radiusCo:
                    normal_vec = position_vec / distance
                    delta = radiusCo - distance
                    Object1.position += 0.5 * delta * normal_vec
                    Object2.position -= 0.5 * delta * normal_vec
                    moved_objects.add((Object1, Object2))
                    moved_objects.add((Object2, Object1))

    def findCollisions(self):
        for i in range(1,len(self.grid)-1):
            for k in range(1,len(self.grid[0])-1):
                #print(i,k,len(self.grid[0]))
                Object1_list = self.grid[i][k]
                if len(Object1_list) == 1: 
                    for x in range(-1,2):
                        for y in range(-1,2):
                            Object2_list = self.grid[i+x][k+y]
                            if len(Object2_list) >= 1:
                                for Objects in Object2_list:
                                    self.solverCollisionV2(Object1_list[0],Objects)
            
 
    def findCollisionsV2(self):
        for i, row in enumerate(self.grid[1:-1,1:-1]):
            for k, Object1_list in enumerate(row):
                if Object1_list:
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            if x == 0 and y == 0:
                                continue
                            Object2_list = self.grid[i+x+1][k+y+1]
                            if Object2_list:
                                for Objects in Object2_list:
                                    self.solverCollisionV4(Object1_list[0],Objects)    

                


    def solverCollisionV2(self,Object1,Object2):
        if Object1 != Object2:
            position_vec = Object1.position - Object2.position
            #distance = math.sqrt((position_vec[0]**2) + (position_vec[1]**2))
            distance = np.linalg.norm(position_vec)
            radiusCo = (Object2.radius)+(Object1.radius)
            if distance < radiusCo:
                normal_vec = position_vec / distance
                delta = radiusCo-distance

                Object1.position += 0.8 * delta * normal_vec
                Object2.position -= 0.8 * delta * normal_vec

    def solverCollisionV3(self, Object1, Object2):
        if Object1 != Object2:
            position_vec = Object1.position - Object2.position
            distance = np.linalg.norm(position_vec)
            radiusCo = Object2.radius + Object1.radius
            if distance < radiusCo:
                normal_vec = position_vec / distance
                delta = radiusCo - distance

                Object1.position += 0.5 * delta * normal_vec
                Object2.position -= 0.5 * delta * normal_vec

                adjustment_vec = np.dot(delta * normal_vec, normal_vec)
                Object1.position += 0 * adjustment_vec
                Object2.position -= 0 * adjustment_vec
                #Object1.position +=  delta * normal_vec
                #Object2.position -=  delta * normal_vec
    
    def solverCollisionV4(self, Object1, Object2):
        if Object1 != Object2:
            position_vec = Object1.position - Object2.position
            distance = np.linalg.norm(position_vec)
            radiusCo = Object2.radius + Object1.radius
            if distance < radiusCo:
                normal_vec = position_vec / distance
                delta = radiusCo - distance

                # Calcular la proyección de penetración mínima
                penetration_vector = delta * normal_vec

                # Desplazar los objetos
                Object1.position += 0.8 * penetration_vector
                Object2.position -= 0.8 * penetration_vector


        #print(Object1.position,Object2.position)