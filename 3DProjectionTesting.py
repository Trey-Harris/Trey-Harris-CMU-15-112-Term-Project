from cmu_graphics import *
import numpy
import math

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.cubeCords = []
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    testProjection(app)

# def makeXRotationMatrix(angle):
#     cosVal = math.cos(math.radians(angle))
#     sinVal = math.sin(math.radians(angle))
#     return [
#         [1, 0, 0, 0],
#         [0, cosVal, -sinVal, 0],
#         [0, sinVal, cosVal, 0],
#         [0, 0, 0, 1]
#     ]

def testProjection(app):
    testCords = [
        [-10,10,10,-10,-10,10,10,-10],       #x values
        [-10,-10,10,10,-10,-10,10,10],   #y values
        [40,40,40,40,60,60,60,60],       #z values
        [2,2,2,2,2,2,2,2]        #w values
    ]
    projectedCords = []
    for i in range(len(testCords[0])):
        cords = [testCords[0][i], testCords[1][i], testCords[2][i], testCords[3][i]]
        # projectAndRotateMatrix = numpy.matmul(app.projectionMatrix, makeXRotationMatrix(150))
        # projectedCords.append(numpy.matmul(projectAndRotateMatrix, cords))
        projectedCords.append(numpy.matmul(app.projectionMatrix, cords))
    make2D(app, projectedCords)
    return projectedCords

def make2D(app, projectedCords):
    for i in range(len(projectedCords)):
        flatX = projectedCords[i][0]/projectedCords[i][3]
        flatY = projectedCords[i][1]/projectedCords[i][3]
        app.cubeCords.append((flatX*100, flatY*100))
        #idk why I have to scale them so much rn, I'll debug this tonight
        #print(len(app.cubeCords))
        
    
def redrawAll(app):
    for i in range(len(app.cubeCords)):
        x = app.width/2 + app.cubeCords[i][0]
        y = app.height/2 + app.cubeCords[i][1]
        drawCircle(x, y, 2)
        if i < len(app.cubeCords)-1:
            x1 = app.width/2 + app.cubeCords[i+1][0]
            y1 = app.height/2 + app.cubeCords[i+1][1]
            drawLine(x, y, x1, y1)

    #print(app.cubeCords)

# print(makeXRotationMatrix(15))

runApp()
print(testProjection(app))