import random
import math
import numpy as np
import time


class Environment:

    def __init__(self):
        self.environmentMap = self.createEnvironmentMap()
        self.possibleActions = self.createPossibleActions()
        self.enterReward = self.createEnterReward()
        self.currentX = 0
        self.currentY = 0
        self.stepNUm = 0
        self.bb = True

    def move(self):
        self.environmentMap[self.currentX][self.currentY] = '.'
        self.environmentMap[0][0] = 'S'
        self.environmentMap[9][9] = 'D'
        possibleAction = list(self.possibleActions[self.currentX][self.currentY])
        random.shuffle(possibleAction)
        rewards = [self.rewardfunction(self.currentX, self.currentY, i) for i in possibleAction]
        action = possibleAction[np.argmax(rewards)]
        self.enterReward[self.currentX][self.currentY] /= 1.35
        self.stepNUm += 1
        if action == 'L':
            self.currentY = self.currentY - 1
        elif action == 'U':
            self.currentX = self.currentX - 1
        elif action == 'R':
            self.currentY = self.currentY + 1
        elif action == 'D':
            self.currentX = self.currentX + 1
        self.environmentMap[self.currentX][self.currentY] = 'X'
        if self.currentX == 9 and self.currentY == 9:
            self.bb = False
        if self.environmentMap[self.currentX][self.currentY] == 'O':
            self.currentX = 0
            self.currentY = 0
        return 1


    def createEnvironmentMap(self):
        environmentMap = [["." for i in range(10)] for j in range(10)]
        for i in range(15):
            environmentMap[random.choice(range(10))][random.choice(range(10))] = '#'
            environmentMap[random.choice(range(10))][random.choice(range(10))] = 'O'
        environmentMap[0][0] = 'S'
        environmentMap[9][9] = 'D'
        return environmentMap

    def createPossibleActions(self):
        possibleActions = [["LURD" for i in range(10)] for j in range(10)]
        possibleActions[0] = ["LRD" for i in range(0, 10)]
        possibleActions[9] = ["LUR" for i in range(0, 10)]
        for i in range(10):
            possibleActions[i][0] = "URD"
        for i in range(10):
            possibleActions[i][9] = "LUD"
        possibleActions[0][0] = 'RD'
        possibleActions[0][9] = 'LD'
        possibleActions[9][0] = 'UR'
        possibleActions[9][9] = 'LU'
        return possibleActions

    def createEnterReward(self):
        enterReward = [["0" for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                if self.environmentMap[i][j] in ['.', 'S', 'D']:
                    enterReward[i][j] = 100 - self.calculateDistance(i, j)
                elif self.environmentMap[i][j] == 'O':
                    enterReward[i][j] = -20
                else:
                    enterReward[i][j] = -10
        return enterReward

    def rewardfunction(self, agentXcordinate, agentYcordinate, action):
        if action == 'L':
            reward = self.enterReward[agentXcordinate][agentYcordinate - 1]
        elif action == 'U':
            reward = self.enterReward[agentXcordinate - 1][agentYcordinate]
        elif action == 'R':
            reward = self.enterReward[agentXcordinate][agentYcordinate + 1]
        elif action == 'D':
            reward = self.enterReward[agentXcordinate + 1][agentYcordinate]
        else:
            print('not valid action')
            return math.inf
        return reward

    def calculateDistance(self, ax, ay, bx=9, by=9):
        return 5 * (abs(ax - bx) + abs(ay - by))

    def printEnvironmentMap(self):
        print('Main map of Environment:')
        print('\'.\':empty locations that agent is able to locate it')
        print('\'S\':Start location of the agent')
        print('\'D\':Destination location of the agent')
        print('\'#\':Block location of the environment(random selection in each compile)')
        print('\'O\':Terminal state location of the agent(random selection in each compile)\n')
        print('\n'.join(['    '.join(['{:4}'.format(item) for item in row]) for row in self.environmentMap]))
        print('\n\n')

    def printMap(self):
        print('\n\n')
        print('steps:' + str(self.stepNUm))
        print('\n'.join(['    '.join(['{:4}'.format(item) for item in row]) for row in self.environmentMap]))
        print('\n\n')

    def printPossibleActions(self):
        print('Possible action in each element:\n')
        print('\n'.join(['    '.join(['{:4}'.format(item) for item in row]) for row in self.possibleActions]))
        print('\n\n')

    def printEnterReward(self):
        print('Reward for entering each element:\n')
        print('\n'.join(['    '.join(['{:4}'.format(item) for item in row]) for row in self.enterReward]))
        print('\n\n')


class Agent:
    def __init__(self, name, environment):
        self.name = name
        self.environment = environment


print('Welcome to the routing Environment..\n\n')

# create an agent that name is Ebi and get it an environment as a parameter
agent = Agent('Ebi', Environment())

# print the main environment map
agent.environment.printEnvironmentMap()

# print all the possible actions that agent can do in the environment
agent.environment.printPossibleActions()

# print all the entering reward of each element
agent.environment.printEnterReward()

print('\nsample test for reward function')
print(
    'the reward for agent in 0 0 location that want to go Down is ' + str(agent.environment.rewardfunction(0, 0, 'D')))
print(
    'the reward for agent in 1 1 location that want to go Right is ' + str(agent.environment.rewardfunction(1, 1, 'R')))
print('the reward for agent in 4 0 location that want to go Up is ' + str(agent.environment.rewardfunction(4, 0, 'U')))

# start agent from the beginning as the '@'
input('press any key to continue...')
while agent.environment.bb:
    agent.environment.move()
    agent.environment.printMap()
    time.sleep(1)

print('you win...')

