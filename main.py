from field import *
from controller import *
from drone import *
from container import *
from drawingAndProjectionin3D import *
import copy
from cmu_graphics import *

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.stepsTaken = 0
    #THIS NEEDS TO BE MOVED AND CITED FROM ERIC
    app.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
    ] #Can multiply by itendity matrix (+ translations in w) to make translations later if need to
    #Controller vars
    app.connectedController = False
    app.controller = setupController(app)
    app.leftRightAxis = 0
    app.forwardBackwardAxis = 0
    app.throttle = 0

    #Drone vars
    app.forwardTiltAngle = 40
    app.sideTiltAngle = 0
    app.avr = Drone(app, 12)   #12 is the zDepth

 #Prop guard vars
    propGuard1 = PropGuard(app, 45, 20) #make these be relative to the drone
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

    #Field Vars
    app.field = Field()

    #Container Vars
    app.container1 = Container(400, 500, 0, 100, 10, 40)
    app.containers = [app.container1]

    #CLAUDE:
    app.field  = Field()
    app.camera = ChaseCamera()
    app.droneX, app.droneY, app.droneZ = 0, -150, -900   # world; y is negative-up
    app.droneX, app.droneY, app.droneZ = app.field.startPosition()
   
def onKeyPress(app, key):
    if key == 't':
        print('hi')
        #for container in app.containers:
        app.container1.isConnected = False
        app.container1.isFalling = True
        app.container1.fallingContainer(app)

def onKeyHold(app, keys):
    #Next 4 lines Claude
    if 'up' in keys:
        app.droneY -= 4        # y is negative-up, so this climbs
    if 'down' in keys:
        app.droneY += 4

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

    #Field (just this line is Claude)
    app.field.draw(app, app.camera, app.width/2, app.height/2)

    #Container
    # drawRect(app.container1.containerCx, app.container1.containerCy, 
    #          app.container1.containerWidth, app.container1.containerHeight, 
    #          align='center', fill=None, border='red')

    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        drawPrism(propGuard.propGuardEdges, propGuard.projectedCords, app.avr.droneCx, app.avr.droneCy)
    #Drone center
    drawPrism(4, app.avr.projectedCubeCords, app.avr.droneCx, app.avr.droneCy)

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
    print(app.container1.isConnected)
    if app.connectedController:
        updateController(app, app.controller)

    app.sideTiltAngle += app.leftRightAxis
    app.forwardTiltAngle += app.forwardBackwardAxis

    #START CLAUDE (EXEMPTED CODE)
    app.droneZ += (app.forwardTiltAngle - 40) * 0.5   # 40 is your neutral
    app.droneX += app.sideTiltAngle * 0.3

    app.droneX, app.droneY, app.droneZ = app.field.clampToArena(
        app.droneX, app.droneY, app.droneZ, 60)
    
    app.camera.follow(app.droneX, app.droneY, app.droneZ)

    app.avr.droneCx, app.avr.droneCy = app.camera.worldToScreen(
        app.droneX, app.droneY, app.droneZ, app.width/2, app.height/2)
    #END CLAUDE (ALL CODE BELOW IS MY OWN)

    #check container connection: THIS CODE BREAKS EVERYTHING, REWRITE
    # for container in app.containers:
    #     if container.isFalling:
    #         container.fallingContainer(app)

    #     if  container.containerCy <= app.avr.droneCy + app.avr.cubeSize:
    #         container.connectContainer(app.avr)

    #     if container.isConnected == True:
    #         container.connectContainer(app.avr)

    #MAKE THE FOLLOWING THEIR OWN FUNCTIONS B/C REPEATED
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

runApp()