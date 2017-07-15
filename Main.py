from Player import Player
from Obstacle import Obstacle
from Enemy import Enemy
import pygame
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

    enemies = []
    for x in range(1, 3):
        enemies.append(Enemy(x*100, 0))
    obstacles = []
    for x in range(0, 29):
        obstacles.append(Obstacle(x*32, 250, 32, 32))

    time = 0
    while True:
        time += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        keys = pygame.key.get_pressed()
        #Movement
        if keys[pygame.K_LEFT]:
            player.orientation = -1
            player.moveX(-3)
        if keys[pygame.K_RIGHT]:
            player.orientation = 1
            player.moveX(3)

        #Check collisions
        player.checkCollisions(obstacles)
        if keys[pygame.K_UP]:
            if(player.onGround):
                player.moveY(50, time)
        player.moveY(0, time)
        player.checkCollisions(obstacles)

        if keys[pygame.K_z]:
            for enemy in enemies:
                if(enemy.rect.colliderect(pygame.Rect(player.rect.x+(19*player.orientation), player.rect.y, 19, 32))):
                    player.smallAttack(enemy)
                    enemy.health

        if(player.onGround):
            time = 0

        #Refresh the background
        window.blit(background, (0,0))

        #Draw the player
        player.drawPlayer(window)

        for enemy in enemies:
            enemy.drawEnemy(window)
            enemy.moveY(0, time)
            enemy.checkCollisions(obstacles)

        #Draw the obstacles
        for obstacle in obstacles:
            obstacle.drawObstacle(window)

        pygame.display.update()

if __name__ == "__main__": main()
