from cmu_graphics import *
from main import *
import numpy
import math

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

#Citation: Gemini helped me debug. 
#Found an aliasing issue when this used to be a mutating function
#Pointed out that I was dividing by my projected z instead of my unprojected z
#Citation: Learned about numpy.matmul() fron numpy documentation:
#https://numpy.org/devdocs/reference/generated/numpy.matmul.html#numpy.matmul

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

#Citation: Gemini helped with completing the shape (suggested to use % to 
#connect index 7 with index 0)
def drawPrism(numSides, cords, cx, cy):
    for i in range(numSides):
        x1 = cords[i][0] + cx
        y1 = cords[i][1] + cy
        x2 = cords[(i+1)%numSides][0] + cx
        y2 = cords[(i+1)%numSides][1] + cy
        # % by numSides so that the last index connects to index 0
        drawLine(x1, y1, x2, y2)

        #Draws bottom half of 3D shape
        x3 = cords[i+numSides][0] + cx
        y3 = cords[i+numSides][1] + cy
        x4 = cords[((i+1)%numSides)+numSides][0] + cx
        y4 = cords[((i+1)%numSides)+numSides][1] + cy
        drawLine(x3, y3, x4, y4)

        # Connects the two faces together
        drawLine(x1, y1, x3, y3)

###Projection Matricies: Learned the style of matrix from Eric, Googled the actual ones
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
