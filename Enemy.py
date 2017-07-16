import pygame
import time
import os

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
        if(coolDown > 1): #Check time elapsed
            #Do damage and start a new cooldown
            self.health -= damage
            self.damageCooldown = True
            self.damageCooldownTime = time.time()
            if(attacker.rect.x > self.rect.x):
                self.moveX(-10)
            else:
                self.moveX(10)
            self.moveY(3)

            if(self.health <= 0):
                del self

    def drawEnemy(self, window):
        #Draw the player
        pygame.draw.rect(window, self.color, self.rect)

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

class Chomper(Enemy):
    """
    This class inherits the functions from the enemy class. It is an enemy type
    that will wait for three seconds and then charge the player.
    """
    def __init__(self, x, y):
        self.health = 100
        self.rect = pygame.Rect(x, y, 64, 64)
        self.dx = 0
        self.dy = 0
        self.speed = 5
        self.orientation = 1
        self.onGround = False
        self.orientation = 1;
        self.time = 0
        self.aggrodist = 100
        self.aggro = False
        self.chargeStart = time.time()
        self.startX = 0
        self.color = (255, 0, 0)
        self.damageCooldown = False
        self.interruptable = True

    def aggroAction(self, player):
        """
        This is triggered when the player enters the aggro distance of the enemy
        """
        #TODO: Make the directionality of this more complex once we have sprites for this
        #Calculate how long it has been since the start time
        currentTime = int(time.time() - self.chargeStart)
        if(not self.aggro):
            #Get the start time to calculate 3 seconds
            self.chargeStart = time.time()
            self.interruptable = False
        if(currentTime == 0):
            #Find the direction the player is in
            if(player.rect.x > self.rect.x):
                self.orientation = 1
            else:
                self.orientation = -1
            #Get the starting x value so always charges the same distance
            self.startX = self.rect.x
        if(currentTime >= 3): #If it has been three seconds
            #Add the speed
            self.moveX(self.speed*self.orientation)
            #If it reaches 300 pixels from the starting point, stop
            if(abs(self.rect.x - self.startX) > 150):
                self.chargeStart = time.time()
                self.interruptable = True
                self.aggro = False

class Spinner(Enemy):
    def __init__(self, x, y, width, height, aggrodist, speed):
        super(Spinner, self).__init__(self, x, y, width, height, aggrodist, speed)
        self.sprites = {}

    def loadSprites(self, dirSymbol):
        os.chdir("sprites" + dirSymbol + "Spinner_Sprites")
        self.sprites = {}
        self.sprites["idle"] = []
        for sprite in os.listdir("Hover_Animation"):
            self.sprites["idle"].append(pygame.image.load("Hover_Animation" + dirSymbol + sprite))
        self.sprites["body-startup"] = []
        self.sprites["body-spin"] = []
        for sprite in os.listdir("Body_Spin_Animation"):
            if("Ready" in sprite):
                self.sprites["body-startup"].append(pygame.image.load("Body_Spin_Animation" + dirSymbol + sprite))
            else:
                self.sprites["body-spin"].append(pygame.image.load("Body_Spin_Animation" + dirSymbol + sprite))
        self.sprites["flame-startup"] = []
        for sprite in os.listdir("Flame_Initiate_Animation"):
            self.sprites["flame-startup"].append(pygame.image.load("Flame_Initiate_Animation" + dirSymbol + sprite))
        self.sprites["flame-spin"] = []
        for sprite ein os.listdir("Flame_Spin_Animation"):
            self.sprites["flame-spin"].append(pygame.image.load("Flame_Spin_Animation" + dirSymbol + sprite))
