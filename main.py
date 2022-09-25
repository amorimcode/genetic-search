from os import system, name
from time import sleep
from random import randint
from math import sqrt

SPEED = 4
SLEEP = 1/SPEED

LEVEL_WIDTH = 70
LEVEL_HEIGHT = 30

WALL = '\u2588'
GOAL = '*'
HOME = 'H'
LEFT = '\u25C0'
DOWN = '\u25BC'
RIGHT = '\u25B6'
UP = '\u25B2'
STOP = "$"
EMPTY = ' '

P1_COLOR = '\033[95m'
P2_COLOR = '\033[94m'
P3_COLOR = '\033[96m'
P4_COLOR = '\033[92m'
P5_COLOR = '\033[93m'
P6_COLOR = '\033[91m'
P7_COLOR = '\033[1m'
P8_COLOR = '\033[4m'
NO_COLOR = '\033[0m'

class Simulation:
    def __init__(self, level):
        self.agents = []
        self.level = level
        self.width = len(self.level[0])
        self.height = len(self.level)

        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.level[y][x] == HOME:
                    self.home = (x, y)
                elif self.level[y][x] == GOAL:
                    self.goal = (x, y)

    def gotoxy(self, x, y):
        print("%c[%d;%df" % (0x1B, y, x), end='')

    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def addAgent(self, agent):
        agent.Start(self)
        agent.Draw()
        self.agents.append(agent);

    def run(self):
        while (True):
            done = 0

            self.draw()
            for agent in self.agents:
                if agent.Done():
                    done += 1
                else:
                    agent.Update()

                agent.Draw()

            if done == len(self.agents):
                break

            sleep(SLEEP)

    def draw(self):
        self.clear()
        for y in range(0, self.height):
            for x in range(0,self.width):
                print(self.level[y][x],end="")
            print("")

class Robot:
    def __init__(self, genes):
        self.x = 0
        self.y = 0
        self.dir = UP
        self.color = '\033[95m'
        self.genes = genes
        self.curr_action = 0

    def Done(self):
        return self.curr_action >= len(self.genes)

    def Start(self, simulation):
        self.x = simulation.home[0]
        self.y = simulation.home[0]
        self.simulation = simulation

    def Move(self, direction):
        dx = self.x
        dy = self.y

        if (direction == UP):
            dy -= 1
            self.dir = UP
        elif (direction == DOWN):
            dy += 1
            self.dir = DOWN
        elif (direction == LEFT):
            dx -= 1
            self.dir = LEFT
        elif (direction == RIGHT):
            dx += 1
            self.dir = RIGHT

        if (self.simulation.level[dy][dx] in (EMPTY, HOME, GOAL)):
            self.x = dx
            self.y = dy

    def Draw(self):
        print("%c[%d;%df" % (0x1B, self.y+1, self.x+1), end='')
        print(self.dir)

    def Update(self):
        self.Move(self.genes[self.curr_action]);
        self.curr_action += 1

    def GetDistance(self):
        dx = abs(self.x - self.simulation.goal[0])
        dy = abs(self.y - self.simulation.goal[1])
        dist = dx + dy
        return dist

###################### Seu trabalho inicia aqui ###############################
# Esse Ã© o desenho do seu level
level = [
    [WALL,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,HOME ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,GOAL ,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,WALL ,EMPTY,EMPTY,EMPTY,WALL],
    [WALL,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL ,WALL]
]

# O robÃ´ recebe como parÃ¢metro os movimentos (DNA)
# Use um tamanho de DNA apropriado.
robot1 = Robot([RIGHT,RIGHT,RIGHT,DOWN,DOWN,RIGHT,RIGHT,RIGHT,RIGHT,RIGHT, UP, UP])
robot2 = Robot([LEFT,LEFT,LEFT,RIGHT,RIGHT,RIGHT,UP,UP,UP,DOWN,DOWN,DOWN])

simulation = Simulation(level)
simulation.addAgent(robot1)
simulation.addAgent(robot2)
simulation.run()

print("DistÃ¢ncia do robot1 atÃ© o objetivo: ", robot1.GetDistance())
print("DistÃ¢ncia do robot2 atÃ© o objetivo: ", robot2.GetDistance())