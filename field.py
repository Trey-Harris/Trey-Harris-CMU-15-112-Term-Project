# CITATION: This entire file was written by Claude Opus. 
# I AM EXEMPTING THIS CODE!!!

# field.py
# ---------------------------------------------------------------------------
# 3D playing field + third-person chase camera for the AVR drone simulator.
#
# The arena is a long rectangular hall: a printed ground plane, a gabled cage
# frame overhead, and a solid barrier splitting the field in half.
# It is deliberately larger than one screenful -- you fly to see the rest.
# ---------------------------------------------------------------------------

import math
import numpy
from drawingAndProjectionin3D import *
from cmu_graphics import *


# # ===========================================================================
# # Small matrix helpers. These live here rather than in
# # drawingAndProjectionin3D.py so that file stays exactly as I wrote it.
# # ===========================================================================
# def makeXRotationMatrixMatrix(angle):
#     cosVal = math.cos(math.radians(angle))
#     sinVal = math.sin(math.radians(angle))
#     return numpy.array([[1, 0, 0, 0],
#                         [0, cosVal, -sinVal, 0],
#                         [0, sinVal, cosVal, 0],
#                         [0, 0, 0, 1]], dtype=float)


# def makeZRotationMatrix(angle):
#     cosVal = math.cos(math.radians(angle))
#     sinVal = math.sin(math.radians(angle))
#     return numpy.array([[cosVal, 0, sinVal, 0],
#                         [0, 1, 0, 0],
#                         [-sinVal, 0, cosVal, 0],
#                         [0, 0, 0, 1]], dtype=float)


# def makeTranslation(dx, dy, dz):
#     return numpy.array([[1, 0, 0, dx],
#                         [0, 1, 0, dy],
#                         [0, 0, 1, dz],
#                         [0, 0, 0, 1]], dtype=float)


# Trim a line to the window rectangle, returning None if it misses entirely.
# Without this, an edge clipped at the near plane projects to coordinates in
# the tens of thousands, which is both slow to rasterise and close to the
# coordinate limit Tk starts misbehaving at.
# Citation: this is the Liang-Barsky line clipping algorithm.
def clipToScreen(x1, y1, x2, y2, width, height):
    dx = x2 - x1
    dy = y2 - y1
    startT = 0.0
    endT   = 1.0
    for (p, q) in [(-dx, x1), (dx, width - x1), (-dy, y1), (dy, height - y1)]:
        if p == 0:
            if q < 0:
                return None          # parallel to this edge and outside it
        else:
            r = q / p
            if p < 0:
                if r > endT:
                    return None
                if r > startT:
                    startT = r
            else:
                if r < startT:
                    return None
                if r < endT:
                    endT = r
    return (x1 + startT*dx, y1 + startT*dy,
            x1 + endT*dx,   y1 + endT*dy)


# ===========================================================================
# ChaseCamera -- rides behind and above the drone, like a third-person game.
# ===========================================================================
# Trim a polygon to the part in front of the camera. Points are (x, y, depth)
# in camera space. Same idea as the line clipper above, but a polygon can gain
# or lose corners, so it is rebuilt edge by edge.
# Citation: this is the Sutherland-Hodgman polygon clipping algorithm.
def clipPolygonToNearPlane(points, near):
    clipped = []
    for i in range(len(points)):
        current  = points[i]
        previous = points[i-1]
        currentIn  = current[2]  >= near
        previousIn = previous[2] >= near
        if currentIn != previousIn:
            t = (near - previous[2]) / (current[2] - previous[2])
            clipped.append((previous[0] + t*(current[0] - previous[0]),
                            previous[1] + t*(current[1] - previous[1]),
                            near))
        if currentIn:
            clipped.append(current)
    return clipped


# Same algorithm again, this time trimming the flat screen-space polygon to
# the window so a face touching the near plane cannot produce coordinates in
# the tens of thousands.
def clipPolygonToScreen(points, width, height):
    margin = 40
    for (axis, limit, keepAbove) in [(0, -margin, True), (0, width + margin, False),
                                     (1, -margin, True), (1, height + margin, False)]:
        if len(points) < 3:
            return []
        clipped = []
        for i in range(len(points)):
            current  = points[i]
            previous = points[i-1]
            if keepAbove:
                currentIn, previousIn = current[axis] >= limit, previous[axis] >= limit
            else:
                currentIn, previousIn = current[axis] <= limit, previous[axis] <= limit
            if currentIn != previousIn:
                t = (limit - previous[axis]) / (current[axis] - previous[axis])
                clipped.append((previous[0] + t*(current[0] - previous[0]),
                                previous[1] + t*(current[1] - previous[1])))
            if currentIn:
                clipped.append(current)
        points = clipped
    return points


