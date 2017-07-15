import random
import copy
from PIL import Image

aliveStart = 45
width = 128
height = 64
deathLimit = 3
birthLimit = 4
steps = 2

def initializeMap(cellMap):
    for x in range(0, width):
        cellMap.append([])
        for y in range(0, height):
            if(random.randint(1,100) < aliveStart):
                cellMap[x].append(True)
            else:
                cellMap[x].append(False)
    return cellMap

def doStep(oldMap):
    newMap = copy.deepcopy(oldMap)
    for x in range(0, len(newMap)):
        for y in range(0, len(newMap[x])):
            aliveNeighbors = countAliveNeighbors(oldMap, x, y)
            if(oldMap[x][y]):
                if(aliveNeighbors < deathLimit):
                    newMap[x][y] = False
                else:
                    newMap[x][y] = True
            else:
                if(aliveNeighbors > birthLimit):
                    newMap[x][y] = True
                else:
                    newMap[x][y] = False
    return newMap


def countAliveNeighbors(cellMap, x, y):
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

def generateMap():
    cellMap = []
    cellMap = initializeMap(cellMap)
    for step in range(0, steps):
        cellMap = doStep(cellMap)
    return cellMap

obstacleMap = generateMap()
output = Image.new('RGB', (width, height))

imagable = []
for x in range(0, len(obstacleMap)):
    for y in range(0, len(obstacleMap[x])):
        if(obstacleMap[x][y]):
            imagable.append((0, 0, 255))
        else:
            imagable.append((168, 168, 168))

output.putdata(imagable)
output.save('map.png')
