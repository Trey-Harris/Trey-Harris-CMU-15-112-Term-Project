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
    app.tiltAngleY = 60
    app.tiltAngleZ = 0
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

#Holds the center cube as well
class Drone:
    def __init__(self, app, zDepth):
        self.droneCx = app.width/2
        self.droneCy = app.height/2
        self.cubeSize = 10
        self.projectedCords = []
        self.makeCenterCube(zDepth)
        self.makeCenterCube(zDepth+10)
        self.projectedCords = self.make2D(app, copy.deepcopy(self.projectedCords))

    def makeCenterCube(self, zDepth):
        angle = 45
        while angle<=360:
            xDisp = self.cubeSize*math.cos(math.radians(angle))
            yDisp = self.cubeSize*math.cos(math.radians(angle))
            self.projectedCords.append((self.droneCx+xDisp, self.droneCy+yDisp, zDepth, 1))
            angle += 90
    def make2D(self, app, projectedCords):
        for i in range(len(self.projectedCords)):
            projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(60))
            #projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeZRotationMatrix(self.tiltAngle))
            projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeYRotationMatrix(app.tiltAngleZ))
            projectedCords[i] = numpy.matmul(projectAndRotateMatrix, self.projectedCords[i])
        perspectiveFactor = None
        for i in range(len(self.projectedCords)):
                perspectiveFactor = self.projectedCords[i][3]
                projectedCords[i][0] /= perspectiveFactor
                projectedCords[i][1] /= perspectiveFactor
        return projectedCords

#Easier to define as a class b/c there are 4 of them with very similar attributes.
class PropGuard:
    def __init__(self, app, drawAngle, zDepth):
        self.offsetRadius = 50
        self.zDepth = zDepth
        self.drawAngle = drawAngle
        self.propRadius = 20
        self.propGuardEdges = 8
        self.propCx = app.avr.droneCx+(self.offsetRadius*math.cos(math.radians(app.tiltAngleY)))
        self.propCy = app.avr.droneCy+(self.offsetRadius*math.sin(math.radians(app.tiltAngleY)))
        
        self.propGuardCords = []
        self.makePropGuard(self.zDepth)
        self.makePropGuard(self.zDepth+10)
        self.projectedCords = self.make2D(app, copy.deepcopy(self.propGuardCords))
        
    def __repr__(self):
        return f'{self.propCx}, {self.propCy}'

    def makePropGuard(self, zDepth):
        self.propCx = (self.offsetRadius*math.cos(math.radians(self.drawAngle)))
        self.propCy = (self.offsetRadius*math.sin(math.radians(self.drawAngle)))
        self.propGuardCords.extend(drawShape(self.propRadius, self.propGuardEdges, self.propCx, self.propCy, zDepth))
    

    def make2D(self, app, projectedCords):
        for i in range(len(self.propGuardCords)):
            projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(60))
            #projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeZRotationMatrix(self.tiltAngle))
            projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeYRotationMatrix(app.tiltAngleZ)) #THIS CONFUSING, FIX IT
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

#cmu_Graphics
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
            app.tiltAngleY += 2
    if 's' in keys:
            for propGuard in app.propGuards:
                #if propGuard.tiltAngleY>=-30:
                app.tiltAngleY -= 2

    #tilting left and right
    if 'd' in keys:
            for propGuard in app.propGuards:
                if app.tiltAngleZ <= 45:
                    app.tiltAngleZ += 2
    if 'a' in keys:
            for propGuard in app.propGuards:
                if app.tiltAngleZ >= -45:
                    app.tiltAngleZ -= 2


def redrawAll(app):
    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        #print(app.stepsTaken, propGuard)
        draw2DPolygon(app, propGuard) 
    drawDroneCenter(app, app.avr)    

