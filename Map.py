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
    def __init__(self, sw, sh, viewXPadding, viewYPadding):
        self.origin = [sw/2,sh/2]
        self.sw = sw
        self.sh = sh
        self.viewXPadding = viewXPadding
        self.viewYPadding = viewYPadding
        self.setBounds()

        # GenerateMap()
        self.localMap = []
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
        playerIn = True
        if ((x > self.xMax) or (y > self.yMax)):  # Detect if the player is out of bounds and reset the origin if they are
            self.origin[0] = x-(self.xMax - self.xMin)/2
            playerIn = False
        elif ((x < self.xMin) or (y < self.yMin)):
            self.origin[0] = x+(self.xMax - self.xMin)/2
            playerIn  = False
        if(y > self.yMax):
            self.origin[1] = y-(self.yMax - self.yMin)/2
            playerIn = False
        elif(y < self.yMin):
            self.origin[1] = y+(self.yMax - self.yMin)/2
            playerIn = False
        self.setBounds()
        return playerIn

    def getLocalMapSubset(self):
        self.mapObjects = []
        localXMap = []
        for i in range(0, len(self.map)): # Iterate through all map values
            if((self.map[i][0] > self.xMin - self.viewXPadding) or (self.map[i][0] < self.xMax + self.viewXPadding)): # If any given map value is within the user's FOV X bounds;
                localXMap.append(self.map[i]) # Add that value to localXMap
        for i in range(0, len(localXMap)): # Iterate through all localXMap values
            if((localXMap[i][1] > self.yMin - self.viewYPadding or localXMap[i][1] < self.yMax + self.viewXPadding)): # If any given localXMap value is within the user's FOV Y bounds;
                self.localMap.append(localXMap[i]) # Add that value to localMap
                self.mapObjects.append(Obstacle(self.localMap[i][0],self.localMap[i][1],self.localMap[i][2],self.localMap[i][3],self.localMap[i][4])) # Obstacle(x,y,w,h)
        print(str(self.mapObjects))

    def setBounds(self):
        self.xMax = self.origin[0] + self.sw/2 - self.viewXPadding
        self.yMax = self.origin[1] + self.sh/2 - self.viewYPadding
        self.xMin = self.origin[0] - self.sw/2 + self.viewXPadding
        self.yMin = self.origin[1] - self.sh/2 + self.viewYPadding

    def getObjectList(self):
        self.getLocalMapSubset()
        return self.mapObjects

    def debug(text,level):
        if(level >= debugLevel):
            print(text)
