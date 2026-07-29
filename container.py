from drawingAndProjectionin3D import *
from cmu_graphics import *
import numpy

class Container:
    def __init__(self, leftX, rightX, bottomY, topY, closeZ, farZ, color='saddleBrown'):
        # These are already real world-space bounds (not screen coordinates),
        # same units as everything in field.py -- e.g. leftX/rightX somewhere
        # within +/- field.fieldLength/2, closeZ/farZ within +/- field.fieldDepth/2.
        self.containerLeftX   = leftX
        self.containerRightX  = rightX
        self.containerBottomY = bottomY
        self.containerTopY    = topY
        self.containerCloseZ  = closeZ
        self.containerFarZ    = farZ
        self.color = color

        self.points = []
        self.edges  = []
        self.faces  = []
        self.buildContainer()
        self.pointArray = numpy.array(self.points, dtype=float).T

        self.isConnected = False
        self.isFalling   = False

    def addPoint(self, x, y, z):
        self.points.append([x, y, z, 1])
        return len(self.points) - 1

    def addEdge(self, a, b, color, lineWidth=1):
        self.edges.append((a, b, color, lineWidth))

    def addFace(self, indices, color):
        self.faces.append((indices, color))

    # Builds a box from the six bounds passed into __init__, the same
    # near/far-z pattern field.py uses for the barrier. Raw world points --
    # nothing gets projected here. That happens every frame in draw().
    def buildContainer(self):
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

        for (indices, color) in self.faces:
            screen = []
            for i in indices:
                sx, sy = camera.perspective(xs[i], ys[i], max(depths[i], near), cx, cy)
                screen.append(sx)
                screen.append(sy)
            drawPolygon(*screen, fill=color, opacity=70)

    # --- Not touched by this fix; both still assume screen-space attributes
    # (containerCx/containerCy, containerHeight) that no longer exist now
    # that the container lives in world space. These will need to be
    # reworked -- e.g. connectContainer setting a world-space offset from
    # the drone instead -- whenever you get to wiring up pickup/drop.
    def connectContainer(self, drone):
        self.isConnected = True
        self.containerCx = drone.droneCx+20
        self.containerCy = drone.droneCy+20
        #REMOVE THE ARBITRARY +20

    def fallingContainer(self, app):
        if self.containerCy+5 <= app.height-self.containerHeight/2:
            self.containerCy += 5
        else:
            self.containerCy = app.height-self.containerHeight/2
            self.isFalling = False