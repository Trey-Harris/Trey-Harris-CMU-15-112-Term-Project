from cmu_cpcs_utils import prettyPrint, almostEqual
from cmu_graphics import *

class Field:
    def __init__(self):
        self.gridWidth = 80
        self.gridHeight = 30
        self.fieldGrid = [[0.0]*self.gridWidth for row in range(self.gridHeight)]

        #Initialize grid with elements
        for row in range(self.gridHeight):
            for col in range(self.gridWidth):
                containerDropLocations = {20, 21, 40, 41}
                containerPickupLocations = {60, 61, 70, 71}
                if col==0 or col==self.gridWidth-1 or row==0 or row==self.gridHeight-1:
                    self.fieldGrid[row][col] = 1.0  #Field boundary

                if col==49 or col==50 or col==51:
                    self.fieldGrid[row][col] = 0.67 #Wall

                #container Drop
                if (col==20 or col==21) and row==15:
                    self.fieldGrid[row][col] = 0.01 
                if (col==35 or col==36) and (row==10 or row==20):
                    self.fieldGrid[row][col] = 0.01

                #container pickup
                if (col==60 or col==61) and (row==10 or row==20):
                    self.fieldGrid[row][col] = 0.01
                if (col==70 or col==71) and row==15:
                    self.fieldGrid[row][col] = 0.01
                

                
        # prettyPrint(self.fieldGrid)

def onAppStart(app):
    app.field = Field()
    app.setMaxShapeCount(5000)
    app.width = 1400
    app.height = 600

def redrawAll(app):
    visualizeField(app)

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