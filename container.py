class Container:
    def __init__(self, x, y):
        self.containerCx = x
        self.containerCy = y   
        #Don't forget x when I get it
        self.containerHeight = 25
        self.containerWidth = 70
        #self.containerDepth = SOMETHING
        self.isConnected = False

    def connectContainer(self, drone):
        self.isConnected = True
        self.containerCx = drone.droneCx
        self.containerCy = drone.droneCy

        # drone.cubeSize
        # drone.droneCx
        # drone.droneCy

    

