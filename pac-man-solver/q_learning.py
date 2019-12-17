import collections
import copy
import random
import numpy as np

from maps import Maps


class QLearning(object):

    def __init__(self, dimension = 3, iterations = 10000):
        self.maps = Maps()
        self.q_table = collections.defaultdict(lambda: [0, 0, 0, 0])
        self.iterations = 10000

        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1

        self.action_space = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.d = 3


    def train(self):

        for _ in range(self.iterations):

            state = Maps()                        
            penalities, reward = 0, 0
            done = False
            flatten_state = state.returnPartialFlatten(self.d)

            while not done:
        
                if random.random() < self.epsilon:
                    action = random.randint(0, 3)
                else:
                    action = np.argmax(self.q_table[flatten_state])
                
                reward, done = state.getReward(self.action_space[action])
                next_flatten = state.returnPartialFlatten(self.d)
                
                old_value = self.q_table[flatten_state][action]
                next_max = np.max(self.q_table[next_flatten])
                
                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[flatten_state][action] = new_value
                
                flatten_state = next_flatten


    def move(self):

        done = False
        record = []

        while not done:
            flatten_state = self.maps.returnPartialFlatten(self.d)
            action = np.argmax(self.q_table[flatten_state])
            
            x, y = start
            dx, dy = self.action_space[action]
            
            if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0]) and not self.nearGhost(x + dx, y + dy) and self.maps.maps[x + dx][y + dy] != 1:
                if (x + dx, y + dy) in self.maps.treasures:
                    self.maps.treasures.remove((x + dx, y + dy))
                    state[x + dx][y + dy] = 0
                    
                self.maps.maps[x][y], self.maps.maps[x + dx][y + dy] = self.maps.maps[x + dx][y + dy], self.maps.maps[x][y]
                self.maps.updateGhost()
                start = (x + dx, y + dy)
                record.append(copy.deepcopy(self.maps.maps))
                
                if not self.maps.treasures: break
            else:
                break

        return record