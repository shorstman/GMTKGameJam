import pygame

class Obstacle(object):
    def __init__(self, x, y, width, height, health):
        self.worldX = x
        self.worldY = y
        self.rect = pygame.Rect(self.worldX, self.worldY, width, height)
        self.health = health

    def drawObstacle(self, window, level):
        pygame.draw.rect(window, (168, 168, 168), self.rect)
        pygame.draw.rect(window, (100, 100, 100), self.rect, 3)

    def damage(self, damage):
        self.health -= damage
        if(self.health >= 0):
            del self

    def updateRectangle(self, xOffset, yOffset):
        newX = self.worldX - xOffset
        newY = self.worldY - yOffset
        self.rect = pygame.Rect(newX, newY, self.rect.width, self.rect.height)

class Hurty(Obstacle):
    def __init__(self, x, y, width, height, damage, health):
        super(Hurty, self).__init__(x, y, width, height, health)
        self.damage = damage

    #Override the damage function to do nothing
    def damage(self, damage):
        pass

class Unbreakable(Obstacle):
    def __init__(self, x, y, width, height, health):
        super(Unbreakable, self).__init__(x, y, width, height, health)

    #Override the damage function to do nothing
    def damage(self, damage):
        pass

    def drawObstacle(self, window, level):
        pygame.draw.rect(window, (100, 100, 100), self.rect)
        pygame.draw.rect(window, (32, 32, 32), self.rect, 3)
