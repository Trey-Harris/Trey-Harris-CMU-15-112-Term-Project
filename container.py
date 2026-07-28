class Container:
    def __init__(self, x, y):
        self.containerCx = x
        self.containerCy = y   
        #Don't forget x when I get it
        self.containerHeight = 25
        self.containerWidth = 70
        #self.containerDepth = SOMETHING
        self.isConnected = False
        self.isFalling = False

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
        

