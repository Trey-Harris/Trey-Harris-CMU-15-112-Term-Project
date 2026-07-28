from drawingAndProjectionin3D import *
import copy

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
        self.projectedFieldCords.extend(makeShape(500, 4, 0, 0, zDepth))