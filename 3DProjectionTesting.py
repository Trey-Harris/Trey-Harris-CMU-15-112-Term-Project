from cmu_graphics import *
import numpy
import math

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.propGuardEdges = 4
    app.cubeCords = []
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
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

def make2D(app):
    testCords = [
        [-10,-10,40,2],
        [10,-10,40,2],
        [10,10,40,2],
        [-10,10,40,2],
        [-10,-10,60,2],
        [10,-10,60,2],
        [10,10,60,2],
        [-10,10,60,2]
    ]
    projectedCords = []
    for i in range(len(testCords)):
        # projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(150))
        # projectedCords.append(numpy.matmul(projectAndRotateMatrix, cords))
        projectedCords.append(numpy.matmul(app.projectionMatrix, testCords[i]))

    perspectiveFactor = None
    for i in range(len(projectedCords)):
            perspectiveFactor = projectedCords[i][3]
            flatX = projectedCords[i][0]/perspectiveFactor
            flatY = projectedCords[i][1]/perspectiveFactor
            app.cubeCords.append((app.width/2 + flatX*100, app.width/2 + flatY*100))
            #idk why I have to scale them so much rn, I'll debug this tonight
            #print(len(app.cubeCords))
def draw2DCube(app): 
    #Points
    for i in range(len(app.cubeCords)):
            x = app.cubeCords[i][0]
            y = app.cubeCords[i][1]
            drawCircle(x, y, 2)
    #Edges
    for i in range(0,app.propGuardEdges):
        sideLen = app.propGuardEdges #shorter var name for easy typing
        #N = len(app.cubeCords) #b/c efficiency, get it?
        print(app.cubeCords[i])
        x1 = app.cubeCords[i][0]
        y1 = app.cubeCords[i][1]
        x2 = app.cubeCords[(i+1)%sideLen][0]    # % by sideLen so that index 3 connects to index 0
        y2 = app.cubeCords[(i+1)%sideLen][1]
        drawLine(x1, y1, x2, y2)

    for j in range(app.propGuardEdges, 2*app.propGuardEdges):
        print(app.cubeCords[j])
        x1 = app.cubeCords[j][0]
        y1 = app.cubeCords[j][1]
        x2 = app.cubeCords[(j+1)%sideLen][0]
        y2 = app.cubeCords[(j+1)%sideLen][1]
        drawLine(x1, y1, x2, y2)
        
    
def redrawAll(app):
    draw2DCube(app)
        #this the problem:
        # if i < len(app.cubeCords)-1:
        #     x1 = app.width/2 + app.cubeCords[i+1][0]
        #     y1 = app.height/2 + app.cubeCords[i+1][1]
        #     drawLine(x, y, x1, y1)

    #print(app.cubeCords)

# print(makeXRotationMatrix(15))

runApp()