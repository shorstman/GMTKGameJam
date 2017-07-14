import pygame

class Obstacle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def drawObstacle(self, window):
        pygame.draw.rect(window, (168, 168, 168), (self.x,self.y,self.width,self.height))
