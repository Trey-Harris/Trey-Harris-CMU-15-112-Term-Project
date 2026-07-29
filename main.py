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
    app.avr = Drone(app, 5)

    #START CLAUDE (EXEMPT):
    app.field = Field()
    app.field.addContainer(Container(app, 700, 800, 0, -20, 230, 260)) 
    app.field.addContainer(Container(app, 300, 400, 0, -20, 230, 260))
    app.field.addContainer(Container(app, 400, 500, 0, -20, 30, 60))

    app.avr.droneX, app.avr.droneY, app.avr.droneZ = app.field.startPosition()

    app.ground = Ground()
    #END CLAUDE

 #Prop guard vars
    propGuard1 = PropGuard(app, 45, 20) #make these be relative toF the drone
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

    #Container Vars
    # app.container1 = Container(app, app.field.fieldLength-300, 
    #                     app.field.fieldLength-200, app.field.fieldDepth+50, app.field.fieldDepth+100, 10, 40)
    # app.containers = [app.container1]


# def start_redrawAll(app):
#     drawLabel('hi', app.width/2, app.height/2)

   
def onKeyPress(app, key):
    if key == 'space':
        for container in app.field.containers:
            container.isConnected = False
            container.isFalling = True
            container.fallingContainer()

def onKeyHold(app, keys):
    #UNIVERSAL DESIGN: Can use controller and keys
    if 'up' in keys:
        app.avr.droneY -= 4        # y is negative-up, why do you do this to me Claude
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
    updateDronePosition(app)
    updateContainers(app)

def updateDronePosition(app):
    
    app.avr.projectedCubeCords = app.avr.makeCenterCube()

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
    app.avr.droneZ += (app.avr.pitch-60) * 0.5   # Arbitrary scale for better flight characteristics
    app.avr.droneX += app.avr.roll * 0.3


    #START EXEMPTED CODE (for camera updates in field code)
    app.avr.droneX, app.avr.droneY, app.avr.droneZ = app.field.clampToArena(
        app.avr.droneX, app.avr.droneY, app.avr.droneZ, 0)
    
    app.camera.follow(app.avr.droneX, app.avr.droneY, app.avr.droneZ)

    app.avr.screenX, app.avr.screenY = app.camera.worldToScreen(
        app.avr.droneX, app.avr.droneY, app.avr.droneZ, app.width/2, app.height/2)
    #END CLAUDE (ALL CODE BELOW IS MY OWN)

def updateContainers(app):
    for container in app.field.containers:
        containerWidth = container.containerRightX-container.containerLeftX
        containerDepth = container.containerFarZ-container.containerCloseZ
        containerHeight = container.containerBottomY-container.containerTopY
        if ((abs(app.avr.droneZ-100-container.containerCloseZ)<=containerDepth/4 or 
            abs(app.avr.droneZ-100-container.containerFarZ)<=containerDepth/4) 
            and
            (abs(app.avr.droneX-container.containerLeftX)<=containerWidth/2 or
            abs(app.avr.droneX-container.containerRightX)<=containerWidth/2)
            and
            (app.avr.droneY)>=-containerHeight):    #negative b/c Claude has increasing
                                                    #altitude as negative
            container.isConnected = True

        if container.isConnected:
            container.connectContainer(app)

        if container.isFalling:
            container.fallingContainer()


    #MAKE THE FOLLOWING THEIR OWN FUNCTIONS B/C REPEATED
    app.stepsTaken += 1
    for propGuard in app.propGuards:
        propGuard.propGuardCords = []
        propGuard.makePropGuard(propGuard.zDepth)
        propGuard.makePropGuard(propGuard.zDepth+10)
        propGuard.projectedCords = project(copy.deepcopy(propGuard.propGuardCords), app.avr.pitch, app.avr.roll)

def redrawAll(app):
    drawLabel('Use WASD for tilt if no controller connected', app.width/2, 50)

    #EXEMPTED NEXT 3 LINES (Part of field):
    app.field.draw(app, app.camera, app.width/2, app.height/2)
    app.ground.draw(app.camera, app.width/2, app.height/2)
    app.ground.drawShadow(app.camera, app.avr, app.width/2, app.height/2)

    #Drawing Container
    for container in app.field.containers:
        if container.isConnected:
            drawPrism(4, container.connectedProjection, app.avr.screenX, app.avr.screenY, 'red')

    #Drawing Prop Guards
    for propGuard in app.propGuards:    #gets each PropGuard instance from a list
        drawPrism(propGuard.propGuardEdges, propGuard.projectedCords, app.avr.screenX, app.avr.screenY, 'black')

    #Drawing Drone Center
    drawPrism(4, app.avr.projectedCubeCords, app.avr.screenX, app.avr.screenY, 'black')


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