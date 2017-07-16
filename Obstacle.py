import pygame

class Obstacle(object):
    def __init__(self, x, y, width, height, health):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health

    def drawObstacle(self, window):
        pygame.draw.rect(window, (168, 168, 168), self.rect)

    def damage(self, damage):
        self.health -= damage
        if(self.health >= 0):
            del self

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
