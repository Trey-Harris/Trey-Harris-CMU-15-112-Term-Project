from cmu_cpcs_utils import prettyPrint, almostEqual
from cmu_graphics import *
import math

class Field:
    def __init__(self):
        self.gridWidth = 80
        self.gridHeight = 30
        self.fieldGrid = [[0.0]*self.gridWidth for row in range(self.gridHeight)]

        #Initialize grid with elements
        for row in range(self.gridHeight):
            for col in range(self.gridWidth):
                #Field Boundaries
                if col==0 or col==self.gridWidth-1 or row==0 or row==self.gridHeight-1:
                    self.fieldGrid[row][col] = 1.0
                #Walls
                if col==49 or col==50 or col==51:
                    self.fieldGrid[row][col] = 0.67 

                #Container Drop Points
                if (col==20 or col==21) and row==15:
                    self.fieldGrid[row][col] = 0.01 
                if (col==35 or col==36) and (row==10 or row==20):
                    self.fieldGrid[row][col] = 0.01

                #Container Pickup Points
                if (col==60 or col==61) and (row==10 or row==20):
                    self.fieldGrid[row][col] = 0.01
                if (col==70 or col==71) and row==15:
                    self.fieldGrid[row][col] = 0.01

#Citation: Learned technique from Eric, and more specifics from lodev.org:
#https://lodev.org/cgtutor/raycasting.html
#Citation: Gemini helped me decide on looping over the ray number (instead
#of the angles) so that I can use a for loop with the required integer step
#instead of a while loop with a decimal step that could lead to floating point
#innacuuracies that might skip rays that need to be drawn.

def castRays(app):
    facingAngle = 90 #b/c drone never spins
    fov = 70
    numRays = app.width
    angle = facingAngle-(fov/2)
    for i in range(1, numRays+2):
        angle = (facingAngle-(fov/2)) + (fov/numRays)*i
        drawLine(app.droneCx, app.droneCy, app.droneCx+200*math.cos(math.radians(angle)), app.droneCy-200*math.sin(math.radians(angle)))




    
    # while angle>=(facingAngle-(fov/2)):
    #     print(angle)
    #     drawLine(app.droneCx, app.droneCy, app.droneCx+100*math.cos(math.radians(angle)), app.droneCy-100*math.sin(math.radians(angle)))
    #     angle -= 0.1



def onAppStart(app):
    app.field = Field()
    app.setMaxShapeCount(999999999999)
    app.width = 1200
    app.height = 600
    app.droneCx = 500
    app.droneCy = 500

def redrawAll(app):
    visualizeField(app)
    castRays(app)

def visualizeField(app):
    dx = 80
    dy = 2
    color = 'black'
    for row in range(app.field.gridHeight):
        for col in range(app.field.gridWidth):
            if not almostEqual(app.field.fieldGrid[row][col], 0.0):
                color = 'red'
            else:
                color = 'black'
            drawLabel(f'{app.field.fieldGrid[row][col]}', dx, dy,size=7, fill=color)
            dx+=app.width/90
        dy+=app.height/60
        dx = 80

runApp()