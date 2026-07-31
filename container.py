from drawingAndProjectionin3D import *
from cmu_graphics import *
import numpy
import copy

class Container:
    def __init__(self, app, leftX, rightX, bottomY, topY, closeZ, farZ, name):
        self.containerLeftX = leftX
        self.containerRightX = rightX
        self.containerBottomY = bottomY
        self.containerTopY = topY
        self.containerCloseZ = closeZ
        self.containerFarZ = farZ
        self.containerWidth = abs(self.containerLeftX - self.containerRightX)
        self.containerHeight = abs(self.containerBottomY - self.containerTopY)
        self.color = 'fireBrick'

        self.fallHeight = 0
        self.isBroken = False
        self.isFilled = False
        self.stepPlacedOnSquare = None
        self.name = name

        self.points = []
        self.edges  = []
        self.faces  = []
        self.buildContainer()

        self.isConnected = False
        self.isFalling   = False

    def __repr__(self):
        return self.name

    def connectContainer(self, app):
        self.isConnected = True
        self.containerLeftX = app.avr.droneX - self.containerWidth/2
        self.containerRightX = app.avr.droneX + self.containerWidth/2
        self.containerTopY = app.avr.droneY-self.containerHeight
        self.containerBottomY = self.containerTopY + self.containerHeight
        self.containerCloseZ = app.avr.droneZ-125   #Arbitrary translation to help with depth perception when connected.
        self.containerFarZ = app.avr.droneZ-100

        self.connectedProjection = []
        self.connectedProjection.extend(makeShape(self.containerWidth*(2**0.5), 4, 0, 0, 0))
        self.connectedProjection.extend(makeShape(self.containerWidth*(2**0.5), 4, 0, 0, -25))
        self.connectedProjection = project(copy.deepcopy(self.connectedProjection), app.avr.pitch, app.avr.roll)
        #Call different method here
        #self.connectedBuildContainer()
        #self.buildContainer()

    def fallingContainer(self, app):
        #The signs are backwards here b/c Claude wrote the field horribly. It has
        #a higher altitude being a more negative number :(
        if self.containerBottomY-5 <= 0:
            self.containerBottomY += 5
            self.containerTopY += 5
            self.buildContainer()
        else:
            self.isFalling = False
            self.containerBottomY = 0
            self.containerTopY = -self.containerHeight
            if self.fallHeight <= -150:
                self.isBroken = True
                app.messages = app.messages +'\n' + f'{self.name} fell from a high place'
            else:
                self.buildContainer() #Transfers back to Claude projection logic b/c
        #container is now a part of the field

                #These ifs only adds score for containers on the correct side
                if app.activeSide == 'left' and self not in app.containersWithPoints:
                    print('hi')
                    if self.leftScoreDropoff(app, -700, -800, 230, 260) != 0:
                        app.points += 3*app.timer
                        app.successfulDrops += 1
                        app.containersWithPoints.append(self)
                        return None
                    if self.leftScoreDropoff(app, -300, -400, 230, 260) != 0:
                        app.points += 3*app.timer
                        app.successfulDrops += 1
                        app.containersWithPoints.append(self)
                        return None
                    if self.leftScoreDropoff(app, -400, -500, 30, 60) != 0:
                        app.points += 3*app.timer
                        app.successfulDrops += 1
                        app.containersWithPoints.append(self)
                        return None
                    
                elif app.activeSide == 'right' and self not in app.containersWithPoints:
                    if self.rightScoreDropoff(app, 700, 800, 230, 260) != 0:
                        app.points += 3*app.timer
                        app.successfulDrops += 1
                        app.containersWithPoints.append(self)
                        return None
                    if self.rightScoreDropoff(app, 300, 400, 230, 260) != 0:
                        app.points += 3*app.timer
                        app.successfulDrops += 1
                        app.containersWithPoints.append(self)
                        return None
                    if self.rightScoreDropoff(app, 400, 500, 30, 60) != 0:
                        app.points += 3*app.timer
                        app.successfulDrops += 1
                        app.containersWithPoints.append(self)
                        return None


    def leftScoreDropoff(self, app, zoneLeft, zoneRight, zoneFar, zoneClose):
        if self.containerRightX < 0:
            if ((self.containerRightX>=zoneLeft) and ((self.containerFarZ>=zoneClose)
                or (self.containerCloseZ<=zoneFar))):
                return 3

            if ((self.containerLeftX<=zoneRight) and ((self.containerFarZ>=zoneClose)
                        or (self.containerCloseZ<=zoneFar))):
                return 3

    def rightScoreDropoff(self, app, zoneLeft, zoneRight, zoneFar, zoneClose):
        if self.containerLeftX > 0:
            if ((self.containerRightX>=zoneLeft) and ((self.containerFarZ>=zoneClose)
                or (self.containerCloseZ<=zoneFar))):
                app.points += 3

            if ((self.containerLeftX<=zoneRight) and ((self.containerFarZ>=zoneClose)
                        or (self.containerCloseZ<=zoneFar))):
                app.points += 3
                


###REST OF THIS FILE IS EXEMPTED: This is Claude implementing the same draw logic
#from the field to the containers they just have to appear in this file to so that
#method types work.
    def addPoint(self, x, y, z):
        self.points.append([x, y, z, 1])
        return len(self.points) - 1

    def addEdge(self, a, b, color, lineWidth=1):
        self.edges.append((a, b, color, lineWidth))

    def addFace(self, indices, color):
        self.faces.append((indices, color))

    #This is when the container behaves as part of the field
    def buildContainer(self):
        self.points = []
        self.edges  = []
        self.faces  = []
        leftX, rightX   = self.containerLeftX, self.containerRightX
        topY, bottomY   = self.containerTopY, self.containerBottomY
        closeZ, farZ    = self.containerCloseZ, self.containerFarZ

        corners = []
        for z in (closeZ, farZ):
            face = [self.addPoint(leftX,  topY,    z),
                    self.addPoint(rightX, topY,    z),
                    self.addPoint(rightX, bottomY, z),
                    self.addPoint(leftX,  bottomY, z)]
            for i in range(4):
                self.addEdge(face[i], face[(i+1) % 4], self.color, 2)
            corners.append(face)
        for i in range(4):
            self.addEdge(corners[0][i], corners[1][i], self.color, 2)

        self.addFace(corners[0], self.color)
        self.addFace(corners[1], self.color)
        self.pointArray = numpy.array(self.points, dtype=float).T

    # Called by Field.draw() for every container in field.containers.
    # Same camera, same projection math field.py uses for its own geometry.
    def draw(self, app, camera, cx, cy):
        cameraSpace = camera.toCameraSpace(self.pointArray)
        xs, ys, depths = cameraSpace[0], cameraSpace[1], cameraSpace[2]
        near = camera.nearPlane

        for (a, b, color, lineWidth) in self.edges:
            depthA, depthB = depths[a], depths[b]
            if depthA < near and depthB < near:
                continue
            x1, y1 = camera.perspective(xs[a], ys[a], max(depthA, near), cx, cy)
            x2, y2 = camera.perspective(xs[b], ys[b], max(depthB, near), cx, cy)
            drawLine(x1, y1, x2, y2, fill=color, lineWidth=lineWidth)

        if self.isFilled:
            for (indices, color) in self.faces:
                screen = []
                for i in indices:
                    sx, sy = camera.perspective(xs[i], ys[i], max(depths[i], near), cx, cy)
                    screen.append(sx)
                    screen.append(sy)
                drawPolygon(*screen, fill=color, opacity=70)