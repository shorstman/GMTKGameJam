import pygame
import time
import os
import random
from _thread import start_new_thread

class Enemy():
    def __init__(self, x, y, width, height, aggrodist, speed):
        self.health = 100
        self.rect = pygame.Rect(x, y, width, height)
        self.worldX = x
        self.worldY = y
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.onGround = False
        self.orientation = 1;
        self.time = 0
        self.aggrodist = 100
        self.aggro = False
        self.color = (255, 0, 0)
        self.damageCooldown = False
        self.damageCooldownTime = None
        self.interruptable = True

    def updatePos(self, xOffset, yOffset):
        newX = self.worldX - xOffset
        newY = self.worldY - yOffset
        self.rect = pygame.Rect(newX, newY, self.rect.width, self.rect.height)

    def moveX(self, distance):
        #Move 'distance' in the x direction
        self.dx = distance
        self.rect.x += self.dx
        self.worldX += self.dx

    def moveY(self, distance):
        self.dy = -distance + 0.1*self.time
        self.rect.y += self.dy
        self.worldY += self.dy
        self.onGround = False

    def damage(self, damage, attacker):
        """
        This function does damage to the enemy
        """
        #Set the cooldown to a default value greater than the actual cooldown,
        #This way if self.damageCooldown is false the second if won't throw an error and will execute
        coolDown = 4
        if(self.damageCooldown):
            #Find the time elapsed since cooldown started
            coolDown = int(time.time() - self.damageCooldownTime)
        if(coolDown > 0.1): #Check time elapsed
            #Do damage and start a new cooldown
            self.aggro = False
            self.health -= damage
            self.damageCooldown = True
            self.damageCooldownTime = time.time()
            if(attacker.rect.x > self.rect.x):
                self.moveX(-10)
            else:
                self.moveX(10)
            self.moveY(3)
            self.animation = time.time()
            self.animationFrame = 0
            if(self.health > 0):
                self.sprite = "damage"
            else:
                self.sprite = "death"

    def checkObstacleCollisions(self, colliders, level):
        """
        This function checks only against basic obstacles because much more needs
        to be done to deal with a collision with these.
        """
        #Check if the player has collided with 'collider'
        if(self.dy > 0):
            self.onGround = False
        for collider in colliders:
            if self.rect.colliderect(collider.rect):
                if self.dx > 0:
                    self.rect.right = collider.rect.left
                    self.worldX = collider.rect.left + level.x
                elif self.dx < 0:
                    self.rect.left = collider.rect.right
                    self.worldX = collider.rect.right + level.x
                if self.dy > 0:
                    #If the player is on top of an obstacle, set onGround to True
                    self.onGround = True
                    self.rect.bottom = collider.rect.top
                    self.worldY = collider.rect.top - self.rect.height + level.y
                elif self.dy < 0:
                    self.rect.top = collider.rect.bottom
                    self.worldY = collider.rect.bottom + level.y
        self.dx = 0
        self.dy = 0

    def drawEnemy(self, window):
        window.blit(self.sprites[self.sprite][self.animationFrame], (self.rect.x, self.rect.y))
        if(self.animationFrame == len(self.sprites[self.sprite]) - 1 and self.sprite == "damage"):
            self.sprite = "idle"
            self.animationFrame = 0
        if(self.animationFrame == len(self.sprites[self.sprite]) - 1 and self.sprite == "death"):
            pass

class Spinner(Enemy):
    def __init__(self, x, y, width, height, aggrodist, speed):
        super(Spinner, self).__init__(x, y, width, height, aggrodist, speed)
        self.sprites = {}
        self.animation = time.time()
        self.animationFrame = 0
        self.sprite = "idle"
        self.attackMode = False
        self.attackTime = 0

    def loadSprites(self, dirSymbol):
        os.chdir("sprites" + dirSymbol + "Spinner_Sprites")
        self.sprites = {}
        self.sprites["idle"] = []
        for sprite in os.listdir("Hover_Animation"):
            self.sprites["idle"].append(pygame.image.load("Hover_Animation" + dirSymbol + sprite))
        self.sprites["aggro"] = []
        self.sprites["spin"] = []
        for sprite in os.listdir("Body_Spin_Animation"):
            if("Ready" in sprite):
                self.sprites["aggro"].append(pygame.image.load("Body_Spin_Animation" + dirSymbol + sprite))
            else:
                self.sprites["spin"].append(pygame.image.load("Body_Spin_Animation" + dirSymbol + sprite))
        self.sprites["death"] = []
        for sprite in range(1, len(os.listdir("Death_Animation")) + 1):
            self.sprites["death"].append(pygame.image.load("Death_Animation" + dirSymbol + "Death_Animation_" + str(sprite) + ".png"))
        self.sprites["damage"] = []
        for sprite in os.listdir("Hurt_Animation"):
            self.sprites["damage"].append(pygame.image.load("Hurt_Animation" + dirSymbol + sprite))
        os.chdir("..")
        os.chdir("..")

    def attack(self, player):
        attackRect = pygame.Rect(self.x - 16, self.y, 82, 50)
        if(player.rect.colliderect(attackRect)):
            player.damage(20)

    def aggroAction(self, player, playerDist):
        attackSpeed = 1
        if(self.sprite == "idle"):
            self.sprite = "aggro"
            self.animationFrame = 0
        if(self.sprite == "aggro" and self.animationFrame == len(self.sprites["aggro"]) - 2):
            self.animationFrame = len(self.sprites["aggro"]) - 2
        if(playerDist < 50 and random.randint(1,100) == 1 and not self.attackMode):
            self.sprite = "spin"
            self.attackMode = True
            self.animationFrame = 0
        if(self.sprite == "spin" and self.animationFrame == len(self.sprites["spin"]) - 1):
            self.sprite == "aggro"
            self.animationFrame = 0
            attackSpeed = 1
        if(self.attackMode):
            attackSpeed = 4
            attackRect = pygame.Rect(self.rect.x - 16, self.rect.y, 82, 50)
            if(player.rect.colliderect(attackRect)):
                player.damage(20, self)

        if(player.rect.x > self.rect.x):
            self.moveX(attackSpeed)
        else:
            self.moveX(-attackSpeed)
