from drone import *
from field import *
from controller import *
from drawingAndProjectionin3D import *
import copy
from cmu_graphics import *

def onAppStart(app):
    app.stepsTaken = 0
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ]
    #Controller vars
    app.connectedController = False
    app.controller = setupController(app)
    app.leftRightAxis = 0
    app.forwardBackwardAxis = 0
    app.throttle = 0

    #Drone vars
    app.forwardTiltAngle = 40
    app.sideTiltAngle = 0
    app.avr = Drone(app, 12)

    #Field Vars
    app.field = Field(app)

    #Prop guard vars
    propGuard1 = PropGuard(app, 45, 20)
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

def onKeyHold(app, keys):
    #tilting forward and backward
    if 'w' in keys:
        if app.forwardTiltAngle <= 60:
            app.forwardTiltAngle += 0.5
    if 's' in keys:
        if app.forwardTiltAngle >= 20:
            app.forwardTiltAngle -= 0.5

    #tilting left and right
    if 'd' in keys:            
        if app.sideTiltAngle <= 45:
            app.sideTiltAngle += 0.5
    if 'a' in keys:
        if app.sideTiltAngle >= -45:
            app.sideTiltAngle -= 0.5

def redrawAll(app):
    drawLabel('Use WASD for tilt if no controller connected', app.width/2, 50)
    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        #print(app.stepsTaken, propGuard)
        drawPrism(propGuard.propGuardEdges, propGuard.projectedCords, app.avr.droneCx, app.avr.droneCy)
    drawPrism(4, app.avr.projectedCubeCords, app.avr.droneCx, app.avr.droneCy)
    drawPrism(4, app.field.projectedFieldCords, app.width/2, app.height/2) #TEST

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

def onStep(app):
    if app.connectedController:
        updateController(app, app.controller)
    app.sideTiltAngle += app.leftRightAxis
    app.forwardTiltAngle += app.forwardBackwardAxis

    if app.sideTiltAngle < 0:
        app.avr.droneCx -= 1*abs(0-app.sideTiltAngle)

    if app.sideTiltAngle > 0:
        app.avr.droneCx += 1*abs(0-app.sideTiltAngle)

    if app.forwardTiltAngle > 40:
        app.avr.droneCy -= 0.5*abs(40-app.forwardTiltAngle)

    if app.forwardTiltAngle < 40:
        app.avr.droneCy += 0.5*abs(40-app.forwardTiltAngle)


    app.stepsTaken += 1
    for propGuard in app.propGuards:
        propGuard.propGuardCords = []
        propGuard.makePropGuard(propGuard.zDepth)
        propGuard.makePropGuard(propGuard.zDepth+10)
        propGuard.projectedCords = project(app, copy.deepcopy(propGuard.propGuardCords))
        
    app.avr.projectedCubeCords = []
    app.avr.makeCenterCube(app.avr.zDepth)
    app.avr.makeCenterCube(app.avr.zDepth+10)
    app.avr.projectedCubeCords = project(app, copy.deepcopy(app.avr.projectedCubeCords))

runApp(width=1200, height=600)