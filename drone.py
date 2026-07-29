from drawingAndProjectionin3D import *
import math
import copy

#Holds the center cube as well
class Drone:
    def __init__(self, app, zDepth):
        self.cubeSize = 20
        self.zDepth = zDepth
        #REMOVE THE TRIG
        self.droneCx = app.width/2
        self.droneCy = app.height/2
        self.projectedCubeCords = []
        self.makeCenterCube(self.zDepth) #probably don't need a function for this.
        self.makeCenterCube(self.zDepth+10)
        self.projectedCubeCords = project(app, copy.deepcopy(self.projectedCubeCords))

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
        self.propCx = app.avr.droneCx+(self.offsetRadius*math.cos(math.radians(app.sideTiltAngle)))
        self.propCy = app.avr.droneCy+(self.offsetRadius*math.sin(math.radians(app.sideTiltAngle)))
        
        self.propGuardCords = []
        self.makePropGuard(self.zDepth)
        self.makePropGuard(self.zDepth+10)
        self.projectedCords = project(app, copy.deepcopy(self.propGuardCords))

    def makePropGuard(self, zDepth):
        self.propCx = (self.offsetRadius*math.cos(math.radians(self.drawAngle)))
        self.propCy = (self.offsetRadius*math.sin(math.radians(self.drawAngle)))
        self.propGuardCords.extend(makeShape(self.propRadius, self.propGuardEdges, self.propCx, self.propCy, zDepth))