from cmu_graphics import *
import numpy
import math

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.propGuardCords = []
    app.propRadius = 20
    app.propGuardEdges = 8
    app.propGuardCords = []
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    makePropGuard(app, 4)
    makePropGuard(app, 10)
    make2D(app)

def makeXRotationMatrix(angle):
    cosVal = math.cos(math.radians(angle))
    sinVal = math.sin(math.radians(angle))
    return [
        [1, 0, 0, 0],
        [0, cosVal, -sinVal, 0],
        [0, sinVal, cosVal, 0],
        [0, 0, 0, 1]
    ]

def makePropGuard(app, zDepth):
    angle = (360/app.propGuardEdges)/2    #top left vertex if think of like a stop sign
    while angle<360:
        xDisp = app.propRadius*math.cos(math.radians(angle))
        yDisp = app.propRadius*math.sin(math.radians(angle))
        app.propGuardCords.append((app.width/2+xDisp, app.height/2+yDisp,zDepth,1))
        angle += 360/app.propGuardEdges

def make2D(app):
    projectedCords = []
    for i in range(len(app.propGuardCords)):
        projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(40))
        app.propGuardCords[i] = numpy.matmul(projectAndRotateMatrix, app.propGuardCords[i])
        #print(app.propGuardCords)
        # app.propGuardCords[i] = numpy.matmul(app.projectionMatrix, app.propGuardCords[i])
    print(projectAndRotateMatrix) 
    perspectiveFactor = None
    for i in range(len(app.propGuardCords)):
            perspectiveFactor = app.propGuardCords[i][3]
            flatX = app.propGuardCords[i][0]/perspectiveFactor
            flatY = app.propGuardCords[i][1]/perspectiveFactor
            app.propGuardCords[i][0] += flatX
            app.propGuardCords[i][1] += flatY

#Code is my own, Gemini helped me brainstorm the algorithm
def draw2DPolygon(app): 
    #Points
    for i in range(len(app.propGuardCords)):
            x = app.propGuardCords[i][0]
            y = app.propGuardCords[i][1]
            drawCircle(x, y, 1)

    #Edges
    sideLen = app.propGuardEdges #shorter var name for easy typing
    for i in range(sideLen):
        x1, y1 = app.propGuardCords[i][0], app.propGuardCords[i][1]
        x2, y2 = app.propGuardCords[(i+1)%sideLen][0], app.propGuardCords[(i+1)%sideLen][1]    
        # % by sideLen so that index 3 connects to index 0
        drawLine(x1, y1, x2, y2)

        x3, y3 = app.propGuardCords[i+sideLen][0], app.propGuardCords[i+sideLen][1]
        x4, y4 = app.propGuardCords[((i+1)%sideLen)+sideLen][0], app.propGuardCords[((i+1)%sideLen)+sideLen][1]
        drawLine(x3, y3, x4, y4)

        drawLine(x1, y1, x3, y3)

def redrawAll(app):
    for x,y,z,w in app.propGuardCords:
            drawCircle(x, y, 2)
    draw2DPolygon(app)

runApp()