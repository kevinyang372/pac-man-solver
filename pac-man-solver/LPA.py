import collections
import heapq
import copy

from maps import Maps

class LPA(object):

    def __init__(self, maps = "small_map.txt", ghostsPosition = None, treasuresPosition = None):

        # initialize map
        if maps == "small_map.txt":
            self.maps = Maps(filename = maps, ghostsPosition = ghostsPosition, treasuresPosition = treasuresPosition)
        else:
            self.maps = Maps()

        self.treasures = collections.deque(self.maps.treasures)

        # define the heuristics
        self.heuristic = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
        self.expanded_frontier = 0


    # initialize a new LPA* search
    def initialize(self, start, goal):

        self.queue = []
        self.g = {}
        self.rhs = {}

        self.start = start
        self.goal = goal

        # set the rhs value of starting node as 0
        self.rhs[start] = 0

        # search from the start node
        self.queue.append((self.calculate_key(self.start), self.start))

        # remember the current graph for later changing edge weight updates
        self.memory = copy.deepcopy(self.maps.maps)


    # calculate the priority of a node
    def calculate_key(self, node):
        c = min(self.g.get(node, float('inf')), self.rhs.get(node, float('inf')))
        return (c + self.heuristic(node, self.goal), c)


    # compute the shortest path
    def computeShortestPath(self):

        # continue unitl exhausted the queue (not found) or local inconsistency is solved for the goal (found)
        while (self.queue and self.queue[0][0] < self.calculate_key(self.goal)) or (self.rhs.get(self.goal, float('inf')) != self.g.get(self.goal, float('inf'))):

            _, node = heapq.heappop(self.queue)
            self.expanded_frontier += 1
            
            # local inconsistency
            if self.g.get(node, float('inf')) > self.rhs.get(node, float('inf')):
                
                # solve inconsistency
                self.g[node] = self.rhs.get(node, float('inf'))

                # update vertex of its neighors
                for neighbor in self.getNeighbors(node):
                    self.updateNode(neighbor)
            else:
                # if no local inconsistency, update the vertex of neighbors and the node
                self.g[node] = float('inf')
                self.updateNode(node)

                for neighbor in self.getNeighbors(node):
                    self.updateNode(neighbor)
        
        # reconstruct the path
        if self.g.get(self.goal) == float('inf'):
            return None
        else:
            # back-track with lowest g + edge cost 
            temp = self.goal
            path = [self.goal]
            while temp != self.start:
                temp = min(self.getNeighbors(temp), key = lambda x: self.cost(x, temp) + self.g.get(x, float('inf')))
                path.append(temp)
            path.pop()
            return path


    # find neighbors of a node
    def getNeighbors(self, node):
        return [(node[0] + dx, node[1] + dy) for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]] if 0 <= node[0] + dx < len(self.maps.maps) and 0 <= node[1] + dy < len(self.maps.maps[0])]


    # compute edge weight - inf if one of the node is a ghost or obstacle
    def cost(self, n1, n2):
        return float('inf') if self.maps.maps[n1[0]][n1[1]] in [1, 3] or self.maps.maps[n2[0]][n2[1]] in [1, 3] else 1


    # update vertex
    def updateNode(self, node):
        if node != self.start:
            # set rhs to be one step look ahead value of the lowest neighbors
            self.rhs[node] = float('inf')
            for neighbor in self.getNeighbors(node):
                self.rhs[node] = min(self.rhs[node], self.g.get(neighbor, float('inf')) + self.cost(neighbor, node))

        # remove node from queue if exist
        for ind in range(len(self.queue)):
            if self.queue[ind][1] == node:
                self.queue.pop(ind)
                heapq.heapify(self.queue)
                break

        # push back for update if locally inconsistent
        if self.g.get(node, float('inf')) != self.rhs.get(node, float('inf')):
            heapq.heappush(self.queue, (self.calculate_key(node), node))


    # scan for changing edge weights
    def scan(self):
        l = []
        for i in range(len(self.maps.maps)):
            for j in range(len(self.maps.maps[0])):
                if self.maps.maps[i][j] != self.memory[i][j]:
                    l.append((i, j))
                self.memory[i][j] = self.maps.maps[i][j]
        return l
    

    # solver
    def LPA(self):
        
        record = []
        moves = []

        while self.treasures:
            
            # initialize the search
            self.initialize(tuple(self.maps.player), self.treasures.pop())

            while True:
                p = self.computeShortestPath()
                
                if not p: return -1, None
                
                while self.start != self.goal:
                    next = p.pop()
                    
                    if self.maps.maps[next[0]][next[1]] in [1, 3]:
                        break
                    
                    moves.append(next)
                    self.maps.updateGhost()
                    self.maps.move(next[0], next[1])
                    self.start = (next[0], next[1])
                    record.append(copy.deepcopy(self.maps.maps))
                
                if self.start == self.goal:
                    break
                else:
                    # scan for edge weight changes to update path
                    changed = self.scan()
                    for node in changed:
                        self.updateNode(node)
                    
        return moves, record