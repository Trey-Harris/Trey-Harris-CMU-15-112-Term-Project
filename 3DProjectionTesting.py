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
    makePropGuard(app)
    make2D(app)

# def makeXRotationMatrix(angle):
#     cosVal = math.cos(math.radians(angle))
#     sinVal = math.sin(math.radians(angle))
#     return [
#         [1, 0, 0, 0],
#         [0, cosVal, -sinVal, 0],
#         [0, sinVal, cosVal, 0],
#         [0, 0, 0, 1]
#     ]
def makePropGuard(app):
    angle = (360/app.propGuardEdges)/2    #top left vertex if think of like a stop sign
    while angle<360:
        xDisp = app.propRadius*math.cos(math.radians(angle))
        yDisp = app.propRadius*math.sin(math.radians(angle))
        print('xDisp = ', xDisp)
        app.propGuardCords.append((app.width/2+xDisp, app.height/2+yDisp,4,1))
        #4 is an arbitraty z depth for now
        angle += 360/app.propGuardEdges

def make2D(app):
    # testCords = [
    #     [-10,-10,40,2],
    #     [10,-10,40,2],
    #     [10,10,40,2],
    #     [-10,10,40,2],
    #     [-10,-10,60,2],
    #     [10,-10,60,2],
    #     [10,10,60,2],
    #     [-10,10,60,2]
    # ]
    projectedCords = []
    for i in range(len(app.propGuardCords)):
        # projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(150))
        # projectedCords.append(numpy.matmul(projectAndRotateMatrix, cords))
        print((numpy.matmul(app.projectionMatrix, app.propGuardCords[i])))
        app.propGuardCords[i] = (numpy.matmul(app.projectionMatrix, app.propGuardCords[i]))
        

    perspectiveFactor = None
    for i in range(len(projectedCords)):
            perspectiveFactor = app.propGuardCords[i][3]
            flatX = projectedCords[i][0]/perspectiveFactor
            print('flatX = ', flatX)
            flatY = projectedCords[i][1]/perspectiveFactor
            app.propGuardCords[i] = (app.width/2 + flatX, app.width/2 + flatY, 4, 1)
            print(app.propGuardCords)
            #idk why I have to scale them so much rn, I'll debug this tonight

def draw2DPolygon(app): 
    #Points
    for i in range(len(app.propGuardCords)):
            x = app.propGuardCords[i][0]
            y = app.propGuardCords[i][1]
            drawCircle(x, y, 2)
    #Edges
    for i in range(0,app.propGuardEdges):
        sideLen = app.propGuardEdges #shorter var name for easy typing
        print(len(app.propGuardCords))
        x1 = app.propGuardCords[i][0]
        y1 = app.propGuardCords[i][1]
        x2 = app.propGuardCords[(i+1)%sideLen][0]    # % by sideLen so that index 3 connects to index 0
        y2 = app.propGuardCords[(i+1)%sideLen][1]
        drawLine(x1, y1, x2, y2)

    # for j in range(app.propGuardEdges, 2*app.propGuardEdges):
    #     print(app.cubeCords[j])
    #     x1 = app.cubeCords[j][0]
    #     y1 = app.cubeCords[j][1]
    #     x2 = app.cubeCords[(j+1)%sideLen][0]
    #     y2 = app.cubeCords[(j+1)%sideLen][1]
    #     drawLine(x1, y1, x2, y2)
        

def redrawAll(app):
    for x,y,z,w in app.propGuardCords:
            drawCircle(x, y, 2)
    draw2DPolygon(app)
        #this the problem:
        # if i < len(app.cubeCords)-1:
        #     x1 = app.width/2 + app.cubeCords[i+1][0]
        #     y1 = app.height/2 + app.cubeCords[i+1][1]
        #     drawLine(x, y, x1, y1)

    #print(app.cubeCords)

# print(makeXRotationMatrix(15))

runApp()