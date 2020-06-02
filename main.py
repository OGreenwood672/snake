import pygame
import random
import datetime
import time
import pygame.locals
import os
import neat
import matplotlib.pyplot as plt
import pickle

import snakeObject
import fruitObject

pygame.init()
pygame.display.set_caption('Snake')

display_width = 900
display_height = 600

size = display_height // 20

GEN = 0
average = []
averageFit = []

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

background = (0, 0, 0)
foreground = (255, 255, 255)
foodColor = (219, 64, 64)

def build(snk, AI):
    global GEN
    gameDisplay.fill(background)
    if not AI:
        text(f'Score: {snk.score}', 25, 0, 0)
    else: 
        text(f'GEN: {GEN}', 25, 0, 0)
        if average:
            x = (display_width / 5) / len(average)
            y = (display_height / 5) / max(average)
            for i in range(len(average) - 1):
                try:
                    start = (x * i, display_height - average[i] * y)
                    stop = (x * (i+1), display_height - average[i+1] * y)
                    pygame.draw.line(gameDisplay, foreground, start, stop, 2)
                except:
                    pass

def text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(text, True, foreground)
    gameDisplay.blit(text, (x, y))

def addInfo():
    global averageFit
    global average
    average.append(max(averageFit))
    averageFit = []

def showSnake(snk):
    for x, y in snk.memory:
        pygame.draw.rect(gameDisplay, foreground, [x, y, snk.size, snk.size])

def showFood(food):
    pygame.draw.rect(gameDisplay, foodColor, [food.fruitX, food.fruitY, food.size, food.size])

def checkPressHP():
    YLEVEL = display_height * 0.3
    YSIZE = size * 3
    XCOLUMN1 = display_width * 0.35
    XCOLUMN2 = display_width * 0.55
    XSIZE = size * 5
    XADDITION = display_width * 0.015
    YADDITION = display_height * 0.05
    BUTTONCOLOR = (30, 230, 83)
    pygame.draw.rect(gameDisplay, BUTTONCOLOR, [XCOLUMN2, YLEVEL, XSIZE, YSIZE])
    pygame.draw.rect(gameDisplay, BUTTONCOLOR, [XCOLUMN1, YLEVEL, XSIZE, YSIZE])
    text('SINGLEPLAYER', 25, XCOLUMN1 + XADDITION, YLEVEL + YADDITION)
    text('TRAIN VIA', 22, XCOLUMN2 + XADDITION, YLEVEL + YADDITION * 0.65)
    text('GENETIC ALGORITHEM', 17, XCOLUMN2 + XADDITION, YLEVEL + YADDITION * 2)
    mouse = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    if mouse[0]:
        buttonx_1 = XCOLUMN1 <= x < XCOLUMN1 + XSIZE
        buttonx_2 = XCOLUMN2 <= x < XCOLUMN2 + XSIZE
        buttony = YLEVEL <= y < YLEVEL + YSIZE
        if buttony and buttonx_1:
            singlePlayer()
        elif buttony and buttonx_2:
            runGA()
    keyinput = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

def checkPressSP():
    keyinput = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            if keyinput[pygame.K_UP]: return 'up'
            elif keyinput[pygame.K_DOWN]: return 'down'
            elif keyinput[pygame.K_LEFT]: return 'left'
            elif keyinput[pygame.K_RIGHT]: return 'right'
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

def checkPressGA():
    for event in pygame.event.get():
        keyInput = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            #plt.plot(average)
            #plt.show()
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if keyInput[pygame.K_RETURN]:
                plt.plot(average)
                plt.show()

def runHome():
    running = True
    snk = snakeObject.snake(display_width, display_height, size)
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-398')
    p.run(home, 100)

