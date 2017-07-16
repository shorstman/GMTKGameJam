from Player import Player
from Obstacle import Obstacle
from Enemy import *
from UI import UIElement
from Map import Map
import pygame
from pygame.locals import *
import time
import math
import os
from _thread import start_new_thread

NAME = "GMTKGameJam"
dirSymbol = "/"
screenWidth = 900
screenHeight = 600
viewXPadding = 200
viewYPadding = 100

def loadPlayerSprites():
    #This loads all the sprite images for the player
    os.chdir("sprites" +dirSymbol +"Player_Sprites")
    sprites = {}
    sprites["idle"] = [pygame.image.load("Base_Sprites" +dirSymbol +"PL_BaseF.png")]
    for sprite in os.listdir("Idle_Hover"):
        sprites["idle"].append(pygame.image.load("Idle_Hover" +dirSymbol +sprite))
    sprites["left"] = [pygame.image.load("Base_Sprites" +dirSymbol +"PL_BaseL.png")]
    for sprite in os.listdir("Hover_Left"):
        sprites["left"].append(pygame.image.load("Hover_Left" +dirSymbol +sprite))
    sprites["right"] = [pygame.image.load("Base_Sprites" +dirSymbol +"PL_BaseR.png")]
    for sprite in os.listdir("Hover_Right"):
        sprites["right"].append(pygame.image.load("Hover_Right" +dirSymbol + sprite))
    sprites["leftSmallAttack"] = []
    sprites["rightSmallAttack"] = []
    for sprite in range(1, len(os.listdir("Attack_Basic")) + 1):
        sprites["rightSmallAttack"].append(pygame.image.load("Attack_Basic" +dirSymbol + "Atk_Base" + str(sprite) + ".png"))
        sprites["leftSmallAttack"].append(pygame.transform.flip(pygame.image.load("Attack_Basic" +dirSymbol + "Atk_Base" + str(sprite) + ".png"), True, False))
    sprites["jump"] = []
    for sprite in os.listdir("Jump"):
        sprites["jump"].append(pygame.image.load("Jump" + dirSymbol + sprite))
    os.chdir("..")
    os.chdir("..")
    return sprites

def playerAttackAnimation(window, player):
    if(player.smallAttackFrame > 0 and player.smallAttackFrame < len(player.sprites["rightSmallAttack"]) - .7):
        player.smallAttackFrame += .7
        if(player.orientation == 1):
            player.sprite = "right"
            window.blit(player.sprites["rightSmallAttack"][int(player.smallAttackFrame)], (player.rect.x, player.rect.y))
        else:
            player.sprite = "left"
            window.blit(player.sprites["leftSmallAttack"][int(player.smallAttackFrame)], (player.rect.x - 38, player.rect.y))
    else:
        player.smallAttackFrame = 0

