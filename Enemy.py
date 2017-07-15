import pygame

class Enemy():
    def __init__(self, x, y):
        self.health = 100
        self.sneak = 0
        self.rect = pygame.Rect(x, y, 32, 32)
        self.dx = 0
        self.dy = 0
        self.onGround = False
        self.weight = 1;
        self.orientation = 1;

    def moveX(self, distance):
        #Move 'distance' in the x direction
        self.dx = distance
        self.rect.x += self.dx
        if(self.rect.x > 928 - self.rect.width):
            self.rect.x = 928 - self.rect.width
        if(self.rect.x < 0):
            self.rect.x = 0

    def jump(self, distance, time):
        #Move 'distance' in the y direction
        self.dy = distance
        self.rect.y += self.dy
        if(self.rect.y > 600 - self.rect.height):
            self.rect.y = 600 - self.rect.height
        if(self.rect.y < 0):
            self.rect.y = 0
        self.onGround = False

    def moveY(self, distance, time):
        self.dy = -distance + 0.1*time
        self.rect.y += self.dy
        self.onGround = False


    def drawEnemy(self, window):
        #Draw the player
        pygame.draw.rect(window, (255, 0, 0), self.rect)

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
