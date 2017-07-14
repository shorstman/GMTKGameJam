import pygame
#from pygame.local import *

class Player():
    def __init__(self):
        self.health = 100
        self.sneak = 0
        self.x = 0
        self.y = 0
        self.width = 50
        self.height = 100

    def moveX(self, distance):
        self.x += distance
        if(self.x > 900 - self.width):
            self.x = 900 - self.width
        if(self.x < 0):
            self.x = 0

    def moveY(self, distance):
        self.y += distance
        if(self.y > 600 - self.height):
            self.y = 600 - self.height
        if(self.y < 0):
            self.y = 0

    def drawPlayer(self, window):
        pygame.draw.rect(window, (0, 0, 255), (self.x,self.y,self.width,self.height))
