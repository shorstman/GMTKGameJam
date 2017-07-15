import pygame
import time

class Enemy():
    def __init__(self, x, y, width, height, aggrodist, speed):
        self.health = 100
        self.sneak = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.onGround = False
        self.orientation = 1;
        self.time = 0
        self.aggrodist = 100
        self.aggro = False
        self.color = (255, 0, 0)

    def moveX(self, distance):
        #Move 'distance' in the x direction
        self.dx = distance
        self.rect.x += self.dx
        """
        if(self.rect.x > 928 - self.rect.width):
            self.rect.x = 928 - self.rect.width
        if(self.rect.x < 0):
            self.rect.x = 0
        """

    def moveY(self, distance):
        self.dy = -distance + 0.1*self.time
        self.rect.y += self.dy
        self.onGround = False


    def drawEnemy(self, window):
        #Draw the player
        pygame.draw.rect(window, self.color, self.rect)

    def checkCollisions(self, colliders):
        #Check if the player has collided with 'collider'
        if(self.dy > 0):
            self.onGround = False
        for collider in colliders:
            if self.rect.colliderect(collider.rect):
                if self.dx > 0:
                    self.rect.right = collider.rect.left
                elif self.dx < 0:
                    self.rect.left = collider.rect.right
                if self.dy > 0:
                    self.onGround = True
                    self.rect.bottom = collider.rect.top
                elif self.dy < 0:
                    self.rect.top = collider.rect.bottom

        self.dx = 0
        self.dy = 0

    def kill(self):
        del self


class Chomper(Enemy):
    """
    This class inherits the functions from the enemy class. It is an enemy type
    that will wait for three seconds and then charge the player.
    There is currently a bug that makes it run away from the player after
    its first charge
    """
    def __init__(self, x, y):
        self.health = 100
        self.sneak = 0
        self.rect = pygame.Rect(x, y, 32, 32)
        self.dx = 0
        self.dy = 0
        self.speed = 5
        self.orientation = 1
        self.onGround = False
        self.orientation = 1;
        self.time = 0
        self.aggrodist = 100
        self.aggro = False
        self.chargeStart = None
        self.startX = 0
        self.color = (255, 0, 0)

    def aggroAction(self, player):
        """
        This is triggered when the player enters the aggro distance of the enemy
        """
        #If it is not already aggro'd
        if(not self.aggro):
            self.aggro = True
            #Get the start time to calculate 3 seconds
            self.chargeStart = time.time()
            #Find the direction the player is in
            if(player.rect.x > self.rect.x):
                self.orientation = 1
            else:
                self.orientation = -1

            #Get the starting x value so always charges the same distance
            self.startX = self.rect.x

        #Calculate how long it has been since the start time
        currentTime = int(time.time() - self.chargeStart)
        if(currentTime >= 3): #If it has been three seconds
            #Add the speed
            self.rect.x += self.speed*self.orientation
            #If it reaches 300 pixels from the starting point, stop
            if(abs(self.rect.x - self.startX) > 300):
                self.aggro = False
