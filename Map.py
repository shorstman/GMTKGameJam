"""
As the player moves, we aren't really drawing the map around them, but rather a series of objects on a background
So what we really want is to determine the relative coordinates of all objects and draw them at those relative coordinates IFF the relative coordinates
are contained within the screen area, determined by (playerX-screenWidth/2,playerY+screenHeight/2),(playerX+screenWidth/2,playerY-screenHeight/2)
    These are the top left and right bottom corners respectively.

Actually I want to make it so that the player can move around a preset area, but when they move outside of that area, it shifts the map.
The area will be predefined by the above formula minus some constant so that we have a border

So

if player.x > sc

"""
import pygame
from Obstacle import Obstacle

debugLevel = 1

class Map():
    def __init__(self, sw, sh):
        self.origin = [sw/2,sh/2]
        self.sw = sw
        self.sh = sh
        self.setBounds()


        # GenerateMap()
        self.localMap = []
        self.localXMap = []
        self.map = [[0,0,10,10,40],[100,200,100,100,40],[20,20,10,10,40],[300,300,100,100,40]]
        self.mapObjects = []
        # Map block types:
            # 0: Wall
            # 1: Hurty obstacle
            # 2: Portal In
            # 3: Portal Out

    def inBounds(self, x, y):
        """
        Returns 0 if the player is in bounds. Returns 1 if the player is out of bounds and the map has to be redrawn.
        """
        if ((x > self.xMax) or (y > self.yMax)):  # Detect if the player is out of bounds and reset the origin if they are
            self.origin = [(x-self.sw/2),(y-self.sh/2)]
            return 1
        elif ((x < self.xMin) or (y < self.yMin)):
            self.origin = [(x+self.sw/2),(y+self.sh/2)]
            return 1
        else:
            return 0

    def getLocalMapSubset(self):
        for i in range(0, len(self.map)): # Iterate through all map values
            if((self.map[i][0] > self.xMin) or (self.map[i][0] < self.xMax)): # If any given map value is within the user's FOV X bounds;
                self.localXMap.append(self.map[i]) # Add that value to localXMap
        for i in range(0, len(self.localXMap)): # Iterate through all localXMap values
            if((self.localXMap[i][1] > self.yMin or self.localXMap[i][1] < self.yMax)): # If any given localXMap value is within the user's FOV Y bounds;
                self.localMap.append(self.localXMap[i]) # Add that value to localMap
                self.mapObjects.append(Obstacle(self.localMap[i][0],self.localMap[i][1],self.localMap[i][2],self.localMap[i][3],self.localMap[i][4])) # Obstacle(x,y,w,h)
        print(str(self.mapObjects))

    def setBounds(self):
        self.xMax = self.origin[0] + self.sw/2
        self.yMax = self.origin[1] + self.sh/2
        self.xMin = self.origin[0] - self.sw/2
        self.yMin = self.origin[1] - self.sw/2

    def getObjectList(self):
        self.getLocalMapSubset()
        return self.mapObjects

    def debug(text,level):
        if(level >= debugLevel):
            print(text)

    def subtract():
        print(4 - 2)
