#from main import *
import numpy
import math

def makeShape(radius, numEdges, dispX, dispY, zDepth):
    #This draws actual octagonal prisms w/ x/y disp from center (and cubes)
    shapeCords = []
    angle = (360/numEdges)/2    #top right vertex if think of like a stop sign
    while angle<=360:
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
    projectAndRotateMatrix = numpy.matmul(projectAndRotateMatrix, makeZRotationMatrix(app.sideTiltAngle))
    for i in range(len(cords)):
        projectedPoint = numpy.matmul(projectAndRotateMatrix, cords[i])
        projectedCords.append(projectedPoint)
    return projectedCords

###Projection Matricies: Learned the style of matrix from Eric, Googled the actual ones

#Rotates about x-axis (pitch)
def makeXRotationMatrix(angle):
    cosVal = math.cos(math.radians(angle))
    sinVal = math.sin(math.radians(angle))
    return [
        [1, 0, 0, 0],
        [0, cosVal, -sinVal, 0],
        [0, sinVal, cosVal, 0],
        [0, 0, 0, 1]
    ]

#Rotates about z-axis (into the screen, equivalent to roll)
def makeZRotationMatrix(angle):
    cosVal = math.cos(math.radians(angle))
    sinVal = math.sin(math.radians(angle))
    return [
        [cosVal, 0, sinVal, 0],
        [0, 1, 0, 0],
        [-sinVal, 0, cosVal, 0],
        [0, 0, 0, 1]
    ]

def translateMatrix(dx, dy, dz):
    return[
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ]

#no YRotationMAtrix b/c that would be yaw which the drone doesn't do.