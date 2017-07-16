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
from Obstacle import *
from GenerateMap import GenerateMap

debugLevel = 1

class Map():
    def __init__(self, sw, sh, viewXPadding, viewYPadding):
        self.x = 0
        self.y = 0
        self.sw = sw
        self.sh = sh
        self.viewXPadding = viewXPadding
        self.viewYPadding = viewYPadding
        self.boolMap = GenerateMap(64, 128, 46, 3, 4, 2)
        self.localMap = []
        self.map = self.boolMap.map
        self.mapObjects = []
        self.setBounds()
        self.enemies = self.boolMap.enemies

    def inBounds(self, player):
        """
        Returns 0 if the player is in bounds. Returns 1 if the player is out of bounds and the map has to be redrawn.
        """
        playerIn = True
        if (player.rect.x > self.xMax - self.x):  # Detect if the player is out of bounds and reset the origin if they are
            self.x = player.worldX - 700#self.viewXPadding - (self.xMax - self.xMin)
            playerIn = False
        if (player.rect.x < self.xMin - self.x):
            self.x = player.worldX - self.viewXPadding
            playerIn  = False
        if(player.rect.y > self.yMax - self.y):
            self.y = player.worldY - 500
            playerIn = False
        if(player.rect.y < self.yMin - self.y):
            self.y = player.worldY - self.viewYPadding
            playerIn = False
        return playerIn

    def getLocalMapSubset(self):
        for obstacle in self.mapObjects:
            del obstacle
        self.mapObjects = []
        localXMap = []
        self.localMap = []
        for i in range(0, len(self.map)): # Iterate through all map values
            if((self.map[i].worldX > self.x - 64) and (self.map[i].worldX < self.x + self.sw + 64)): # If any given map value is within the user's FOV X bounds;
                localXMap.append(self.map[i]) # Add that value to localXMap
        for i in range(0, len(localXMap)): # Iterate through all localXMap values
            if((localXMap[i].worldY > self.y - 64 and localXMap[i].worldY < self.y + self.sh + 64)): # If any given localXMap value is within the user's FOV Y bounds;
                self.localMap.append(localXMap[i]) # Add that value to localMap
        for i in range(0, len(self.localMap)):
            self.mapObjects.append(self.localMap[i]) # Obstacle(x,y,w,h)

    def setBounds(self):
        self.xMax = self.x + self.sw - self.viewXPadding
        self.xMin = self.x + self.viewXPadding
        self.yMax = self.y + self.sh - self.viewYPadding
        self.yMin = self.y + self.viewYPadding
        for obstacle in self.map:
            obstacle.updateRectangle(self.x, self.y)

    def getObjectList(self):
        self.getLocalMapSubset()
        return self.mapObjects
