import pygame

class Player():
    def __init__(self, x, y):
        self.health = 100
        self.sneak = 0
        self.rect = pygame.Rect(x, y, 64, 64)
        self.dx = 0
        self.dy = 0
        self.onGround = False
        self.weight = 1
        self.orientation = 1
        self.time = 0
        self.jumps = 0
        self.jumping = 0
        self.vulnerable = False
        self.vulnerability = 1
        self.rocketDamage = 30
        self.damageCooldown = False
        self.damageCooldownTime = 0

    def moveX(self, distance):
        #Move 'distance' in the x direction
        self.dx = distance
        self.rect.x += self.dx
        if(self.rect.x > 928 - self.rect.width):
            self.rect.x = 928 - self.rect.width
        if(self.rect.x < 0):
            self.rect.x = 0

    def moveY(self, distance):
        #Do kinematics calculations for gravity
        self.dy = -distance + 0.02*self.time
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
        pygame.draw.rect(window, (0, 255, 0), self.rect)

    def checkObstacleCollisions(self, colliders):
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
                elif self.dx < 0:
                    self.rect.left = collider.rect.right
                if self.dy > 0:
                    #If the player is on top of an obstacle, set onGround to True
                    self.onGround = True
                    self.rect.bottom = collider.rect.top
                elif self.dy < 0:
                    self.rect.top = collider.rect.bottom
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
