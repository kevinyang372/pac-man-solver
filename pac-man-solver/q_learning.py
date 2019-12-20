import collections
import copy
import random
import numpy as np

from maps import Maps


class QLearning(object):

    def __init__(self, dimension = 4, iterations = 10000, maps = "small_map.txt", ghostsPosition = set([(5, 3)]), treasuresPosition = [(1, 7), (6, 0)]):
        self.maps = Maps(filename = maps, ghostsPosition = set(ghostsPosition), treasuresPosition = list(treasuresPosition))
        self.q_table = collections.defaultdict(lambda: [0, 0, 0, 0])
        self.iterations = iterations

        self.file = maps
        self.g = ghostsPosition
        self.t = treasuresPosition
        
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.2

        self.action_space = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.d = dimension


    def train(self):

        for _ in range(self.iterations):

            state = Maps(filename = self.file, ghostsPosition = set(self.g), treasuresPosition = list(self.t))

            reward = 0
            done = False
            flatten_state = state.returnFlatten()

            while not done:

                if random.random() < self.epsilon:
                    action = random.randint(0, 3)
                else:
                    action = np.argmax(self.q_table[flatten_state])
                
                reward, done = state.getReward(self.action_space[action])
                next_flatten = state.returnFlatten()
                
                old_value = self.q_table[flatten_state][action]
                next_max = np.max(self.q_table[next_flatten])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[flatten_state][action] = new_value
                flatten_state = next_flatten


    def move(self):

        done = False
        record = []
        moves = []
        
        while not done:
            flatten_state = self.maps.returnFlatten()
            action = np.argmax(self.q_table[flatten_state])
            
            x, y = self.maps.player
            dx, dy = self.action_space[action]
            
            if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0]) and not self.maps.nearGhost(x + dx, y + dy) and self.maps.maps[x + dx][y + dy] != 1:

                if (x + dx, y + dy) in self.maps.treasures:
                    self.maps.treasures.remove((x + dx, y + dy))
                    self.maps.maps[x + dx][y + dy] = 0    

                moves.append((x + dx, y + dy))
                if len(moves) > 50: return -1, [] # stuck in loop

                self.maps.move(x + dx, y + dy)
                self.maps.updateGhost()
                record.append(copy.deepcopy(self.maps.maps))
                
                if not self.maps.treasures: break
            else:
                return -1, []
                
        self.maps = Maps(filename = self.file, ghostsPosition = set(self.g), treasuresPosition = list(self.t))
        return moves, record