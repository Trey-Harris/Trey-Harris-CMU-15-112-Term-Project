from cmu_graphics import *
from drone import *
from field import *
from controller import *
from drawingAndProjectionin3D import *
import pygame
import numpy
import math
import copy

def onAppStart(app):
    app.width = 1200
    app.height = 600
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

    #Prop guard vars
    propGuard1 = PropGuard(app, 45, 20)
    propGuard2 = PropGuard(app, 135, 20)
    propGuard3 = PropGuard(app, 225, 4)
    propGuard4 = PropGuard(app, 315, 4)
    app.propGuards = [propGuard1, propGuard2, propGuard3, propGuard4]

    #Field Vars
    app.field = field()

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
    #drawShape(600, 4, app.field.fieldCx, app.field.fieldCy, 15) #TEST

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

runApp()