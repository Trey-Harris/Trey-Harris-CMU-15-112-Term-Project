from drone import *
from drawingAndProjectionin3D import *


class Field:
    def __init__(self, app):
        self.fieldCx = app.width/2
        self.fieldCy = app.height/2
        self.projectedFieldCords = []
        self.zDepth = 15
        self.makeField(self.zDepth)
        self.makeField(self.zDepth+10)
        self.projectedFieldCords = project(app, copy.deepcopy(self.projectedFieldCords))

    def makeField(self, zDepth):
        self.projectedFieldCords.extend(drawShape(200, 4, self.fieldCx, self.fieldCy, zDepth))



#So this raycasting thing is not going to work:

# from cmu_cpcs_utils import prettyPrint, almostEqual
# from cmu_graphics import *
# import math


# #Everything until the field class is copied from CS Academy for visualization.
# #It will not be in my final project, it is just here to act as a visual test 
# #function for my raycasting algorithm
# def onAppStart(app):
#     app.rows = 30
#     app.cols = 80
#     app.boardLeft = 0
#     app.boardTop = 0
#     app.boardWidth = 1200
#     app.boardHeight = 600
#     app.cellBorderWidth = 1

#     app.field = Field()
#     app.setMaxShapeCount(50000)
#     app.width = 1200
#     app.height = 600
#     app.droneCx = 500
#     app.droneCy = 500

# def redrawAll(app):
#     drawBoard(app)
#     drawBoardBorder(app)
#     #visualizeField(app)
#     castRays(app)   #This line is mine :)
#     drawCircle(app.droneCx, app.droneCy, 5)

# def drawBoard(app):
#     for row in range(app.rows):
#         for col in range(app.cols):
#             drawCell(app, row, col)

# def drawBoardBorder(app):
#     # draw the board outline (with double-thickness):
#     drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
#              fill=None, border='black',
#              borderWidth=2*app.cellBorderWidth)

# def drawCell(app, row, col):
#     cellLeft, cellTop = getCellLeftTop(app, row, col)
#     cellWidth, cellHeight = getCellSize(app)
#     drawRect(cellLeft, cellTop, cellWidth, cellHeight,
#              fill=None, border='black',
#              borderWidth=app.cellBorderWidth)
#     if not almostEqual(app.field.fieldGrid[row][col], 0.0):
#         color = 'red'
#     else:
#         color = 'black'
#     drawLabel(f'{app.field.fieldGrid[row][col]}', cellLeft+cellWidth/2, cellTop+cellHeight/2, size=7, fill=color)

# def getCellLeftTop(app, row, col):
#     cellWidth, cellHeight = getCellSize(app)
#     cellLeft = app.boardLeft + col * cellWidth
#     cellTop = app.boardTop + row * cellHeight
#     return (cellLeft, cellTop)

# def getCellSize(app):
#     cellWidth = app.boardWidth / app.cols
#     cellHeight = app.boardHeight / app.rows
#     return (cellWidth, cellHeight)

# #Now back to stuff I wrote:
# def onKeyHold(app, keys):
#     if 'up' in keys:
#         app.droneCy -= 5
#     if 'down' in keys:
#         app.droneCy += 5
#     if 'left' in keys:
#         app.droneCx -= 5
#     if 'right' in keys:
#         app.droneCx += 5

# def onMouseMove(app, mouseX, mouseY):
#     app.droneCx, app.droneCy = mouseX, mouseY


# class Field:
#     def __init__(self):
#         self.numCols = 80
#         self.numRows = 30
#         self.fieldGrid = [[0.0]*self.numCols for row in range(self.numRows)]

#         #Initialize grid with elements
#         for row in range(self.numRows):
#             for col in range(self.numCols):
#                 #Field Boundaries
#                 if col==0 or col==self.numCols-1 or row==0 or row==self.numRows-1:
#                     self.fieldGrid[row][col] = 1.0
#                 #Walls
#                 if col==49 or col==50 or col==51:
#                     self.fieldGrid[row][col] = 0.67 

#                 #Container Drop Points
#                 if (col==20 or col==21) and row==15:
#                     self.fieldGrid[row][col] = 0.01 
#                 if (col==35 or col==36) and (row==10 or row==20):
#                     self.fieldGrid[row][col] = 0.01

#                 #Container Pickup Points
#                 if (col==60 or col==61) and (row==10 or row==20):
#                     self.fieldGrid[row][col] = 0.01
#                 if (col==70 or col==71) and row==15:
#                     self.fieldGrid[row][col] = 0.01


# #Citation: Learned technique from Eric, and more specifics from lodev.org:
# #https://lodev.org/cgtutor/raycasting.html
# #Citation: Gemini helped me decide on looping over the ray number (instead
# #of the angles) so that I can use a for loop with the required integer step
# #instead of a while loop with a decimal step that could lead to floating point
# #innacuuracies that might skip rays that need to be drawn. Also helped me learn
# #more about the implementation of Digital Differential Analysis in Python

# #LOOK AT CS NOTES TO SEE HOW TO CASH THE ANGLES, MAYBE STORE IN A SET B/C ORDER NO MATTER?
# #Does order matter, b/c I will just draw on the angle value anyway which I have access
# #to if I access a value from a set?
# def castRays(app):
#     facingAngle = 90 #b/c drone never spins
#     fov = 70
#     numRays = app.width//15 #Ideally I would be at 1, but this helps it run faster w/o much resolution loss
#     angle = facingAngle-(fov/2)
    
#     #I need to be not stupid and figure these out.
#     droneRow = (app.field.numRows*app.width/app.field.numRows)//app.droneCx
#     droneCol = app.droneCx//(app.field.numCols)
#     print(droneRow, droneCol)

#     nextCellDx = app.width/app.cols
#     nextCellDy = app.height/app.rows
#     # distToXBound = #SOMETHING
#     # distToYBound = #SOMETHING


#     #DON'T DELETE THIS, JUST COMMENTED FOR TESTING PURPOSES
#     for i in range(1, numRays+1):
#         farLeftAngle = (facingAngle-(fov/2))
#         angleStep = (fov/numRays)*i
#         angle = farLeftAngle + angleStep
#         drawLine(app.droneCx, app.droneCy, app.droneCx+200*math.cos(math.radians(angle)), app.droneCy-200*math.sin(math.radians(angle)), opacity = 5)




# # def visualizeField(app):
# #     dx = 80
# #     dy = 2
# #     color = 'black'
# #     for row in range(app.field.numRows):
# #         for col in range(app.field.numCols):
# #             if not almostEqual(app.field.fieldGrid[row][col], 0.0):
# #                 color = 'red'
# #             else:
# #                 color = 'black'
# #             drawLabel(f'{app.field.fieldGrid[row][col]}', dx, dy,size=7, fill=color)
# #             dx+=app.width/90
# #         dy+=app.height/60
# #         dx = 80

# runApp()