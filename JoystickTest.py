'''
Preliminary Code [12 pts]: You should have a start on your code. 
This code may be prototype code, and so perhaps may not be part 
of your final project. It may or may not have any user interface.
Regardless, there still should be some code. 
You do not need to submit your code anywhere, but do make sure to 
commit your work before the deadline if you are not working in CS Academy.
'''
import pygame #ONLY USED FOR JOYSTICK CONTROL, everything else is CMU Graphics
from cmu_graphics import *

def onAppStart(app):
    app.controller = setupController()
    if not pygame.joystick.get_init:    #No controller connected
        print('No controller connected, use arrow keys (W/S for throttle)')
    app.cx = app.width/2
    app.cy = app.height/2

def redrawAll(app):
    drawCircle(app.cx, app.cy, 20)

def onStep(app):
    updateController(app, app.controller)

def setupController():
    pygame.init()
    pygame.joystick.init()  #initializes joystick MODULE, small part of pygame
    
    controller = pygame.joystick.Joystick(0) #Create joystick instance for my controller
    controller.init()   #initialize my controller
    return controller

###Folowing code written myself, I learned the methods from pygame documentation:
###https://www.pygame.org/docs/ref/joystick.html#pygame.joystick.Joystick.init
def updateController(app, controller):
    pygame.event.pump() #retrieves data from computer USB
    dx = -(controller.get_axis(0)) #negative to flip direction b/c data is input with right being negative which is confusing
    dy = controller.get_axis(1) #forward/backward
    dz = controller.get_axis(2) #throttle level
    print([dx, dy, dz])
    app.cx += dx*5
    app.cy -= dy*5

runApp()
