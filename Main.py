import pygame
from pygame.locals import *

NAME = "GMTKGameJam"

def main():
    pygame.init()
    window = pygame.display.set_mode((900, 600))
    pygame.display.set_caption(NAME)

    background = pygame.Surface(window.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    window.blit(background, (0,0))
    pygame.display.flip()

    x = 0
    y = 0
    moveX = 10
    moveY = 10
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        window.blit(background, (0,0))
        pygame.draw.rect(window, (0, 0, 255), (x,y,100,50))
        x += moveX
        y += moveY
        if(x > 800 or x < 0):
            moveX = moveX*-1
        if(y > 550 or y < 0):
            moveY = moveY*-1
        pygame.display.update()

if __name__ == "__main__": main()
