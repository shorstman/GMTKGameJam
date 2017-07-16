import pygame
import threading

class Player():
    def __init__(self, x, y):
        self.maxHealth = 100
        self.health = self.maxHealth
        self.worldX = x
        self.worldY = y
        self.rect = pygame.Rect(x, y, 34, 64)
        self.dx = 0
        self.dy = 0
        self.onGround = False
        self.orientation = 1
        self.time = 0
        self.jumping = 0
        self.vulnerable = False
        self.vulnerability = 1
        self.rocketDamage = 30
        self.damageCooldown = False
        self.damageCooldownTime = 0
        self.sprite = "idle"
        self.hoverSprite = 1
        self.smallAttackFrame = 0
        self.jumpFrame = 0

    def updatePos(self, xOffset, yOffset):
        newX = self.worldX - xOffset
        newY = self.worldY - yOffset
        self.rect = pygame.Rect(newX, newY, self.rect.width, self.rect.height)

    def moveX(self, distance):
        self.dx = distance
        self.rect.x += self.dx
        self.worldX += self.dx

    def moveY(self, distance):
        #Do kinematics calculations for gravity
        self.dy = -distance + 0.02*self.time
        self.worldY += self.dy
        self.rect.y += self.dy
        self.onGround = False

    def damage(self, damage):
        #Set the cooldown to a default value greater than the actual cooldown,
        #This way if self.damageCooldown is false the second if won't throw an error and will execute
        coolDown = 4
        if(self.damageCooldown):
            #Find the time elapsed since cooldown started
            coolDown = int(time.time() - self.damageCooldownTime)
        if(coolDown > 1): #Check time elapsed
            #Do damage and start a new cooldown
            self.health -= damage*self.vulnerability
            self.damageCooldown = True
            self.damageCooldownTime = time.time()

    def drawPlayer(self, window):
        #Draw the player
        if(self.hoverSprite >= len(self.sprites[self.sprite])):
            self.hoverSprite = 1
        window.blit(self.sprites[self.sprite][0], (self.rect.x, self.rect.y))
        if(self.jumping == 0):
            window.blit(self.sprites[self.sprite][int(self.hoverSprite)], (self.rect.x, self.rect.y))
            self.hoverSprite += .05

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

    def checkCollisions(self, collider):
        """
        This function checks collisions against anything and returns a boolean
        value for more versatility than checkObstacleCollisions()
        """
        collided = False
        if self.rect.colliderect(collider.rect):
            collided = True

        return collided

    def smallAttack(self):
        while int(self.smallAttackFrame) < len(self.sprites["leftSmallAttack"]):
            self.smallAttackFrame += .0004
        self.smallAttackFrame = 0
