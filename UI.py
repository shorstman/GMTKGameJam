import pygame

class UIElement():
    def __init__(self, x, y, width, height, onClick):
        self.rect = pygame.Rect(x, y, width, height)
        self.onClick = onClick

    def clicked(self):
        return self.onClick

    def drawElement(self, window):
        #Draw the element
        pygame.draw.rect(window, (100, 100, 100), self.rect)
