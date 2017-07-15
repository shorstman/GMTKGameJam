
class Item():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class Health(Item):
    def __init__(self, healthBoost):
        super.__init__()
        self.healthBoost = healthBoost

    def onPickUp(self, player):
        player.health += self.healthBoost
        if(player.health > player.maxHealth):
            player.health = player.maxHealth
