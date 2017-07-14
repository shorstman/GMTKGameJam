import pygame
#from pygame.local import *

class Player():
    def __init__(self, x, y):
        self.health = 100
        self.sneak = 0
        self.rect = pygame.Rect(x, y, 32, 32)
        self.dx = 0
        self.dy = 0

    def moveX(self, distance):
        self.dx = distance
        self.rect.x += self.dx
        if(self.rect.x > 900 - self.rect.width):
            self.rect.x = 900 - self.rect.width
        if(self.rect.x < 0):
            self.rect.x = 0

    def moveY(self, distance):
        self.dy = distance
        self.rect.y += self.dy
        if(self.rect.y > 600 - self.rect.height):
            self.rect.y = 600 - self.rect.height
        if(self.rect.y < 0):
            self.rect.y = 0

    def drawPlayer(self, window):
        pygame.draw.rect(window, (0, 0, 255), self.rect)

    def checkCollisions(self, collider):
        if self.rect.colliderect(collider.rect):
            if self.dx > 0:
                self.rect.right = collider.rect.left
            elif self.dx < 0:
                self.rect.left = collider.rect.right
            if self.dy > 0:
                self.rect.bottom = collider.rect.top
            elif self.dy < 0:
                self.rect.top = collider.rect.bottom

        self.dx = 0
        self.dy = 0
