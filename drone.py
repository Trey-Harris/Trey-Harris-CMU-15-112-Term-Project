from drawingAndProjectionin3D import *
from field import * #DELETE THIS ONCE I WRITE MY OWN!!!
import math
import copy

#Holds the center cube as well
class Drone:
    def __init__(self, app, zDepth):
        self.cubeSize = 20
        self.zDepth = zDepth
        self.roll = 0
        self.pitch = 60
        self.droneX = 0
        self.droneY = -150
        self.droneZ = -900 
        self.screenX = app.width/2
        self.screenY = app.height/2
        self.projectedCubeCords = []
        self.projectedCubeCords = self.computeCube(app)
        

    def computeCube(self, app):
        self.makeCenterCube(self.zDepth) #probably don't need a function for this.
        self.makeCenterCube(self.zDepth+10)
        self.projectedCubeCords = project(copy.deepcopy(self.projectedCubeCords), self.pitch, self.roll)
        self.projectedCubeCords = makeTranslation(self.projectedCubeCords, 
                                                    self.droneX, self.droneY, self.droneZ)
        return self.makeClaude3D(app, copy.deepcopy(self.projectedCubeCords))

    #FROM CLAUDE, DON"T UNDERSTAND, WORK ON THIS
    def makeClaude3D(self, app, cords):
        L = []
        for i in range(len(cords)):
            screenX, screenY = app.camera.worldToScreen(cords[i][0], 
                                cords[i][1], cords[i][2], 
                                app.width/2, app.height/2)
            L.append((screenX, screenY))
        return L

    def makeCenterCube(self, zDepth):
        self.projectedCubeCords.extend(makeShape(self.cubeSize, 4, 0, 0, zDepth))

 
#Easier to define as a class b/c there are 4 of them with very similar attributes.
#(instead of making part of one huge Drone class)
class PropGuard:
    def __init__(self, app, drawAngle, zDepth):
        self.offsetRadius = 50
        self.zDepth = zDepth
        self.drawAngle = drawAngle
        self.propRadius = 20
        self.propGuardEdges = 8
        self.propCx = app.avr.droneX+(self.offsetRadius*math.cos(math.radians(app.avr.roll)))
        self.propCy = app.avr.droneY+(self.offsetRadius*math.sin(math.radians(app.avr.roll)))
        
        self.propGuardCords = []
        self.makePropGuard(self.zDepth)
        self.makePropGuard(self.zDepth+10)
        self.projectedCords = project(copy.deepcopy(self.propGuardCords), app.avr.pitch, app.avr.roll)

    def makePropGuard(self, zDepth):
        self.propCx = (self.offsetRadius*math.cos(math.radians(self.drawAngle)))
        self.propCy = (self.offsetRadius*math.sin(math.radians(self.drawAngle)))
        self.propGuardCords.extend(makeShape(self.propRadius, self.propGuardEdges, self.propCx, self.propCy, zDepth))