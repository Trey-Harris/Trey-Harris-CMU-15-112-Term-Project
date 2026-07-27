from cmu_graphics import *
import math
import numpy

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.droneCx = app.width/2
    app.droneCy = app.height/2
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    makeXRotationMatrix(20)     #Update this with var later
    propGuard1 = PropGuard(app, -50, -50)
    propGuard2 = PropGuard(app, 50, -50)
    propGuard3 = PropGuard(app, -50, 50)
    propGuard4 = PropGuard(app, 50, 50)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

    # propGuard1.makePropGuard(app, 4)
    # propGuard1.makePropGuard(app, 10)
    # propGuard2.makePropGuard(app, 4)
    # propGuard2.makePropGuard(app, 10)
    # propGuard3.makePropGuard(app, 4)
    # propGuard3.makePropGuard(app, 10)
    # propGuard4.makePropGuard(app, 4)
    # propGuard4.makePropGuard(app, 10)
    #make2D(app)


class Drone:
    def __init__(self):
        self.droneCx = app.width/2
        self.droneCy = app.height/2

#Easier to define as a class b/c there are 4 of them with very similar attributes.
class PropGuard:
    def __init__(self, app, xOffset, yOffset):
        self.xOffset, self.yOffset = xOffset, yOffset
        self.propCx, self.propCy = app.droneCx+self.xOffset, app.droneCy+self.yOffset
        self.propRadius = 20
        self.propGuardEdges = 8
        self.propGuardCords = []
        self.makePropGuard(app, 4)
        self.makePropGuard(app, 10)
        make2D(self, app)

    def makePropGuard(self, app, zDepth):
        angle = (360/self.propGuardEdges)/2    #top left vertex if think of like a stop sign
        while angle<360:
            xDisp = self.propRadius*math.cos(math.radians(angle))
            yDisp = self.propRadius*math.sin(math.radians(angle))
            self.propGuardCords.append((app.droneCx/2+xDisp, app.droneCy/2+yDisp,zDepth,1))
            angle += 360/self.propGuardEdges
        make2D(self, app)

def make2D(self, app):
    projectedCords = []
    for i in range(len(self.propGuardCords)):
        projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(40))
        self.propGuardCords[i] = numpy.matmul(projectAndRotateMatrix, self.propGuardCords[i])
        #print(app.propGuardCords)
        # app.propGuardCords[i] = numpy.matmul(app.projectionMatrix, app.propGuardCords[i])
    print(projectAndRotateMatrix) 
    perspectiveFactor = None
    for i in range(len(self.propGuardCords)):
            perspectiveFactor = self.propGuardCords[i][3]
            flatX = self.propGuardCords[i][0]/perspectiveFactor
            flatY = self.propGuardCords[i][1]/perspectiveFactor
            self.propGuardCords[i][0] += flatX
            self.propGuardCords[i][1] += flatY
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

def onKeyHold(app, keys):
    if 'left' in keys:
        app.droneCx -= 5
    if 'right' in keys:
        app.droneCx += 5
    if 'up' in keys:
        app.droneCy -= 5
    if 'down' in keys:
        app.droneCy += 5
    print(app.droneCx, app.droneCy)

#UPDATE FROM HERE
def onStep(app):
    for propGuard in app.propGuards:
        propGuard.propGuardCords = []
        propGuard.makePropGuard(app, 4)
        propGuard.makePropGuard(app, 10)

    # app.propGuardCords = []
    # makePropGuard(app, 4)
    # makePropGuard(app, 10)
    # make2D(app)

def redrawAll(app):
    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        # for x,y,z,w in propGuard.propGuardCords:
        #     drawCircle(x, y, 2)
        draw2DPolygon(app, propGuard)     

#Code is my own, Gemini helped me brainstorm for drawing the connecting edges
def draw2DPolygon(app, self): 
    #Points
    #for propGuard in app.propGuards:    #gets each PropGuard instance from a list
    for x,y,z,w in self.propGuardCords:
        drawCircle(x, y, 2)

    # for i in range(len(app.propGuardCords)):
    #         x = app.propGuardCords[i][0]
    #         y = app.propGuardCords[i][1]
    #         drawCircle(x, y, 1)

    #Edges
    sideLen = self.propGuardEdges #shorter var name for easy typing
    for i in range(sideLen):
        x1, y1 = self.propGuardCords[i][0], self.propGuardCords[i][1]
        x2, y2 = self.propGuardCords[(i+1)%sideLen][0], self.propGuardCords[(i+1)%sideLen][1]    
        # % by sideLen so that index 3 connects to index 0
        drawLine(x1, y1, x2, y2)

        x3, y3 = self.propGuardCords[i+sideLen][0], self.propGuardCords[i+sideLen][1]
        x4, y4 = self.propGuardCords[((i+1)%sideLen)+sideLen][0], self.propGuardCords[((i+1)%sideLen)+sideLen][1]
        drawLine(x3, y3, x4, y4)

        drawLine(x1, y1, x3, y3)

runApp()