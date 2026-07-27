##############################################
### THIS CODE IS NOW IMPLEMENTED IN 3DProjectionTesting.py
##############################################


from cmu_graphics import *
import math

def onAppStart(app):
    app.width = 1200
    app.height = 600
    app.octCords = []
    app.octRadius = 120
    prepOctagon(app)

def prepOctagon(app):
    angle = 22.5    #top left vertex if think of like a stop sign
    while angle<360:
        xDisp = app.octRadius*math.cos(math.radians(angle))
        yDisp = app.octRadius*math.sin(math.radians(angle))
        app.octCords.append((app.width/2+xDisp, app.height/2+yDisp))
        angle += 45     #degrees each vertex is from neighboring vertex
    print(app.octCords)
def redrawAll(app):
    for x,y in app.octCords:
        drawCircle(x, y, 10)

    # drawRegularPolygon(200,200,100,12,border='black',fill=None)
    # drawPolygon(100,100,200,100,200,200)
    #try to unpack list with call(*points), gets each element as an argument.

runApp()