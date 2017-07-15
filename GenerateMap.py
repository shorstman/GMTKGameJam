
class GenerateMap():
    def __init__(self, width, height, aliveStart, deathLimit, birthLimit, steps):
        self.width = width
        self.height = height
        self.aliveStart = aliveStart
        self.deathLimit = deathLimit
        self.birthLimit = birthLimit
        self.steps = steps
        self.map = self.generateMap()

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
                aliveNeighbors = countAliveNeighbors(oldMap, x, y)
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
        cellMap = initializeMap(cellMap)
        for step in range(0, self.steps):
            cellMap = doStep(cellMap)
        return cellMap
