import pygame
from Player import Player
from Obstacle import Obstacle
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

    player = Player(0, 0)
    obstacle = Obstacle(450, 300)

    x = 0
    y = 0
    moveX = 2
    moveY = 2
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.moveY(-3)
        if keys[pygame.K_DOWN]:
            player.moveY(3)
        player.checkCollisions(obstacle)
        if keys[pygame.K_LEFT]:
            player.moveX(-3)
        if keys[pygame.K_RIGHT]:
            player.moveX(3)
        player.checkCollisions(obstacle)
        window.blit(background, (0,0))
        player.drawPlayer(window)
        obstacle.drawObstacle(window)
        pygame.display.update()

if __name__ == "__main__": main()
