import pygame

###I wrote both setupController(app) and updateController(app) myself, but I 
###learned the methods from pygame documentation:
###https://www.pygame.org/docs/ref/joystick.html#pygame.joystick.Joystick.init
def setupController(app):
    pygame.init()
    pygame.joystick.init()  #initializes joystick MODULE, small part of pygame

    if pygame.joystick.get_count() == 0:   #No controller connected
            print('No controller connected, use WASD for tilt')
            return None     #FIX THIS!!! IT WORKS BUT IS KINDA DANGEROUS!!!
    app.connectedController = True
    controller = pygame.joystick.Joystick(0) #Create joystick instance for my controller
    #controller.init()   #initialize my controller (No existe mas en python, no existe mas en mi code)
    return controller


def updateController(app, controller):
    pygame.event.pump() #retrieves data from computer USB
    app.leftRightAxis = -(controller.get_axis(0)) #negative to flip direction b/c data is input with right being negative which is confusing
    app.forwardBackwardAxis = controller.get_axis(1) #forward/backward

    #Need to add 0.8 to account for fact that 0 throttle on joystick is read as
    #~-0.8 by computer
    app.throttle = (controller.get_axis(2))+0.8
    
    #b/c there is a slight inaccuracy in controller reading, complete throttle
    #down can be between -0.8 and -0.7, so I if my scaled throttle is less than
    #0.1, I arbitrarily set it to 0 to prevent negative (or very small positive) throttle.
    if app.throttle <= 0.1:
        app.throttle = 0