#Code is my own, Gemini helped me brainstorm logic for connecting edges w/ mod
def draw2DPolygon(app, self): 
    numSide = self.propGuardEdges #shorter var name for easy typing
    for i in range(numSide):
        x1 = self.projectedCords[i][0] + app.avr.droneCx
        y1 = self.projectedCords[i][1] + app.avr.droneCy
        x2 = self.projectedCords[(i+1)%numSide][0] + app.avr.droneCx
        y2 = self.projectedCords[(i+1)%numSide][1] + app.avr.droneCy
        # % by sideLen so that index 3 connects to index 0
        drawLine(x1, y1, x2, y2)

        x3 = self.projectedCords[i+numSide][0] + app.avr.droneCx
        y3 = self.projectedCords[i+numSide][1]  + app.avr.droneCy
        x4 = self.projectedCords[((i+1)%numSide)+numSide][0] + app.avr.droneCx
        y4 = self.projectedCords[((i+1)%numSide)+numSide][1] + app.avr.droneCy
        drawLine(x3, y3, x4, y4)

        #Connects the two faces together
        drawLine(x1, y1, x3, y3)

def drawDroneCenter(app, self):
    numSide = 4 #shorter var name for easy typing
    for i in range(numSide):
        x1 = self.projectedCords[i][0] #+ app.avr.droneCx
        y1 = self.projectedCords[i][1] #+ app.avr.droneCy
        x2 = self.projectedCords[(i+1)%numSide][0] #+ app.avr.droneCx
        y2 = self.projectedCords[(i+1)%numSide][1] #+ app.avr.droneCy
        # % by sideLen so that index 3 connects to index 0
        drawLine(x1, y1, x2, y2)

        x3 = self.projectedCords[i+numSide][0] #+ app.avr.droneCx
        y3 = self.projectedCords[i+numSide][1]  #+ app.avr.droneCy
        x4 = self.projectedCords[((i+1)%numSide)+numSide][0] #+ app.avr.droneCx
        y4 = self.projectedCords[((i+1)%numSide)+numSide][1] #+ app.avr.droneCy
        drawLine(x3, y3, x4, y4)

        #Connects the two faces together
        drawLine(x1, y1, x3, y3)

def onStep(app):
    app.stepsTaken += 1
    for propGuard in app.propGuards:
        propGuard.projectedCords = propGuard.propGuardCords #this too early
        propGuard.propGuardCords = []
        propGuard.makePropGuard(propGuard.zDepth)
        propGuard.makePropGuard(propGuard.zDepth+10)
        propGuard.projectedCords = propGuard.make2D(app, copy.deepcopy(propGuard.projectedCords))

runApp()

#Drone center projection stuff:
#THIS IS COPY PASTED!!!, I NEED TO GET THIS GOING WITH POLYMORPHISM
# def make2D(self, app, projectedCords):
#         for i in range(len(self.projectedCords)):
#             projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(60))
#             #projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeZRotationMatrix(self.tiltAngle))
#             projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeYRotationMatrix(app.tiltAngleZ))
#             projectedCords[i] = numpy.matmul(projectAndRotateMatrix, self.projectedCords[i])
#         perspectiveFactor = None
#         for i in range(len(self.projectedCords)):
#                 perspectiveFactor = self.projectedCords[i][3]
#                 projectedCords[i][0] /= perspectiveFactor
#                 projectedCords[i][1] /= perspectiveFactor
#         return projectedCords



# OLD PROP GUARD DRAWING:

    # for i in range(len(self.propGuardCords)):
        #     self.propGuardCords[i][0] += self.propCx
        #     self.propGuardCords[i][1] += self.propCy


        ###I WANT TO MAKE THIS A drawShape() FUNCTION THAT CAN WORK WITH MULTIPLE SHAPES
        # angle = (360/self.propGuardEdges)/2    #top left vertex if think of like a stop sign
        # while angle<360:
        #     xDisp = self.propRadius*math.cos(math.radians(angle))
        #     yDisp = self.propRadius*math.sin(math.radians(angle))
        #     self.propGuardCords.append((self.propCx+xDisp, self.propCy+yDisp, zDepth, 1))
        #     angle += 360/self.propGuardEdges