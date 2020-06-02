import os
from math import atan2, degrees

class snake:
    def __init__(self, display_width, display_height, size):
        self.snakeX = int(round(display_width // 2 / size) * size)
        self.snakeY = int(round(display_height // 2 / size) * size)
        self.display_width = display_width
        self.display_height = display_height
        self.direction = 'up'
        self.size = size
        self.score = 0
        self.movesMade = 0
        self.maxMoves = display_width // 4
        self.memory = []
    
    def newCoords(self):
        directions = {'up': -self.size, 'down': self.size,
                      'left': -self.size, 'right': self.size}
        if self.direction in ['up', 'down']:
            self.snakeY += directions[self.direction]
        else:
            self.snakeX += directions[self.direction]
    
    def checkAlive(self):
        x = self.snakeX in range(self.display_width)
        y = self.snakeY in range(self.display_height)
        try:
            itself = (self.snakeX, self.snakeY) in self.memory[1:]
        except:
            itself = False
        return x and y and not itself

    def move(self):
        self.memory.insert(0, (self.snakeX, self.snakeY))
        while len(self.memory) > self.score + 1:
            self.memory.pop()
    
    def checkDirection(self, new):
        ud = ['up', 'down']
        lr = ['left', 'right']
        allDirect = [ud, lr]
        for i in allDirect:
            if self.direction in i and new in i:
                break
        else:
            self.direction = new
    
    def checkEat(self, frt):
        return [self.snakeX, self.snakeY] == [frt.fruitX, frt.fruitY]
    
    def getDistances(self, fruit):
        distances = []
        directions = [[0, 1], [1, 1], [1, 0], [1, -1],
                      [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        memory = [list(i) for i in self.memory]
        fruitCoords = [[fruit.fruitX, fruit.fruitY]]
        for x in [memory, fruitCoords]:
            for i in directions:
                total = 0
                change = 1
                coords = [((change * i[0]) * self.size) + self.snakeX, ((change * i[1]) * self.size) + self.snakeY]
                while coords[0] in range(self.display_width) and coords[1] in range(self.display_height) and True:
                    if coords in x:
                        total = change
                        break
                    change += 1
                    coords = [((change * i[0]) * self.size) + self.snakeX, ((change * i[1]) * self.size) + self.snakeY]
                else: 
                    if x != fruitCoords:
                        total = change - 1
                distances.append(total)
        
        delta_x = self.snakeX - fruitCoords[0][0]
        delta_y = fruitCoords[0][1] - self.snakeY
        theta = degrees(atan2(delta_y, delta_x))

        info = distances[:8]
        info.append(theta)

        return info