import collections
import copy
import random
import numpy as np

from maps import Maps

class QLearning(object):

    def __init__(self, iterations = 10000, maps = "small_map.txt", ghostsPosition = set([(5, 3)]), treasuresPosition = [(1, 7), (6, 0)]):

        # initialize the map for path search
        self.maps = Maps(filename = maps, ghostsPosition = set(ghostsPosition), treasuresPosition = list(treasuresPosition))

        # set default value for q-table to be 0 in all four directions
        self.q_table = collections.defaultdict(lambda: [0, 0, 0, 0])
        self.iterations = iterations

        # record setting for the map
        self.file = maps
        self.g = ghostsPosition
        self.t = treasuresPosition
        
        # q-learning parameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.2

        # define search space
        self.action_space = [[0, 1], [1, 0], [0, -1], [-1, 0]]


    # train a q-learning agent
    def train(self):

        for _ in range(self.iterations):

            # initialize a new map with same parameter settings
            state = Maps(filename = self.file, ghostsPosition = set(self.g), treasuresPosition = list(self.t))

            reward = 0
            done = False

            # flatten state for hashmaps
            flatten_state = state.returnFlatten()

            while not done:

                # epilson defines how "explorative" the agent is
                if random.random() < self.epsilon:
                    action = random.randint(0, 3)
                else:
                    action = np.argmax(self.q_table[flatten_state])
                
                # feedback from the map
                reward, done = state.getReward(self.action_space[action])
                next_flatten = state.returnFlatten()
                
                old_value = self.q_table[flatten_state][action]
                next_max = np.max(self.q_table[next_flatten])

                # update the q table
                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[flatten_state][action] = new_value
                flatten_state = next_flatten


    # move a trained agent
    def move(self):

        done = False
        record = []
        moves = []
        
        while not done:

            # acquire the best move from q_table
            flatten_state = self.maps.returnFlatten()
            action = np.argmax(self.q_table[flatten_state])
            
            x, y = self.maps.player
            dx, dy = self.action_space[action]
            
            # check whether agent is still in-bound
            if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0]) and not self.maps.nearGhost(x + dx, y + dy) and self.maps.maps[x + dx][y + dy] != 1:

                # remove the treasure if it's reached
                if (x + dx, y + dy) in self.maps.treasures:
                    self.maps.treasures.remove((x + dx, y + dy))
                    self.maps.maps[x + dx][y + dy] = 0    

                moves.append((x + dx, y + dy))
                if len(moves) > 50: return -1, [] # stuck in loop

                # updates the agent
                self.maps.move(x + dx, y + dy)
                self.maps.updateGhost()
                record.append(copy.deepcopy(self.maps.maps))
                
                if not self.maps.treasures: break
            else:
                return -1, []
                
        self.maps = Maps(filename = self.file, ghostsPosition = set(self.g), treasuresPosition = list(self.t))
        return moves, record