import pygame

class UIElement():
    def __init__(self, x, y, width, height, onClick, text):
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 16)
        self.rect = pygame.Rect(x, y, width, height)
        self.onClick = onClick
        self.text = text

    def clicked(self):
        return self.onClick

    def drawElement(self, window):
        #Draw the element
        pygame.draw.rect(window, (100, 100, 100), self.rect)
        textArea = self.font.render(self.text, False, (0, 0, 0))
        window.blit(textArea,(self.rect.x,self.rect.y))
        #print("Width: " +str(textArea.get_width()) +", Height: " +str(textArea.get_height()))