class ChaseCamera:
    def __init__(self):
        # Where the camera is looking. This trails the drone slightly instead
        # of snapping to it, which is what makes the motion feel weighty
        # rather than rigid.
        self.focusX = 0
        self.focusY = -120
        self.focusZ = 0
        self.hasTarget = False      # set on the first follow() call
        self.followSpeed = 0.18     # 0 = never catches up, 1 = welded on

        # The drone cannot yaw, so the camera never rotates -- it only slides
        # along behind. Change this once if you want a different fixed facing;
        # 0 looks down +z, which is the length of the hall.
        self.heading  = 0
        self.distance = 300         # how far behind the drone it sits
        self.height   = 130         # how far above it sits

        # Focal length sets the field of view. Bigger = more zoomed in.
        # 700 over a 1200px window is roughly an 81 degree horizontal FOV.
        self.focalLength  = 700
        self.nearPlane    = 12      # anything closer than this gets clipped
        self.drawDistance = 2600    # geometry past this is skipped entirely

    # The camera pitches down by exactly the angle that puts the drone in the
    # middle of the screen, so this is derived rather than stored.
    def getPitch(self):
        return math.degrees(math.atan2(self.height, self.distance))

    def getPosition(self):
        headingRadians = math.radians(self.heading)
        forwardX = math.sin(headingRadians)
        forwardZ = math.cos(headingRadians)
        return (self.focusX - forwardX*self.distance,
                self.focusY - self.height,      # y grows DOWNWARD, so minus is up
                self.focusZ - forwardZ*self.distance)

    def follow(self, targetX, targetY, targetZ):
        # First call of the app: jump straight there. Otherwise the camera
        # spends the opening second sliding over from wherever it started,
        # with the drone off the edge of the screen.
        if not self.hasTarget:
            self.focusX, self.focusY, self.focusZ = targetX, targetY, targetZ
            self.hasTarget = True
            return
        self.focusX += (targetX - self.focusX) * self.followSpeed
        self.focusY += (targetY - self.focusY) * self.followSpeed
        self.focusZ += (targetZ - self.focusZ) * self.followSpeed

    def viewMatrix(self):
        # Slide the world so the camera sits at the origin, then spin it so
        # the camera looks straight down +z.
        cameraX, cameraY, cameraZ = self.getPosition()
        matrix = numpy.matmul(makeXRotationMatrix(self.getPitch()),
                              makeZRotationMatrix(-self.heading))
        return numpy.matmul(matrix, translateMatrix(-cameraX, -cameraY, -cameraZ))

    # Every point in one numpy call instead of one call per point. pointArray
    # is shape (4, N); the result is camera space, where z is depth ahead.
    def toCameraSpace(self, pointArray):
        return numpy.matmul(self.viewMatrix(), pointArray)

    def perspective(self, x, y, depth, cx, cy):
        if depth < self.nearPlane:
            depth = self.nearPlane
        scale = self.focalLength / depth
        return x*scale + cx, y*scale + cy

    # Screen position of a single world point -- this is how the drone gets
    # placed, and it is why the drone stays centred.
    def worldToScreen(self, x, y, z, cx, cy):
        point = numpy.matmul(self.viewMatrix(), numpy.array([x, y, z, 1.0]))
        return self.perspective(point[0], point[1], point[2], cx, cy)


