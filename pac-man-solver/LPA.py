import collections
import heapq
import copy

from maps import Maps

class LPA(object):

    def __init__(self):
        self.maps = Maps()
        self.treasures = collections.deque(self.maps.treasures)

        self.heuristic = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

    def initialize(self, start, goal):

        self.queue = []
        self.g = {}
        self.rhs = {}

        self.start = start
        self.goal = goal
        self.rhs[start] = 0

        self.queue.append((self.calculate_key(self.start), self.start))
        self.memory = copy.deepcopy(self.maps.maps)

    def calculate_key(self, node):
        c = min(self.g.get(node, float('inf')), self.rhs.get(node, float('inf')))
        return (c + self.heuristic(node, self.goal), c)

    def computeShortestPath(self):
        while (self.queue and self.queue[0][0] < self.calculate_key(self.goal)) or (self.rhs.get(self.goal, float('inf')) != self.g.get(self.goal, float('inf'))):
            _, node = heapq.heappop(self.queue)
            
            if self.g.get(node, float('inf')) > self.rhs.get(node, float('inf')):
                self.g[node] = self.rhs.get(node, float('inf'))

                for neighbor in self.getNeighbors(node):
                    self.updateNode(neighbor)
            else:
                self.g[node] = float('inf')
                self.updateNode(node)

                for neighbor in self.getNeighbors(node):
                    self.updateNode(neighbor)
        
        if self.g.get(self.goal) == float('inf'):
            return None
        else:
            temp = self.goal
            path = [self.goal]
            while temp != self.start:
                temp = min(self.getNeighbors(temp), key = lambda x: self.cost(x, temp) + self.g.get(x, float('inf')))
                path.append(temp)
            return path

    def getNeighbors(self, node):
        return [(node[0] + dx, node[1] + dy) for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]] if 0 <= node[0] + dx < len(self.maps.maps) and 0 <= node[1] + dy < len(self.maps.maps[0])]

    def cost(self, n1, n2):
        return float('inf') if self.maps.maps[n1[0]][n1[1]] in [1, 3] or self.maps.maps[n2[0]][n2[1]] in [1, 3] else 1

    def updateNode(self, node):
        if node != self.start:
            self.rhs[node] = float('inf')
            for neighbor in self.getNeighbors(node):
                self.rhs[node] = min(self.rhs[node], self.g.get(neighbor, float('inf')) + self.cost(neighbor, node))

        for ind in range(len(self.queue)):
            if self.queue[ind][1] == node:
                self.queue.pop(ind)
                heapq.heapify(self.queue)
                break

        if self.g.get(node, float('inf')) != self.rhs.get(node, float('inf')):
            heapq.heappush(self.queue, (self.calculate_key(node), node))

    def scan(self):
        l = []
        for i in range(len(self.maps.maps)):
            for j in range(len(self.maps.maps[0])):
                if self.maps.maps[i][j] != self.memory[i][j]:
                    l.append((i, j))
                self.memory[i][j] = self.maps.maps[i][j]
        return l
    
    def LPA(self):
        
        record = []
        while self.treasures:
            self.initialize(tuple(self.maps.player), self.treasures.pop())
            while True:
                p = self.computeShortestPath()
                
                if not p:
                    self.maps.updateGhost()
                    changed = self.scan()
                    for node in changed:
                        self.updateNode(node)
                    continue
                
                while self.start != self.goal:
                    next = p.pop()
                    
                    if self.maps.maps[next[0]][next[1]] in [1, 3]:
                        break
                    
                    self.maps.updateGhost()
                    self.maps.move(next[0], next[1])
                    self.start = (next[0], next[1])
                    record.append(copy.deepcopy(self.maps.maps))
                
                if self.start == self.goal:
                    break
                else:
                    changed = self.scan()
                    for node in changed:
                        self.updateNode(node)
                    
        return record