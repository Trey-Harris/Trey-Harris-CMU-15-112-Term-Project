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
  
    #Controller vars
    app.connectedController = False
    app.controller = setupController(app)
    app.leftRightAxis = 0
    app.forwardBackwardAxis = 0
    app.throttle = 0

    #CLAUDE
    app.camera = ChaseCamera()

    #Drone vars
    # app.avr.pitch = 40
    # app.avr.roll = 0
    app.avr = Drone(app, 5)   #12 is the zDepth

    #START CLAUDE (EXEMPT):
    app.field = Field()
    app.field.addContainer(Container(-800, -700, 0, -40, -25, 25)) 
    #def __init__(self, leftX, rightX, bottomY, topY, closeZ, farZ, color='saddleBrown'):

    app.avr.droneX, app.avr.droneY, app.avr.droneZ = app.field.startPosition()

    app.ground = Ground()
    #END CLAUDE

 #Prop guard vars
    propGuard1 = PropGuard(app, 45, 20) #make these be relative to the drone
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

    #Container Vars
    # app.container1 = Container(app, app.field.fieldLength-300, 
    #                     app.field.fieldLength-200, app.field.fieldDepth+50, app.field.fieldDepth+100, 10, 40)
    # app.containers = [app.container1]

   
def onKeyPress(app, key):
    if key == 't':
        print('hi')
        #for container in app.containers:
        app.container1.isConnected = False
        app.container1.isFalling = True
        app.container1.fallingContainer(app)

def onKeyHold(app, keys):
    #UNIVERSAL DESIGN: Can use controller and keys

    #Next 4 lines Claude
    if 'up' in keys:
        app.avr.droneY -= 4        # y is negative-up, so this climbs
    if 'down' in keys:
        app.avr.droneY += 4

    #tilting forward and backward
    if 'w' in keys:
        if app.avr.pitch <= 80:
            app.avr.pitch += 0.5
    if 's' in keys:
        if app.avr.pitch >= 40:
            app.avr.pitch -= 0.5

    #tilting left and right
    if 'd' in keys:            
        if app.avr.roll <= 45:
            app.avr.roll += 1.5
    if 'a' in keys:
        if app.avr.roll >= -45:
            app.avr.roll -= 1.5

def onStep(app):
    if app.connectedController:
        updateController(app, app.controller)

    if -45<=app.avr.roll<=45:
        app.avr.roll += app.leftRightAxis*2 #x2 to get more snappy flight feel
        #Need these checks b/c could scale by 1.6 and go beyond limit
        if app.avr.roll<-45:
            app.avr.roll=-45
        if app.avr.roll>45:
            app.avr.roll=45

    if 40<=app.avr.pitch<=80:
        app.avr.pitch += app.forwardBackwardAxis*2 
        if app.avr.pitch>80:
            app.avr.pitch=80
        if app.avr.pitch<40:
            app.avr.pitch=40

    #Update drone position (w/ scale factors for speed)
    app.avr.droneZ += (app.avr.pitch-60) * 0.5   # Arbitrary scale for flight feel
    app.avr.droneX += app.avr.roll * 0.3


    #START CLAUDE (EXEMPTED CODE)
    app.avr.droneX, app.avr.droneY, app.avr.droneZ = app.field.clampToArena(
        app.avr.droneX, app.avr.droneY, app.avr.droneZ, 0)
    
    app.camera.follow(app.avr.droneX, app.avr.droneY, app.avr.droneZ)

    app.avr.screenX, app.avr.screenY = app.camera.worldToScreen(
        app.avr.droneX, app.avr.droneY, app.avr.droneZ, app.width/2, app.height/2)
    #END CLAUDE (ALL CODE BELOW IS MY OWN)


    #check container connection: THIS CODE BREAKS EVERYTHING, REWRITE!!!
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
        propGuard.projectedCords = project(copy.deepcopy(propGuard.propGuardCords), app.avr.pitch, app.avr.roll)

    #MAKE A FUCNTION FOR THIS
    app.avr.projectedCubeCords = []
    app.avr.makeCenterCube(app.avr.zDepth) 
    app.avr.makeCenterCube(app.avr.zDepth+10)
    app.avr.projectedCubeCords = project(copy.deepcopy(app.avr.projectedCubeCords), app.avr.pitch, app.avr.roll)

def redrawAll(app):
    drawLabel('Use WASD for tilt if no controller connected', app.width/2, 50)

    #Field (just this line is Claude)
    app.field.draw(app, app.camera, app.width/2, app.height/2)
    #Also updates container cords

    #Container
    #app.container1.draw(app, app.camera, app.width/2, app.height/2)
    #drawPrism(4, app.container1.projectedContainerCords, app.width/4, app.height/4, 'red')

    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        drawPrism(propGuard.propGuardEdges, propGuard.projectedCords, app.avr.screenX, app.avr.screenY, 'black')
    #Drone center
    drawPrism(4, app.avr.projectedCubeCords, app.avr.screenX, app.avr.screenY, 'black')

    #CLAUDE:
    app.ground.draw(app.camera, app.width/2, app.height/2)
    app.ground.drawShadow(app.camera, app.avr, app.width/2, app.height/2)

#Citation: Gemini suggested to use % to connect index 7 with index 0, but the 
#rest of the code is my own
def drawPrism(numSides, cords, cx, cy, color):
    for i in range(numSides):
        x1 = cords[i][0] + cx
        y1 = cords[i][1] + cy
        x2 = cords[(i+1)%numSides][0] + cx
        y2 = cords[(i+1)%numSides][1] + cy
        # % by numSides so that the last index connects to index 0
        drawLine(x1, y1, x2, y2, fill=color)

        #Draws bottom half of 3D shape
        x3 = cords[i+numSides][0] + cx
        y3 = cords[i+numSides][1] + cy
        x4 = cords[((i+1)%numSides)+numSides][0] + cx
        y4 = cords[((i+1)%numSides)+numSides][1] + cy
        drawLine(x3, y3, x4, y4, fill=color)

        # Connects the two faces together
        drawLine(x1, y1, x3, y3, fill=color)

runApp()