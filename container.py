from drawingAndProjectionin3D import *
import copy

class Container:
    def __init__(self, app, leftX, rightX, bottomY, topY, closeZ, farZ):
        self.containerLeftX = leftX
        self.containerRightX = rightX
        self.containerBottomY = bottomY
        self.containerTopY = topY
        self.containerCloseZ = closeZ
        self.containerFarZ = farZ
        self.projectedContainerCords = []
        self.projectedContainerCords.extend(self.makeContainer(app, self.containerCloseZ))
        self.projectedContainerCords.extend(self.makeContainer(app, self.containerFarZ))
        self.projectedContainerCords = project(copy.deepcopy(self.projectedContainerCords), 20, 0)
        self.isConnected = False
        self.isFalling = False

#Idea to loop over a tuple of zClose and zFar was inspired by Claude's
#implementation in the exepmpted field class.
    def makeContainer(self, app, zDepth):
        return makeShape(50, 4, app.width/4, app.width/4, zDepth)

        # points = []
        # points.append([self.containerLeftX, self.containerTopY, zDepth, 1])
        # points.append([self.containerLeftX, self.containerBottomY, zDepth, 1])
        # points.append([self.containerRightX, self.containerTopY, zDepth, 1])
        # points.append([self.containerRightX, self.containerBottomY, zDepth, 1])
        # return points

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



    # #CLAUDE FUNCTIONS THAT I MIGHT NEED TO USE TO DRAW THE CONTAINERS:
    #  def addBox(self, leftX, rightX, topY, bottomY, nearZ, farZ, color, lineWidth=1):
    #         corners = []
    #         for z in (nearZ, farZ):
    #             face = [self.addPoint(leftX,  topY,    z),
    #                     self.addPoint(rightX, topY,    z),
    #                     self.addPoint(rightX, bottomY, z),
    #                     self.addPoint(leftX,  bottomY, z)]
    #             for i in range(4):
    #                 self.addEdge(face[i], face[(i+1) % 4], color, lineWidth)
    #             corners.append(face)
    #         for i in range(4):
    #             self.addEdge(corners[0][i], corners[1][i], color, lineWidth)
    # def buildStructures(self):
    #     # Small buildings scattered across both halves. These matter more than
    #     # they look like they should -- without objects at known sizes there
    #     # is nothing to judge speed or distance against.
    #     placements = [(-960, -260, 90, 80), (-620,  180, 80, 70),
    #                   (-300, -120, 100, 90), ( 330,  240, 85, 75),
    #                   ( 700, -300, 95, 85),  ( 1010, 100, 80, 70)]
    #     for (x, z, size, tall) in placements:
    #         self.addBox(x - size/2, x + size/2, -tall, 0,
    #                     z - size/2, z + size/2, self.structureColor, 2)
    # def addPoint(self, x, y, z):
    #     self.points.append([x, y, z, 1])
    #     return len(self.points) - 1


    # def addEdge(self, a, b, color, lineWidth=1):
    #     self.edges.append((a, b, color, lineWidth))