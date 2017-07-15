import pygame
from Player import Player
from Obstacle import Obstacle
from pygame.locals import *

NAME = "GMTKGameJam"

def main():
    #Initialize the window
    pygame.init()
    window = pygame.display.set_mode((928, 600))
    pygame.display.set_caption(NAME)

    #Create the background object
    background = pygame.Surface(window.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #Draw the background
    window.blit(background, (0,0))
    pygame.display.flip()

    #Create the player object
    player = Player(0, 0)
    obstacles = []
    for x in range(0, 29):
        obstacles.append(Obstacle(x*50, 250, 32, 32))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        keys = pygame.key.get_pressed()
        #Movement
        if keys[pygame.K_UP]:
            player.moveY(-3)
        if keys[pygame.K_DOWN]:
            player.moveY(3)
        player.checkCollisions(obstacle)
        if keys[pygame.K_LEFT]:
            player.moveX(-3)
        if keys[pygame.K_RIGHT]:
            player.moveX(3)

        #Check collisions
        player.checkCollisions(obstacle)

        #Refresh the background
        window.blit(background, (0,0))

        #Draw the player
        player.drawPlayer(window)
        obstacle.drawObstacle(window)
        pygame.display.update()

if __name__ == "__main__": main()
