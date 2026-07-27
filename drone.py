from cmu_graphics import *
import math
import numpy
import copy

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.stepsTaken = 0
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    app.forwardTiltAngle = 40
    app.sideTiltAngle = 0
    app.avr = Drone(app, 12)
    propGuard1 = PropGuard(app, 45, 20)
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]


def drawShape(radius, numEdges, dispX, dispY, zDepth):
    #This draws actual octagonal prisms w/ x/y disp from center (and cubes)
    shapeCords = []
    angle = (360/numEdges)/2    #top right vertex if think of like a stop sign
    while angle<360:
        dx = radius*math.cos(math.radians(angle))
        dy = radius*math.sin(math.radians(angle))
        shapeCords.append([dx + dispX, dy + dispY, zDepth, 1])
        angle += 360/numEdges
    return shapeCords

def project(app, cords):
    projectedCords = []

    projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(app.forwardTiltAngle))
    projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeYRotationMatrix(app.sideTiltAngle))
    for i in range(len(cords)):
        projectedPoint = numpy.matmul(projectAndRotateMatrix, cords[i])
        perspectiveFactor = cords[i][3]
        projectedPoint[0] /= perspectiveFactor
        projectedPoint[1] /= perspectiveFactor
        projectedCords.append(projectedPoint)
    return projectedCords

#Gemini gave the the idea to use % to connect index 7 with index 0
def drawPrism(numSides, cords, cx, cy):
    for i in range(numSides):
        x1 = cords[i][0] + cx
        y1 = cords[i][1] + cy
        x2 = cords[(i+1)%numSides][0] + cx
        y2 = cords[(i+1)%numSides][1] + cy
        # % by numSides so that the last index connects to index 0
        drawLine(x1, y1, x2, y2)

        x3 = cords[i+numSides][0] + cx
        y3 = cords[i+numSides][1] + cy
        x4 = cords[((i+1)%numSides)+numSides][0] + cx
        y4 = cords[((i+1)%numSides)+numSides][1] + cy
        drawLine(x3, y3, x4, y4)

        # Connects the two faces together
        drawLine(x1, y1, x3, y3)

#Holds the center cube as well
class Drone:
    def __init__(self, app, zDepth):
        self.cubeSize = 20
        self.zDepth = zDepth
        self.droneCx = app.width/2+(self.cubeSize*math.cos(math.radians(app.sideTiltAngle)))
        self.droneCy = app.height/2+(self.cubeSize*math.sin(math.radians(app.sideTiltAngle)))
        self.projectedCubeCords = []
        self.makeCenterCube(self.zDepth)
        self.makeCenterCube(self.zDepth+10)
        self.projectedCubeCords = project(app, copy.deepcopy(self.projectedCubeCords))

    def makeCenterCube(self, zDepth):
        self.projectedCubeCords.extend(drawShape(self.cubeSize, 4, 0, 0, zDepth))

 
#Easier to define as a class b/c there are 4 of them with very similar attributes.
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
        self.makePropGuard(app, self.zDepth)
        self.makePropGuard(app, self.zDepth+10)
        self.projectedCords = project(app, copy.deepcopy(self.propGuardCords))

    def makePropGuard(self, app, zDepth):
        self.propCx = (self.offsetRadius*math.cos(math.radians(self.drawAngle)))
        self.propCy = (self.offsetRadius*math.sin(math.radians(self.drawAngle)))
        self.propGuardCords.extend(drawShape(self.propRadius, self.propGuardEdges, self.propCx, self.propCy, zDepth))

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

# def makeZRotationMatrix(angle):
#     cosVal = math.cos(math.radians(angle))
#     sinVal = math.sin(math.radians(angle))
#     return [
#         [cosVal, -sinVal, 0, 0],
#         [sinVal, cosVal, 0, 0],
#         [0, 0, 1, 0],
#         [0, 0, 0, 1]
#     ]

#cmu_graphics
def onKeyHold(app, keys):
    #tilting forward and backward
    if 'w' in keys:
        for propGuard in app.propGuards:
            if app.forwardTiltAngle <= 60:
                app.forwardTiltAngle += 0.5
    if 's' in keys:
        for propGuard in app.propGuards:
            if app.forwardTiltAngle >= 20:
                app.forwardTiltAngle -= 0.5

    #tilting left and right
    if 'd' in keys:
            for propGuard in app.propGuards:
                if app.sideTiltAngle <= 45:
                    app.sideTiltAngle += 0.5
    if 'a' in keys:
            for propGuard in app.propGuards:
                if app.sideTiltAngle >= -45:
                    app.sideTiltAngle -= 0.5

    if 'left' in keys:
        if app.sideTiltAngle < 0:
            app.avr.droneCx -= 1*abs(0-app.sideTiltAngle)
    if 'right' in keys:
        if app.sideTiltAngle > 0:
            app.avr.droneCx += 1*abs(0-app.sideTiltAngle)
    if 'up' in keys:
        if app.forwardTiltAngle > 40:
            app.avr.droneCy -= 0.5*abs(40-app.forwardTiltAngle)
    if 'down' in keys:
        if app.forwardTiltAngle < 40:
            app.avr.droneCy += 0.5*abs(40-app.forwardTiltAngle)


def redrawAll(app):
    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        #print(app.stepsTaken, propGuard)
        drawPrism(propGuard.propGuardEdges, propGuard.projectedCords, app.avr.droneCx, app.avr.droneCy)
    drawPrism(4, app.avr.projectedCubeCords, app.avr.droneCx, app.avr.droneCy)

def onStep(app):
    app.stepsTaken += 1
    for propGuard in app.propGuards:
        #propGuard.projectedCords = propGuard.propGuardCords #this too early
        propGuard.propGuardCords = []
        propGuard.makePropGuard(app, propGuard.zDepth)
        propGuard.makePropGuard(app, propGuard.zDepth+10)
        propGuard.projectedCords = project(app, copy.deepcopy(propGuard.propGuardCords))
        
    app.avr.projectedCubeCords = []
    app.avr.makeCenterCube(app.avr.zDepth)
    app.avr.makeCenterCube(app.avr.zDepth+10)
    app.avr.projectedCubeCords = project(app, copy.deepcopy(app.avr.projectedCubeCords))

runApp()