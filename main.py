from field import *
from controller import *
from drone import *
from container import *
from drawingAndProjectionin3D import *
import copy
from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.stepsPerSecond = 30
    app.paused = True
    resetApp(app)

def resetApp(app):
    #Game (not its own class b/c takes info from so many other classes, so 
    #its cleaner if integrated in main)
    app.stepsTaken = 0
    app.timer = 60
    app.points = 0
    app.successfulDrops = 0
    app.containersWithPoints = []
    app.message = ''
    app.gameOver = False
    app.activeSide = 'left'
    app.scores = [
        ['The 112 Dragon', 15112],
        ["Lauren's Candy Jar", 953],
        ['The isPrime Guy', 756],
        ["Stever 5's Resident Cockraoches", 424],
        ['The 112 Axolotl', 112],
        ['Trey debugging this at 2am', -1]
    ]
    startBackground = Image.open("IMG_5797.JPG")
    app.startBg = CMUImage(startBackground.resize((1200,600)))
    leaderboardBackground = Image.open("IMG_5796.JPG")
    app.endBg = CMUImage(leaderboardBackground.resize((1200,600)))
  
    #CLAUDE
    app.camera = ChaseCamera()

    #Drone vars
    app.avr = Drone(app, 5)

    #Controller vars
    app.connectedController = False
    app.controller = setupController(app)
    app.leftRightAxis = 0
    app.forwardBackwardAxis = 0
    app.throttle = 0
    

    #START CLAUDE (EXEMPT):
    app.field = Field()
    app.camera.setBounds(app.field)
    app.field.addContainer(Container(app, 700, 800, 0, -20, 230, 260, 'container1')) 
    app.field.addContainer(Container(app, 300, 400, 0, -20, 230, 260, 'container2'))
    app.field.addContainer(Container(app, 400, 500, 0, -20, 30, 60, 'container3'))

    app.avr.droneX, app.avr.droneY, app.avr.droneZ = app.field.startPosition()

    app.ground = Ground()
    #END CLAUDE

 #Prop guard vars
    propGuard1 = PropGuard(app, 45, 20) #make these be relative toF the drone
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

def onKeyPress(app, key):
    if key == 'space':
        for container in app.field.containers:
            if container.isConnected:
                container.fallHeight = app.avr.droneY
                container.isConnected = False
                container.isFalling = True
                container.fallingContainer(app)
    if key == 'p':
        app.gameOver = not app.gameOver

    if key == 'r':
        app.paused = False
        resetApp(app)


def onKeyHold(app, keys):
    if 'up' in keys and app.throttle<1.5:
        app.throttle += 0.1        
    if 'down' in keys and app.throttle>-0.5:
        app.throttle -= 0.1

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
    if not app.paused:
        takeStep(app)

def takeStep(app):
    if not app.gameOver and not app.paused:
        app.stepsTaken += 1
        if app.stepsTaken%30==0:
            app.timer-=1
        if app.stepsTaken == 1800 or (app.successfulDrops==3 and app.activeSide=='left'):
            app.timer = 60
            app.stepsTaken = 1800 #to account for the fact that could finish before step limit
            app.containersWithPoints = [] #containers can now score points on the other end
            app.activeSide = 'right'
        if app.stepsTaken == 3600 or (app.successfulDrops==6 and app.gameOver==False):
            app.scores.append(['You', app.points])
            app.gameOver = True

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

    if app.throttle>app.avr.throttleThreshold:
        app.avr.droneY -= 5*app.throttle

    if app.throttle<app.avr.throttleThreshold:
        app.avr.droneY += 7.5*(app.avr.throttleThreshold-app.throttle)

    #Update drone position (w/ scale factors for speed)
    app.avr.droneZ += (app.avr.pitch-60) * 0.5   # Arbitrary scale for better flight characteristics
    app.avr.droneX += app.avr.roll * 0.3


    #START EXEMPTED CODE (for camera updates in field code)
    app.avr.droneX, app.avr.droneY, app.avr.droneZ = app.field.clampToArena(app, 
        app.avr.droneX, app.avr.droneY, app.avr.droneZ)
    
    app.camera.follow(app.avr.droneX, app.avr.droneY, app.avr.droneZ)

    app.avr.screenX, app.avr.screenY = app.camera.worldToScreen(
        app.avr.droneX, app.avr.droneY, app.avr.droneZ, app.width/2, app.height/2)
    #END CLAUDE (ALL CODE BELOW IS MY OWN)

