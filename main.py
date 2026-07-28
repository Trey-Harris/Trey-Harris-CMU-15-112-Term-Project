from cmu_graphics import *
from drone import *
from field import *
import pygame
import numpy
import math
import copy

def onAppStart(app):
    app.field = field()

def redrawAll(app):
    drawShape(600, 4, app.field.fieldCx, app.field.fieldCy, 15)
runApp()