def main():
    #Initialize the window
    pygame.init()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption(NAME)

    #Create the background object
    background = pygame.Surface(window.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #Draw the background
    window.blit(background, (0,0))
    pygame.display.flip()

    activeInterface = "game"
    menu = []
    menu.append(UIElement(100, 100, 150, 40, "game", "Return to game"))
    #menu.append(UIElement(100, 150, 150, 40, "menu", "Menu"))
    menu.append(UIElement(screenWidth/2,screenHeight/2,50,20,"menu","Paused"))

    #Create the player object
    player = Player(500, 300)
    player.sprites = loadPlayerSprites()

    pauseBg = pygame.Surface((screenWidth,screenHeight))
    pauseBg.set_alpha(1)
    pauseBg.fill((255, 255, 255))
    bgCtr = 0;

    enemies = []
    #Create enemies
    enemies = []
    for x in range(1, 2):
        enemies.append(Spinner(x*300, 200, 50, 50, 100, 3))

    for enemy in enemies:
        enemy.loadSprites(dirSymbol)
    # Create map object
    level = Map(screenWidth,screenHeight, viewXPadding, viewYPadding)
    obstacles = level.getObjectList() # If the player is out of bounds, update the obstacles

    while True:
        if(activeInterface == "menu"):
            if (bgCtr < 100):
                window.blit(pauseBg, (0,0))
                bgCtr+= 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    for element in menu:
                        if(element.rect.collidepoint(mousePos)):
                            activeInterface = element.clicked()
                            if(not activeInterface == "menu"):
                                hasRun = False;
            if (not hasRun):
                for element in menu:
                    element.drawElement(window)

            hasRun = True;

        elif(activeInterface == "game"):
            player.time += 1
            player.sprite = "idle"
            #Refresh the background
            window.blit(background, (0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        bgCtr = 0;
                        hasRun = False;
                        activeInterface = "menu"

                    #Check if the z key is pressed
                    if event.key == pygame.K_z:
                        if(player.orientation == 1):
                            attackRect = pygame.Rect(player.rect.x+player.rect.width, player.rect.y, 38, player.rect.height)
                        else:
                            attackRect = pygame.Rect(player.rect.x - 38, player.rect.y, 38, 32)
                        player.smallAttackFrame = 1
                        for enemy in enemies:
                            #If an enemy is in range call smallAttack from the player
                            if(enemy.rect.colliderect(attackRect)):
                                enemy.damage(30, player)
                        for obstacle in obstacles:
                            if(obstacle.rect.colliderect(attackRect)):
                                obstacle.damage(20)
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
                            attackRect = pygame.Rect(player.rect.x + player.rect.width, player.rect.y, 2000, player.rect.height)
                            for obstacle in obstacles:
                                if(attackRect.colliderect(obstacle.rect)):
                                    attackRect.width = obstacle.rect.x - attackRect.x
                        else:
                            attackRect = pygame.Rect(player.rect.x - 2000, player.rect.y, 2000, player.rect.height)
                            for obstacle in obstacles:
                                if(attackRect.colliderect(obstacle.rect)):
                                        difference = attackRect.x - obstacle.rect.x
                                        attackRect.x = obstacle.rect.x
                                        attackRect.width -= difference

                    # If the c key is pressed
                    if event.key == pygame.K_c:
                        print("player X = " + str(player.rect.x))
                        print("player Y = " + str(player.rect.y))
                        print("xMax = " + str(level.xMax - level.x))
                        print("xMin = " + str(level.xMin - level.x))
                        print("yMax = " + str(level.yMax - level.y))
                        print("yMin = " + str(level.yMin - level.y))

            if(not level.inBounds(player)): # Check if the player is in bounds every loop
                player.updatePos(level.x, level.y)
                for enemy in enemies:
                    enemy.updatePos(level.x, level.y)
                level.setBounds()
                obstacles = level.getObjectList() # If the player is out of bounds, update the obstacles

            keys = pygame.key.get_pressed()
            #Movement left/right
            if keys[pygame.K_LEFT]:
                player.sprite = "left"
                player.orientation = -1
                player.moveX(-1)
            if keys[pygame.K_RIGHT]:
                player.sprite = "right"
                player.orientation = 1
                player.moveX(1)

            #Check collisions on x axis
            player.updatePos(level.x, level.y)
            player.checkObstacleCollisions(obstacles, level)

            #Jump
            if keys[pygame.K_UP]:
                if(player.onGround):
                    player.jumping = 2.3
                    player.moveY(player.jumping)
            player.moveY(player.jumping)

            #Check collisions on y axis
            player.updatePos(level.x, level.y)
            player.checkObstacleCollisions(obstacles, level)

            for enemy in enemies:
                #Check if player is on the ground for jump attack
                if(not player.onGround):
                    #Create rectangle to collide with enemy
                    attack = pygame.Rect(player.rect.x, player.rect.y + player.rect.height,
                                        player.rect.width, 16)
                    #If rectangle collides, do damage
                    if(enemy.rect.colliderect(attack)):
                        enemy.damage(30, player)
                if(enemy.health <= 0 and enemy.animationFrame == len(enemy.sprites[enemy.sprite]) - 1):
                    del enemies[enemies.index(enemy)]
                else:
                    if(time.time() - enemy.animation >= 0.1):
                        enemy.animationFrame += 1
                        enemy.animation = time.time()
                        if(enemy.animationFrame >= len(enemy.sprites[enemy.sprite])):
                            enemy.animationFrame = 0

                    #Get the distance between the enemy and the player
                    playerDist = math.sqrt(math.pow(player.rect.x - enemy.rect.x, 2)
                                            + math.pow(player.rect.y - enemy.rect.y, 2))

                    #If the player is within aggro distance of the enemy, run aggro action
                    if(playerDist <= enemy.aggrodist and not enemy.aggro):
                        enemy.aggroAction(player)
                        enemy.aggro = True
                    if(enemy.aggro):
                        enemy.aggroAction(player)
                        if(playerDist > enemy.aggrodist + 100 and enemy.interruptable):
                            enemy.aggro = False

                    #Draw enemy and to kinatmics calculations/check for collisions
                    enemy.time += 1
                    enemy.moveY(0)
                    enemy.checkObstacleCollisions(obstacles, level)
                    if(enemy.onGround):
                        enemy.time = 0
                    enemy.drawEnemy(window)


            if(player.jumping > 0):
                player.jumpFrame += 1
                if(player.jumpFrame >= len(player.sprites["jump"])):
                    player.jumpFrame = 1
                window.blit(player.sprites["jump"][int(player.jumpFrame)], (player.rect.x, player.rect.y))

            #If the player is on the ground reset the jump and time values
            if(player.onGround):
                player.time = 0
                player.jumping = 0

            playerAttackAnimation(window, player)

            #Do vulnerability increase/decay calculations
            if(player.vulnerable):
                currentTime = int(time.time() - startTime)
                player.vulnerability = 0.1*currentTime + 1
            else:
                if(player.vulnerability > 1):
                    currentTime = int(time.time() - startTime)
                    player.vulnerability = -0.05*currentTime + vulnerabilityDecay

            #Draw the player
            player.drawPlayer(window)

            #Draw the obstacles
            for obstacle in obstacles:
                if(obstacle.health <= 0):
                    del obstacles[obstacles.index(obstacle)]
                else:
                    obstacle.drawObstacle(window, level)

        #Update the display
        pygame.display.update()

if __name__ == "__main__":
    # OS detection for filepath stuff
    if os.name == 'nt': # If we're using Windows
        dirSymbol = "\\"
    main()
