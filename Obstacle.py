import pygame

class Obstacle():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)

    def drawObstacle(self, window):
        pygame.draw.rect(window, (168, 168, 168), self.rect)