# ===========================================================================
# Field -- all the static world geometry.
# ===========================================================================
class Field:
    def __init__(self):
        # ---- Arena shell ---------------------------------------------------
        # x is the LONG axis and runs left-right across the view.
        # z is the SHORT axis and runs away from the camera.
        # The drone faces +z, so it looks at the long back edge, and it
        # explores by sliding left and right rather than flying up the hall.
        self.fieldLength = 2400      # x: -1200 .. 1200
        self.fieldDepth  = 1000      # z:  -500 .. 500
        self.eaveHeight  = 330       # where the side posts stop
        self.ridgeHeight = 470       # the peak of the gabled roof
        self.bayCount    = 10        # hoops spaced along the length

        # ---- Barrier splitting the field in half ---------------------------
        # It stands at x = 0 and runs the full depth, so it cuts the long
        # axis into two halves and sits off to one side of the drone.
        self.barrierHeight    = 260
        self.barrierThickness = 40
        # The wall is drawn as filled panels rather than one huge quad. Depth
        # sorting is per-shape, so one long face would sort as a single unit
        # and punch through things it should sit behind.
        self.barrierPanels    = 12

        # ---- Ground grid ----------------------------------------------------
        self.gridSpacing = 200
        # Pushed back in the sort order by more than one tile, so ground
        # always paints before the things resting on it.
        self.floorSortBias = 320

        # ---- Colours --------------------------------------------------------
        self.groundColor    = 'forestGreen'   # perimeter outline
        self.groundFill     = 'forestGreen'   # panel fill
        self.floorLight     = 'oliveDrab'        # alternating floor tiles
        self.floorDark      = 'darkOliveGreen'
        self.gridColor      = 'gray'             # tile borders = the grid
        self.frameColor     = 'dimGray'
        self.barrierColor   = 'lightSlateGray'    # outline
        self.barrierFill    = 'lightSlateGray'       # solid face

        self.points = []
        self.edges  = []        # (indexA, indexB, colour, lineWidth)
        self.faces  = []        # (list of point indices, fill colour)
        self.buildGround()
        self.buildCage()
        self.buildBarrier()

        # Transposed to (4, N) so the whole field transforms in one matmul.
        self.pointArray = numpy.array(self.points, dtype=float).T

    # -------------------------------------------------------------------
    # Geometry construction
    # -------------------------------------------------------------------
    def addPoint(self, x, y, z):
        self.points.append([x, y, z, 1])
        return len(self.points) - 1

    def addEdge(self, a, b, color, lineWidth=1):
        self.edges.append((a, b, color, lineWidth))

    def addFace(self, indices, color):
        self.faces.append((indices, color))

    def buildGround(self):
        halfLength = self.fieldLength / 2
        halfDepth  = self.fieldDepth / 2

        # Perimeter of the printed floor, drawn heavier than the grid.
        corners = [self.addPoint(-halfLength, 0, -halfDepth),
                   self.addPoint( halfLength, 0, -halfDepth),
                   self.addPoint( halfLength, 0,  halfDepth),
                   self.addPoint(-halfLength, 0,  halfDepth)]
        for i in range(4):
            self.addEdge(corners[i], corners[(i+1) % 4], self.groundColor, 3)

        # Filled in grid-sized panels rather than one huge quad, same reason
        # as the wall: a single panel would sort as one unit at its average
        # depth and could cover things nearer than its far edge.
        columns = int(self.fieldLength // self.gridSpacing)
        rows    = int(self.fieldDepth // self.gridSpacing)
        colEdges = [-halfLength + c*self.gridSpacing for c in range(columns + 1)]
        rowEdges = [-halfDepth + r*self.gridSpacing for r in range(rows + 1)]
        colEdges[0], colEdges[-1] = -halfLength, halfLength
        rowEdges[0], rowEdges[-1] = -halfDepth, halfDepth
        for c in range(len(colEdges) - 1):
            for r in range(len(rowEdges) - 1):
                x1, x2 = colEdges[c], colEdges[c+1]
                z1, z2 = rowEdges[r], rowEdges[r+1]
                self.addFace([self.addPoint(x1, 0, z1), self.addPoint(x2, 0, z1),
                              self.addPoint(x2, 0, z2), self.addPoint(x1, 0, z2)],
                             self.groundFill)

        # Grid lines on top of the fill, running both directions.
        for x in colEdges[1:-1]:
            self.addEdge(self.addPoint(x, 0, -halfDepth),
                         self.addPoint(x, 0,  halfDepth), self.gridColor, 1)
        for z in rowEdges[1:-1]:
            self.addEdge(self.addPoint(-halfLength, 0, z),
                         self.addPoint( halfLength, 0, z), self.gridColor, 1)

    def buildCage(self):
        # Gabled hoops spaced along the length, joined by three rails: one
        # down each eave and one along the ridge. The ridge runs the length
        # of the hall, so from the drone it recedes to left and right.
        halfLength = self.fieldLength / 2
        halfDepth  = self.fieldDepth / 2
        spacing    = self.fieldLength / self.bayCount

        nearEaves = []
        farEaves  = []
        ridges    = []
        for bay in range(self.bayCount + 1):
            x = -halfLength + bay*spacing
            nearBase = self.addPoint(x, 0, -halfDepth)
            nearEave = self.addPoint(x, -self.eaveHeight, -halfDepth)
            ridge    = self.addPoint(x, -self.ridgeHeight, 0)
            farEave  = self.addPoint(x, -self.eaveHeight, halfDepth)
            farBase  = self.addPoint(x, 0, halfDepth)

            self.addEdge(nearBase, nearEave, self.frameColor, 2)
            self.addEdge(nearEave, ridge,    self.frameColor, 2)
            self.addEdge(ridge,    farEave,  self.frameColor, 2)
            self.addEdge(farEave,  farBase,  self.frameColor, 2)

            nearEaves.append(nearEave)
            ridges.append(ridge)
            farEaves.append(farEave)

        for rail in (nearEaves, ridges, farEaves):
            for i in range(len(rail) - 1):
                self.addEdge(rail[i], rail[i+1], self.frameColor, 1)

    def buildBarrier(self):
        # A solid wall standing at x = 0, running the full depth of the field
        # and cutting the long axis in half. Built as a run of panels so the
        # painter's sort in draw() can order it correctly against everything
        # else in the scene.
        halfDepth     = self.fieldDepth / 2
        halfThickness = self.barrierThickness / 2
        topY          = -self.barrierHeight
        step          = self.fieldDepth / self.barrierPanels

        for panel in range(self.barrierPanels):
            nearZ = -halfDepth + panel*step
            farZ  = nearZ + step
            # The two long sides.
            for x in (-halfThickness, halfThickness):
                self.addFace([self.addPoint(x, topY, nearZ),
                              self.addPoint(x, topY, farZ),
                              self.addPoint(x, 0,    farZ),
                              self.addPoint(x, 0,    nearZ)], self.barrierFill)
            # The strip along the top.
            self.addFace([self.addPoint(-halfThickness, topY, nearZ),
                          self.addPoint( halfThickness, topY, nearZ),
                          self.addPoint( halfThickness, topY, farZ),
                          self.addPoint(-halfThickness, topY, farZ)], self.barrierFill)

        # Outline: the long top and base edges, plus the ends. This is what
        # keeps the silhouette crisp once the faces are filled in.
        for x in (-halfThickness, halfThickness):
            self.addEdge(self.addPoint(x, topY, -halfDepth),
                         self.addPoint(x, topY,  halfDepth), self.barrierColor, 2)
            self.addEdge(self.addPoint(x, 0, -halfDepth),
                         self.addPoint(x, 0,  halfDepth), self.barrierColor, 2)
        for z in (-halfDepth, halfDepth):
            corners = [self.addPoint(-halfThickness, topY, z),
                       self.addPoint( halfThickness, topY, z),
                       self.addPoint( halfThickness, 0,    z),
                       self.addPoint(-halfThickness, 0,    z)]
            for i in range(4):
                self.addEdge(corners[i], corners[(i+1) % 4], self.barrierColor, 2)

    # -------------------------------------------------------------------
    # Drawing
    # -------------------------------------------------------------------
    def draw(self, app, camera, cx, cy):
        cameraSpace = camera.toCameraSpace(self.pointArray)
        xs, ys, depths = cameraSpace[0], cameraSpace[1], cameraSpace[2]
        near = camera.nearPlane

        # Lines and filled faces go into one list together. Sorting them
        # separately would mean every face painted over every line, so a grid
        # line in front of the wall would vanish behind it.
        shapes = []      # (sortDepth, kind, data)

        for (a, b, color, lineWidth) in self.edges:
            depthA, depthB = depths[a], depths[b]
            if depthA < near and depthB < near:
                continue
            if min(depthA, depthB) > camera.drawDistance:
                continue
            ax, ay, az = xs[a], ys[a], depthA
            bx, by, bz = xs[b], ys[b], depthB
            if az < near:
                t = (near - az) / (bz - az)
                ax, ay, az = ax + t*(bx - ax), ay + t*(by - ay), near
            elif bz < near:
                t = (near - bz) / (az - bz)
                bx, by, bz = bx + t*(ax - bx), by + t*(ay - by), near
            shapes.append(((az + bz)/2, 'line',
                           (color, lineWidth, ax, ay, az, bx, by, bz)))

        for (indices, color) in self.faces:
            corners = []
            for i in indices:
                corners.append((xs[i], ys[i], depths[i]))
            if max(c[2] for c in corners) < near:
                continue
            if min(c[2] for c in corners) > camera.drawDistance:
                continue
            corners = clipPolygonToNearPlane(corners, near)
            if len(corners) < 3:
                continue
            average = sum(c[2] for c in corners) / len(corners)
            shapes.append((average, 'face', (color, corners)))

        # Painter's algorithm: farthest first so nearer shapes cover them.
        shapes.sort(key=lambda shape: shape[0], reverse=True)

        for (depth, kind, data) in shapes:
            if kind == 'line':
                (color, lineWidth, ax, ay, az, bx, by, bz) = data
                x1, y1 = camera.perspective(ax, ay, az, cx, cy)
                x2, y2 = camera.perspective(bx, by, bz, cx, cy)
                trimmed = clipToScreen(x1, y1, x2, y2, app.width, app.height)
                if trimmed == None:
                    continue
                drawLine(trimmed[0], trimmed[1], trimmed[2], trimmed[3],
                         fill=color, lineWidth=lineWidth,
                         opacity=self.depthOpacity(depth, camera))
            else:
                (color, corners) = data
                screen = []
                for c in corners:
                    screen.append(camera.perspective(c[0], c[1], c[2], cx, cy))
                screen = clipPolygonToScreen(screen, app.width, app.height)
                if len(screen) < 3:
                    continue
                flattened = []
                for (px, py) in screen:
                    flattened.append(px)
                    flattened.append(py)
                # Faces fade less than lines so the wall stays readable as a
                # solid surface all the way to the far end.
                drawPolygon(*flattened, fill=color,
                            opacity=self.depthOpacity(depth, camera, 58))

    def depthOpacity(self, depth, camera, faintest=22):
        # Distant geometry fades out, so the far end of the hall reads as far
        # away instead of as clutter.
        howFar = depth / camera.drawDistance
        if howFar < 0:
            howFar = 0
        if howFar > 1:
            howFar = 1
        return int(faintest + (100 - faintest)*(1 - howFar))

    # -------------------------------------------------------------------
    # Collision helpers
    # -------------------------------------------------------------------
    # The roof is gabled, so headroom depends on how far out from the ridge
    # you are: highest over the middle, lowest at the eaves. Returns the y of
    # the roof (negative, because y grows downward).
    def ceilingAt(self, z):
        howFarOut = abs(z) / (self.fieldDepth/2)
        if howFarOut > 1:
            howFarOut = 1
        return -(self.ridgeHeight +
                 (self.eaveHeight - self.ridgeHeight) * howFarOut)

    def isInBounds(self, x, y, z, margin=0):
        return (abs(x) <= self.fieldLength/2 - margin and
                abs(z) <= self.fieldDepth/2 - margin and
                self.ceilingAt(z) + margin <= y <= -margin)

    def hitsBarrier(self, x, y, z, margin=0):
        if abs(x) > self.barrierThickness/2 + margin:
            return False
        if abs(z) > self.fieldDepth/2 + margin:
            return False
        return y > -self.barrierHeight - margin

    # Where to spawn: in the left half, facing the long back edge, close
    # enough to the barrier that it frames up on the right of the view.
    def startPosition(self):
        return (-self.fieldLength/6, -150, 0)

    def clampToArena(self, x, y, z, margin=0):
        # Cheap way to keep the drone inside: shove it back to the wall it
        # tried to leave through. Swap for a real bounce when you have time.
        limitX = self.fieldLength/2 - margin
        limitZ = self.fieldDepth/2 - margin
        x = min(limitX, max(-limitX, x))
        z = min(limitZ, max(-limitZ, z))
        y = min(-margin, max(self.ceilingAt(z) + margin, y))
        return x, y, z