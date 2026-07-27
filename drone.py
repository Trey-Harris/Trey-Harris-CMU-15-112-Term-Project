from cmu_graphics import *
import math
import numpy
import copy

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.stepsTaken = 0
    # app.droneCx = app.width/2
    # app.droneCy = app.height/2
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    app.avr = Drone(app)
    propGuard1 = PropGuard(app, 45, 20)
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

class Drone:
    def __init__(self, app):
        self.droneCx = app.width/2
        self.droneCy = app.height/2

#Easier to define as a class b/c there are 4 of them with very similar attributes.
class PropGuard:
    def __init__(self, app, drawAngle, zDepth):
        self.offsetRadius = 50
        self.zDepth = zDepth
        self.drawAngle = drawAngle
        self.tiltAngleY = 60
        self.tiltAngleZ = 0
        self.propRadius = 20
        self.propGuardEdges = 8
        self.propCx = app.avr.droneCx+(self.offsetRadius*math.cos(math.radians(self.tiltAngleY)))
        self.propCy = app.avr.droneCy+(self.offsetRadius*math.sin(math.radians(self.tiltAngleY)))
        
        self.propGuardCords = []
        self.makePropGuard(app, self.zDepth)
        self.makePropGuard(app, self.zDepth+10)
        self.projectedCords = self.make2D(app)
        

    def __repr__(self):
        return f'{self.propCx}, {self.propCy}'

    def makePropGuard(self, app, zDepth):
        #Recalculate centers b/c drone prop moved
        # self.propCx = app.droneCx+(self.offsetRadius*math.cos(math.radians(self.tiltAngle)))
        # self.propCy = app.droneCy+(self.offsetRadius*math.sin(math.radians(self.tiltAngle)))
        #tiltedAngle = self.drawAngle + self.tiltAngle
        self.propCx = (self.offsetRadius*math.cos(math.radians(self.drawAngle)))
        self.propCy = (self.offsetRadius*math.sin(math.radians(self.drawAngle)))

        #This draws actual octagonal prisms w/ x/y disp from center
        angle = (360/self.propGuardEdges)/2    #top left vertex if think of like a stop sign
        # angle += self.tiltAngle #tilts the octagon to match drone tilt
        while angle<360:
            xDisp = self.propRadius*math.cos(math.radians(angle))
            yDisp = self.propRadius*math.sin(math.radians(angle))
            self.propGuardCords.append((self.propCx+xDisp, self.propCy+yDisp, zDepth, 1))
            angle += 360/self.propGuardEdges

    def make2D(self, app):
        projectedCords = copy.deepcopy(self.propGuardCords)
        for i in range(len(self.propGuardCords)):
            projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(60))
            #projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeZRotationMatrix(self.tiltAngle))
            projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeYRotationMatrix(self.tiltAngleZ))
            projectedCords[i] = numpy.matmul(projectAndRotateMatrix, self.propGuardCords[i])
        perspectiveFactor = None
        for i in range(len(self.propGuardCords)):
                perspectiveFactor = self.propGuardCords[i][3]
                projectedCords[i][0] /= perspectiveFactor
                projectedCords[i][1] /= perspectiveFactor
        return projectedCords
    
###Projection Stuff:
def makeXRotationMatrix(angle):
    cosVal = math.cos(math.radians(angle))
    sinVal = math.sin(math.radians(angle))
    return [
        [1, 0, 0, 0],
        [0, cosVal, -sinVal, 0],
        [0, sinVal, cosVal, 0],
        [0, 0, 0, 1]
    ]

def makeYRotationMatrix(angle):
    cosVal = math.cos(math.radians(angle))
    sinVal = math.sin(math.radians(angle))
    return [
        [cosVal, 0, sinVal, 0],
        [0, 1, 0, 0],
        [-sinVal, 0, cosVal, 0],
        [0, 0, 0, 1]
    ]

def makeZRotationMatrix(angle):
    cosVal = math.cos(math.radians(angle))
    sinVal = math.sin(math.radians(angle))
    return [
        [cosVal, -sinVal, 0, 0],
        [sinVal, cosVal, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

#CMU_Graphics
def onKeyHold(app, keys):
    if 'left' in keys:
        app.avr.droneCx -= 5
    if 'right' in keys:
        app.avr.droneCx += 5
    if 'up' in keys:
        app.avr.droneCy -= 5
    if 'down' in keys:
        app.avr.droneCy += 5

    #w and s still need debugging
    if 'w' in keys:
        for propGuard in app.propGuards:
            #if propGuard.tiltAngleY<=30:
            propGuard.tiltAngleY += 2
    if 's' in keys:
            for propGuard in app.propGuards:
                #if propGuard.tiltAngleY>=-30:
                propGuard.tiltAngleY -= 2

    #tilting left and right
    if 'd' in keys:
            for propGuard in app.propGuards:
                if propGuard.tiltAngleZ<=90:
                    propGuard.tiltAngleZ += 2
    if 'a' in keys:
            for propGuard in app.propGuards:
                if propGuard.tiltAngleZ>= -60:
                    propGuard.tiltAngleZ -= 2

def redrawAll(app):
    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        #print(app.stepsTaken, propGuard)
        draw2DPolygon(app, propGuard)     

#Code is my own, Gemini helped me brainstorm logic for connecting edges w/ mod
def draw2DPolygon(app, self): 
    numSide = self.propGuardEdges #shorter var name for easy typing
    for i in range(numSide):
        x1, y1 = self.projectedCords[i][0], self.projectedCords[i][1]
        x2, y2 = self.projectedCords[(i+1)%numSide][0], self.projectedCords[(i+1)%numSide][1]    
        # % by sideLen so that index 3 connects to index 0
        drawLine(app.avr.droneCx+x1, app.avr.droneCy+y1, app.avr.droneCx+x2, app.avr.droneCy+y2)

        x3, y3 = self.projectedCords[i+numSide][0], self.projectedCords[i+numSide][1]
        x4, y4 = self.projectedCords[((i+1)%numSide)+numSide][0], self.projectedCords[((i+1)%numSide)+numSide][1]
        drawLine(app.avr.droneCx+x3, app.avr.droneCy+y3, app.avr.droneCx+x4, app.avr.droneCy+y4)

        #Connects the two faces together
        drawLine(app.avr.droneCx+x1, app.avr.droneCy+y1, app.avr.droneCx+x3, app.avr.droneCy+y3)

def onStep(app):
    app.stepsTaken += 1
    for propGuard in app.propGuards:
        propGuard.projectedCords = propGuard.propGuardCords #this too early
        propGuard.propGuardCords = []
        propGuard.makePropGuard(app, propGuard.zDepth)
        propGuard.makePropGuard(app, propGuard.zDepth+10)
        propGuard.projectedCords = propGuard.make2D(app)

runApp()