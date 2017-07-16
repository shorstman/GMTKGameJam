import random
import copy
from Obstacle import *
from Enemy import *

class GenerateMap():
    def __init__(self, width, height, aliveStart, deathLimit, birthLimit, steps):
        """
        The settings for this should be
        aliveStart = 46
        height = 128
        width = 64
        deathLimit = 3
        birthLimit = 4
        steps = 2
        """
        self.width = width
        self.height = height
        self.aliveStart = aliveStart
        self.deathLimit = deathLimit
        self.birthLimit = birthLimit
        self.steps = steps
        self.boolMap = self.generateMap()
        self.map = []
        self.enemies = []
        self.convertMap()

    def initializeMap(self, cellMap):
        for x in range(0, self.width):
            cellMap.append([])
            for y in range(0, self.height):
                if(random.randint(1,100) < self.aliveStart):
                    cellMap[x].append(True)
                else:
                    cellMap[x].append(False)
        return cellMap

    def doStep(self, oldMap):
        newMap = copy.deepcopy(oldMap)
        for x in range(0, len(newMap)):
            for y in range(0, len(newMap[x])):
                aliveNeighbors = self.countAliveNeighbors(oldMap, x, y)
                if(oldMap[x][y]):
                    if(aliveNeighbors < self.deathLimit):
                        newMap[x][y] = False
                    else:
                        newMap[x][y] = True
                else:
                    if(aliveNeighbors > self.birthLimit):
                        newMap[x][y] = True
                    else:
                        newMap[x][y] = False
        return newMap


    def countAliveNeighbors(self, cellMap, x, y):
        count = 0
        for i in range(-1, 2):
            for a in range(-1, 2):
                neighbor_X = x + i
                neighbor_Y = y + a
                if(i == 0 and a == 0):
                    pass
                elif(neighbor_X < 0 or neighbor_Y < 0
                    or neighbor_X >= len(cellMap) or neighbor_Y >= (len(cellMap[x]))):
                    count += 1
                elif(cellMap[neighbor_X][neighbor_Y]):
                    count += 1

        return count

    def generateMap(self):
        cellMap = []
        cellMap = self.initializeMap(cellMap)
        for step in range(0, self.steps):
            cellMap = self.doStep(cellMap)

        # Create a spawn area so that the player doesn't spawn on top of the map
        for x in range(1, 10): # From 1 to 10 X
            for y in range(1, 5): # From 1 to 10 Y
                    cellMap[x][y] = True

        return cellMap

    def convertMap(self):
        for x in range(0, len(self.boolMap)):
            for y in range(0, len(self.boolMap[x])):
                if(not self.boolMap[x][y]):
                    self.map.append(Obstacle(x*64, y*64, 64, 64, 40))
                #Add a border around the map
                if x == 0:
                    self.map.append(Unbreakable(x*64 ,y*64 ,64 ,64 ,100))
                elif x == len(self.boolMap) - 1:
                    self.map.append(Unbreakable(x*64 ,y*64 ,64 ,64 ,100))
                elif y == 0:
                    self.map.append(Unbreakable(x*64 ,y*64 ,64 ,64 ,100))
                elif y == len(self.boolMap) - 1:
                    self.map.append(Unbreakable(x*64 ,y*64 ,64 ,64 ,100))

                if((random.randint(1,100) == 5) and (self.boolMap[x][y] == True)):
                    enemyType = random.randint(1,3)
                    if(enemyType == 1):
                        self.enemies.append(Spinner(x, y, 50, 50, 100, 3))
                        print("Created spinner enemy at " +str(x) +"," +str(y))
                    # elif(enemyType == 2):
                    #     self.enemies.append(Chomper(x*300, 200, 50, 50, 100, 3))
                    # elif(enemyType == 3):
                    #     self.enemies.append(Bomb(x*300, 200, 50, 50, 100, 3))

    def getObstacleCount(self):
        obstacleCount = 0
        for x in range(0, len(self.boolMap)):
            for y in range(0, len(self.boolMap[x])):
                if(self.boolMap[x][y]):
                    obstacleCount += 1

        return obstacleCount