def home(genomes, config):
    nets = []
    ge = []
    snakes = []
    foodList = []

    for _, g in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(g, config))
        snakes.append(snakeObject.snake(display_width, display_height, size))
        foodList.append(fruitObject.fruit(display_width, display_height, size))
        g.fitness = 0
        ge.append(g)

    gameEvent = True
    index = 0
    movementDue = 0
    speed = 4
    while gameEvent:

        build(snakes[0], False)
        if movementDue > speed:
            viewDistance = snakes[index].getDistances(foodList[index])

            output = nets[index].activate((viewDistance))

            output = output.index(max(output))
            directions = ['up', 'down', 'left', 'right']
            snakes[index].checkDirection(directions[output])

            snakes[index].newCoords()
            snakes[index].move()
            snakes[index].memory = [snakes[index].memory[0]]

            if snakes[index].checkEat(foodList[index]):
                foodList[index].spot()
                snakes[index].score += 1
                snakes[index].maxMoves += 100
            
            snakes[index].movesMade += 1
            
            if not snakes[index].checkAlive() or snakes[index].movesMade > snakes[index].maxMoves:
                ge[index].fitness = snakes[index].score + 1
                averageFit.append(ge[index].fitness)
                nets.pop(index)
                ge.pop(index)
                foodList.pop(index)
                snakes.pop(index)
            
            movementDue = 0
        
        showSnake(snakes[index])
        showFood(foodList[index])


        checkPressHP() # buttons
        movementDue += 1
        pygame.display.update()
        clock.tick(60)

def singlePlayer():
    running = True
    snk = snakeObject.snake(display_width, display_height, size)
    food = fruitObject.fruit(display_width, display_height, size)
    showFood(food)
    changeDirection = None
    movementDue = 0
    speed = 8
    while running:

        if movementDue > speed:

            if changeDirection:
                snk.checkDirection(changeDirection)

            build(snk, False)

            snk.newCoords()
            snk.move()
            showSnake(snk)
            showFood(food)

            movementDue = 0
            
        
        if snk.checkEat(food):
            food.spot()
            snk.score += 1

        newDirection = checkPressSP()
        if newDirection:
            changeDirection = newDirection
        
        if not snk.checkAlive():
            running = False
        
        movementDue += 1

        pygame.display.update()
        clock.tick(60)

def runGA():
    configPath = os.path.join(os.path.dirname(__file__), 'GAInfo.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                configPath)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(200, filename_prefix='17Input-'))
    winner = p.run(snakeGA, 300)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    #with open('snake.model', 'wb') as f:
     #   pickle.dump(winner_net, f)
    #plt.plot(average)
    #plt.show()

def snakeGA(genomes, config):
    global GEN
    nets = []
    ge = []
    snakes = []
    foodList = []

    for _, g in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(g, config))
        snakes.append(snakeObject.snake(display_width, display_height, size))
        foodList.append(fruitObject.fruit(display_width, display_height, size))
        g.fitness = 0
        ge.append(g)

    gameEvent = True
    while gameEvent:

        build(snakes[0], True)

        for index in range(len(snakes)-1):

            if index > len(snakes)-1:
                break

            viewDistance = snakes[index].getDistances(foodList[index])

            output = nets[index].activate((viewDistance))

            output = output.index(max(output))
            directions = ['up', 'down', 'left', 'right']
            snakes[index].checkDirection(directions[output])

            snakes[index].newCoords()
            snakes[index].move()
            showSnake(snakes[index])
            showFood(foodList[index])

            if snakes[index].checkEat(foodList[index]):
                foodList[index].spot()
                snakes[index].score += 1
                snakes[index].maxMoves += 150

            snakes[index].movesMade += 1

            if not snakes[index].checkAlive() or snakes[index].movesMade > snakes[index].maxMoves:
                ge[index].fitness = snakes[index].score + 1
                averageFit.append(ge[index].fitness)
                nets.pop(index)
                ge.pop(index)
                foodList.pop(index)
                snakes.pop(index)
            
            checkPressGA()

        if len(snakes) <= 1:
            gameEvent = False
            break

        pygame.display.update()
        clock.tick(120)
    GEN += 1
    addInfo()

if __name__ == '__main__':
    runHome()