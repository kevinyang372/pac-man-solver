import collections
import copy
import random
import numpy as np

from maps import Maps


class QLearning(object):

    def __init__(self, dimension = 4, iterations = 10000):
        self.maps = Maps()
        self.q_table = collections.defaultdict(lambda: [0, 0, 0, 0])
        self.iterations = iterations

        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.2

        self.action_space = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.d = dimension


    def train(self):

        for i in range(self.iterations):

            state = Maps()                        
            reward = 0
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
        prev = None
        
        while not done:
            flatten_state = self.maps.returnPartialFlatten(self.d)
            action = np.argmax(self.q_table[flatten_state])
            
            x, y = self.maps.player
            dx, dy = self.action_space[action]

            if (x + dx, y + dy) == prev:
                action = np.where(np.argsort(self.q_table[flatten_state]) == 2)[0][0]
                dx, dy = self.action_space[action]
            
            prev = (x, y)
            
            if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0]) and not self.maps.nearGhost(x + dx, y + dy) and self.maps.maps[x + dx][y + dy] != 1:

                if (x + dx, y + dy) in self.maps.treasures:
                    self.maps.treasures.remove((x + dx, y + dy))
                    self.maps.maps[x + dx][y + dy] = 0    

                self.maps.move(x + dx, y + dy)
                self.maps.updateGhost()
                record.append(copy.deepcopy(self.maps.maps))
                
                if not self.maps.treasures: break
            else:
                break

        return record