def updateContainers(app):
    print(app.points, app.successfulDrops)
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
            app.throttleThreshold = 50
            container.connectContainer(app)

        if container.isFalling:
            container.fallingContainer(app)

    #MAKE THE FOLLOWING THEIR OWN FUNCTIONS B/C REPEATED
    for propGuard in app.propGuards:
        propGuard.propGuardCords = []
        propGuard.makePropGuard(propGuard.zDepth)
        propGuard.makePropGuard(propGuard.zDepth+10)
        propGuard.projectedCords = project(copy.deepcopy(propGuard.propGuardCords), app.avr.pitch, app.avr.roll)


def redrawAll(app):
    if app.paused:
        drawStartScreen(app)
    #To make sure it doesn't continue onward and draw over start screen
    else:
        if app.gameOver:
            displayLeaderboard(app)

        else:
            drawLabel('Use WASD for tilt if no controller connected', app.width/2, 50)
            drawLabel(app.timer, app.width/2, 70)

            y = 5
            for line in app.message.splitlines():
                drawLabel(line, 10, y, align='left-top',size=16, fill='fireBrick')
                y+=16
            
            #EXEMPTED NEXT 3 LINES (Part of field):
            app.field.draw(app, app.camera, app.width/2, app.height/2)
            app.ground.draw(app.camera, app.width/2, app.height/2)
            app.ground.drawShadow(app.camera, app.avr, app.width/2, app.height/2)

            #Drawing Container
            for container in app.field.containers:
                if container.isConnected:
                    drawPrism(4, container.connectedProjection, app.avr.screenX, app.avr.screenY, 'fireBrick')

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


def drawStartScreen(app):
    drawImage(app.startBg, 0, 0)
    drawRect(app.width/2, app.height/2-100, 900, 300, fill='navy', opacity=60, align='center')
    introMessage = '''
    Welcome pilot-in-training! This is Sky Scavenger - AVR Flight Similator

    Your goal: Connect to containers and bring them accross the
    wall in the center of the field. There are two phases, one transporting containers
    from right to left, and the other from left to right. You get more points for
    dropping containers in zones faster, but play it safe at first because crashing
    into the net or wall will ruin the drone!
    '''

    drawRect(350, 450, 500, 150, fill='navy', opacity=60, align='center')
    joystickMessage = '''
    Drone Controller (recommended):
    - Tilt left joystick up and down to control altitude
    - Tilt right joystick in direction you want the drone to move
    - USE SMALL INPUTS!!! It is easy to loose control of the drone at first.
    - Space to drop a container (don't drop from too high or it will break!)
    '''
    drawRect(850, 450, 500, 150, fill='navy', opacity=60, align='center')
    keyboardMessage = '''
    Keyboard (not ideal):
    - Up and down arrow keys for altitude
    - WASD to move the drone forward/backward/left/right
    - Space to drop a container (don't drop from too high or it will break!)
    - WARNING: Keyboard mode is more difficult than with a controller
'''
    messageScreenY = 100
    for line in introMessage.splitlines():
        drawLabel(line, app.width/2, messageScreenY, font='orbitron', size=18, fill='white')
        messageScreenY += 25

    joystickScreenY = 375
    for line in joystickMessage.splitlines():
        drawLabel(line, 350, joystickScreenY, font='orbitron', size=12, fill='white')
        joystickScreenY += 25

    keyboardScreenY = 375
    for line in keyboardMessage.splitlines():
        drawLabel(line, 850, keyboardScreenY, font='orbitron', size=12, fill='white')
        keyboardScreenY += 25

    drawLabel('Press r to begin!', app.width/2, app.height/2+20, font='orbitron', size = 20, fill='red')




def displayLeaderboard(app): 
    drawImage(app.endBg, 0, 0)  
    drawRect(app.width/2, 75, 700, 100, fill='navy', opacity=60, align='center')
    drawLabel('Leaderboard', app.width/2, 75, font='orbitron', size=80, fill='white')
    drawRect(app.width/2, 450, 500, 300, fill='navy', opacity=60, align='center')
    leaderboard = sorted(copy.deepcopy(app.scores), key = lambda x: x[1], reverse=True)

    screenPosY = 325
    for team in leaderboard:
        drawLabel(f'{team[0]} ----- {team[1]}', app.width/2, screenPosY, 
                  font='orbitron', bold=True, size=20, fill='white')
        screenPosY += 35

    drawRect(app.width/2, 250, 750, 35, fill='navy', opacity=60, align='center')
   
    playerIndex = None
    for i in range(len(leaderboard)):
        if leaderboard[i][0] == 'You':
            playerIndex = i
    message = f'You finished ahead of {leaderboard[playerIndex+1][0]}. Good job!'
    drawLabel(message, app.width/2, 250, font='orbitron', size=20,fill='white')

    drawRect(app.width/2, 150, 300, 30, fill='navy', opacity=60, align='center')
    drawLabel('Press r to restart', app.width/2, 150, font='orbitron',size=16,fill='white')

runApp()