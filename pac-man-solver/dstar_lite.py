import collections

from maps import Maps

class DstarLite(object):

    def __init__(self):
        self.maps = Maps()
        self.treasures = collections.deque(self.maps.treasures)

        self.graph = {}
        self.heuristics = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
        self.cost = lambda x, y: float('inf') if any([self.graph[x] == 1, self.graph[y] == 1]) else 1

        self.scan()
        self.setGoal()

    def scan(self):
        res = []
        for i in range(len(self.maps.maps)):
            for j in range(len(self.maps.maps)):
                origin = self.graph.get((i, j), -1)
                if self.maps.maps[i][j] == 1:
                    self.graph[i, j] = 1
                elif self.maps.maps[i][j] == 3:
                    for di, dj in range([0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]):
                        if 0 <= i + di < len(self.maps.maps) and 0 <= j + dj < len(self.maps.maps[0]):
                            self.graph[i + di, j + dj] = 1
                else:
                    self.graph[i, j] = max(0, self.graph.get((i, j), 0))

                if origin != self.graph[i, j]: res.append((i, j))

        return res

    def setGoal(self):
        self.g = {}
        self.rhs = {}
        self.km = 0

        self.goal = self.treasures.popleft()
        self.rhs[self.goal] = 0

        self.frontier = [(self.calculateKey(self.goal), self.goal)]
        self.back_pointers = {}
        self.back_pointers[self.goal] = None

    def calculateKey(self, node):
        f1 = min([self.g[node], self.rhs[node]])
        return f1 + self.heuristics(node, self.maps.player) + self.km, f1

    def compute_shortest_path(self):
        last_nodes = collections.deque(maxlen=10)
        while self.frontier[0][0] < self.calculate_key(self.maps.player) or self.rhs.get(self.maps.player, float('inf')) != self.g.get(self.maps.player, float('inf')):

            k_old, node = self.frontier.pop()
            last_nodes.append(node)

            if len(last_nodes) == 10 and len(set(last_nodes)) < 3:
                raise Exception("Fail! Stuck in a loop")

            k_new = self.calculate_key(node)
            if k_old < k_new:
                heapq.heappush(self.frontier, (k_new, node))
            elif self.g.get(node, float('inf')) > self.rhs.get(node, float('inf')):
                self.g[node] = self.rhs.get(node, float('inf'))
                self.update_nodes(self.graph.neighbors(node))
            else:
                self.g[node] = float('inf')
                self.update_nodes(self.graph.neighbors(node) + [node])

        return self.back_pointers.copy(), self.G_VALS.copy()

    def updateNeighbors(node):

        x, y = node

        for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0]):
                curr = (x + dx, y + dy)

                if self.rhs.get()

    def getNeighobrs(node):
        x, y = node
        return [(x + dx, y + dy) for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]] if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0])]

    def getAllNeighbors(node):
        x, y = node
        return [(x + dx, y + dy) for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1]] if 0 <= x + dx < len(self.maps.maps) and 0 <= y + dy < len(self.maps.maps[0])]


    def dLite(self):
        self.setGoal()
        self.compute_shortest_path()
        last = self.maps.player

        while self.maps.player != self.goal:

            next = min(self.getNeighobrs(self.maps.player), key = lambda x: self.cost(x, self.maps.player) + self.g.get(x, float('inf')))
            self.maps.move(next[0], next[1])

            changed = self.scan()
            if changed:
                km += self.heuristics(self.maps.player, last)
                last = self.maps.player




