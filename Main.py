from Player import Player
from Obstacle import Obstacle
from Enemy import *
import pygame
from pygame.locals import *
import time
import math

NAME = "GMTKGameJam"

def start():
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

    #Create enemies
    enemies = []
    for x in range(1, 2):
        enemies.append(Chomper(x*300, 0))

    #Create obstacles
    obstacles = []
    for x in range(0, 20):
        obstacles.append(Obstacle(x*32, 250, 32, 32))

    main()


def main():
    while True:
        player.time += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.KEYDOWN:
                #Check if the z key is pressed
                if event.key == pygame.K_z:
                    for enemy in enemies:
                        #If an enemy is in range call smallAttack from the player
                        if(player.orientation == 1):
                            attack = pygame.Rect(player.rect.x+player.rect.width, player.rect.y, 38, player.rect.height)
                        else:
                            attack = pygame.Rect(player.rect.x - 38, player.rect.y, 38, 32)
                        if(enemy.rect.colliderect(attack)):
                            enemy.damage(20)
                #Check if the left shift is pressed
                if event.key == pygame.K_LSHIFT:
                    #Toggle on/off vulnerable ability
                    player.vulnerable = not player.vulnerable
                    #Start a timer
                    startTime = time.time()

                    #If the player is coming out of vulernable ability, save the vulnerability multiplier for use in the decay equation
                    if(not player.vulnerable):
                        vulnerabilityDecay = player.vulnerability

                #If the x key is pressed
                if event.key == pygame.K_x:
                    if(player.orientation == 1):
                        #Create a very large attack rectangle
                        attack = pygame.Rect(player.rect.x + player.rect.width, player.rect.y, 2000, player.rect.height)
                        #Check for obstacles colliding with the attack and trim it as needed
                        for obstacle in obstacles:
                            if(attack.colliderect(obstacle.rect)):
                                attack.width = obstacle.rect.x - attack.x
                    else:
                        #This is the same as above but slightly different because they're in different directions
                        attack = pygame.Rect(player.rect.x - 2000, player.rect.y, 2000, player.rect.height)
                        for obstacle in obstacles:
                            if(attack.colliderect(obstacle.rect)):
                                    difference = attack.x - obstacle.rect.x
                                    attack.x = obstacl.rect.x
                                    attack.width -= difference

        keys = pygame.key.get_pressed()
        #Movement left/right
        if keys[pygame.K_LEFT]:
            player.orientation = -1
            player.moveX(-1)
        if keys[pygame.K_RIGHT]:
            player.orientation = 1
            player.moveX(1)

        #Check collisions on x axis
        player.checkObstacleCollisions(obstacles)

        #Jump
        if keys[pygame.K_UP]:
            if(player.onGround):
                player.jumping = 2
                player.moveY(player.jumping)
        player.moveY(player.jumping)

        #Check collisions on y axis
        player.checkObstacleCollisions(obstacles)

        #If the player is on the ground reset the jump and time values
        if(player.onGround):
            player.time = 0
            player.jumping = 0

        #Do vulnerability increase/decay calculations
        if(player.vulnerable):
            currentTime = int(time.time() - startTime)
            player.vulnerability = 0.1*currentTime + 1
        else:
            if(player.vulnerability > 1):
                currentTime = int(time.time() - startTime)
                player.vulnerability = -0.05*currentTime + vulnerabilityDecay


        #Refresh the background
        window.blit(background, (0,0))

        #Draw the player
        player.drawPlayer(window)

        for enemy in enemies:
            #Check if player is on the ground for jump attack
            if(not player.onGround):
                #Create rectangle to collide with enemy
                attack = pygame.Rect(player.rect.x, player.rect.y + player.rect.height,
                                    player.rect.width, 16)
                #If rectangle collides, do damage
                if(enemy.rect.colliderect(attack)):
                    enemy.damage(30)

            #If the enemy has zero health, remove it
            if(enemy.health <= 0):
                enemy.kill()
            else:
                #Draw enemy and to kinatmics calculations/check for collisions
                enemy.time += 1
                enemy.drawEnemy(window)
                enemy.moveY(0)
                enemy.checkObstacleCollisions(obstacles)
                if(enemy.onGround):
                    enemy.time = 0

                #Get the distance between the enemy and the player
                playerDist = math.sqrt(math.pow(player.rect.x - enemy.rect.x, 2)
                                        + math.pow(player.rect.y - enemy.rect.y, 2))
                #If the player is within aggro distance of the enemy, run aggro action
                if(playerDist <= enemy.aggrodist):
                    enemy.aggroAction(player)

        #Draw the obstacles
        for obstacle in obstacles:
            obstacle.drawObstacle(window)

        #Update the display
        pygame.display.update()

if __name__ == "__main__": start()
