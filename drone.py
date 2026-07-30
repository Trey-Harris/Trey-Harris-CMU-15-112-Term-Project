from drawingAndProjectionin3D import *
import math
import copy

#Holds the center cube as well
class Drone:
    def __init__(self, app, zDepth):
        self.cubeSize = 40 #Approx 100*sqrt(2)
        self.zDepth = zDepth
        self.roll = 0
        self.pitch = 60
        self.droneX = 0
        self.droneY = -150
        self.droneZ = -900 
        self.throttleThreshold = 0.5 #~30% of 1.5 (which is throttle max)
        self.screenX = app.width/2
        self.screenY = app.height/2
        self.projectedCubeCords = self.makeCenterCube()

    def makeCenterCube(self):
        temp = []
        temp.extend(makeShape(self.cubeSize, 4, 0, 0, self.zDepth))
        temp.extend(makeShape(self.cubeSize, 4, 0, 0, self.zDepth+10))
        temp = project(copy.deepcopy(temp), self.pitch, self.roll)
        return temp
 
#Easier to define as a class b/c there are 4 of them with very similar attributes.
#(instead of making part of one huge Drone class)
class PropGuard:
    def __init__(self, app, drawAngle, zDepth):
        self.offsetRadius = 100
        self.zDepth = zDepth
        self.drawAngle = drawAngle
        self.propRadius = 50
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