import pygame #ONLY USED FOR JOYSTICK CONTROL, everything else is CMU Graphics
from cmu_graphics import *

def onAppStart(app):
    app.connectedController = False
    app.controller = setupController(app)
    app.cx = app.width/2
    app.cy = app.height/2

def redrawAll(app):
    drawCircle(app.cx, app.cy, 20)

def onKeyHold(app, keys):
    #Must all be ifs so that can move in multiple directions at same time
    if 'up' in keys:
        app.cy -= 5
    if 'down' in keys:
        app.cy += 5
    if 'left' in keys:
        app.cx -= 5
    if 'right' in keys:
        app.cx += 5
     

def onStep(app):
    if app.connectedController:
        updateController(app, app.controller)

###I wrote both setupController(app) and updateController(app) myself, but I 
###learned the methods from pygame documentation:
###https://www.pygame.org/docs/ref/joystick.html#pygame.joystick.Joystick.init
def setupController(app):
    pygame.init()
    pygame.joystick.init()  #initializes joystick MODULE, small part of pygame

    if pygame.joystick.get_count() == 0:   #No controller connected
            print('No controller connected, use arrow keys (W/S for throttle)')
            return None
    app.connectedController = True
    controller = pygame.joystick.Joystick(0) #Create joystick instance for my controller
    #controller.init()   #initialize my controller (No existe mas en python, no existe mas en mi code)
    return controller

def updateController(app, controller):
    pygame.event.pump() #retrieves data from computer USB
    dx = -(controller.get_axis(0)) #negative to flip direction b/c data is input with right being negative which is confusing
    dy = controller.get_axis(1) #forward/backward
    throttle = (controller.get_axis(2))+0.8
    #Need to add 0.7 to account for fact that 0 throttle on joystick is read as
    #-0.79xxxxxxxxxx by computer
    if throttle <= 0.1:
        throttle = 0
    #b/c there is a slight inaccuracy in controller reading, complete throttle
    #down can be between -0.8 and -0.7, so I if my scaled throttle is less than
    #0.1, I arbitrarily set it to 0 to prevent negative (or very small positive) throttle.
    
    print([dx, dy, throttle])
    app.cx += dx*5 * (throttle*5)
    app.cy -= dy*5 * (throttle*5)

runApp()
