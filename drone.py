from cmu_graphics import *
import math
import numpy
import copy

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.stepsTaken = 0
    app.droneCx = app.width/2
    app.droneCy = app.height/2
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    propGuard1 = PropGuard(app, -100, -100, 6)
    propGuard2 = PropGuard(app, 100, -100, 6)
    propGuard3 = PropGuard(app, -100, 100, 2)
    propGuard4 = PropGuard(app, 100, 100, 2)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

class Drone:
    def __init__(self):
        self.droneCx = app.width/2
        self.droneCy = app.height/2

#Easier to define as a class b/c there are 4 of them with very similar attributes.
class PropGuard:
    def __init__(self, app, xOffset, yOffset, zDepth):
        self.xOffset, self.yOffset = xOffset, yOffset
        self.zDepth = zDepth
        self.propCx, self.propCy = app.droneCx+self.xOffset, app.droneCy+self.yOffset
        self.propRadius = 20
        self.propGuardEdges = 8
        self.propGuardCords = []
        self.makePropGuard(app, self.zDepth)
        self.makePropGuard(app, self.zDepth+10)
        self.projectedCords = self.make2D(app)
        

    def __repr__(self):
        return f'{self.propCx}, {self.propCy}'

    def makePropGuard(self, app, zDepth):
        self.propCx, self.propCy = app.droneCx+self.xOffset, app.droneCy+self.yOffset
        angle = (360/self.propGuardEdges)/2    #top left vertex if think of like a stop sign
        while angle<360:
            xDisp = self.propRadius*math.cos(math.radians(angle))
            yDisp = self.propRadius*math.sin(math.radians(angle))
            self.propGuardCords.append((self.propCx/2+xDisp, self.propCy/2+yDisp, zDepth, 1))
            angle += 360/self.propGuardEdges

    def make2D(self, app):
        projectedCords = copy.deepcopy(self.propGuardCords)
        for i in range(len(self.propGuardCords)):
            projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(70))
            projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeYRotationMatrix(0))
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

def onKeyHold(app, keys):
    if 'left' in keys:
        app.droneCx -= 5
    if 'right' in keys:
        app.droneCx += 5
    if 'up' in keys:
        app.droneCy -= 5
    if 'down' in keys:
        app.droneCy += 5

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
        drawLine(x1, y1, x2, y2)

        x3, y3 = self.projectedCords[i+numSide][0], self.projectedCords[i+numSide][1]
        x4, y4 = self.projectedCords[((i+1)%numSide)+numSide][0], self.projectedCords[((i+1)%numSide)+numSide][1]
        drawLine(x3, y3, x4, y4)

        #Connects the two faces together
        drawLine(x1, y1, x3, y3)

def onStep(app):
    app.stepsTaken += 1
    for propGuard in app.propGuards:
        propGuard.projectedCords = propGuard.propGuardCords #this too early
        propGuard.propGuardCords = []
        propGuard.makePropGuard(app, propGuard.zDepth)
        propGuard.makePropGuard(app, propGuard.zDepth+10)
        propGuard.projectedCords = propGuard.make2D(app)

runApp()