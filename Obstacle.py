import pygame

class Obstacle():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def drawObstacle(self, window):
        pygame.draw.rect(window, (168, 168, 168), self.rect)
