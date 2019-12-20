# a* solver
import heapq
import collections
import copy

from maps import Maps

class Astar(object):

    def __init__(self, maps = "small_map.txt", ghostsPosition = None, treasuresPosition = None):

        # initialize map
        if maps == "small_map.txt":
            self.maps = Maps(filename = maps, ghostsPosition = ghostsPosition, treasuresPosition = treasuresPosition)
        else:
            self.maps = Maps()

        self.treasures = self.maps.treasures
        self.expanded_frontier = 0


    # astar algorithm
    def astar(self, maps, start, end):

        cost = {}
        cost[start[0], start[1]] = 0
        
        # set all the nearby area of a ghost as obstacles
        # this avoids the possibility of agent colliding with ghost
        gp = [(x, y) for x in range(len(maps)) for y in range(len(maps[0])) if maps[x][y] == 3]
        gn = set()

        for x, y in gp:
            for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]:
                gn.add((dx + x, dy + y))
        
        # defines the manhattan as the heuristics
        def manhattan(x, y):
            return abs(x[0] - y[0]) + abs(x[1] - y[1])
        
        # initialize the frontier
        d = [(manhattan(start, end), 0, start[0], start[1], [])]

        while d:

            # expands the node with smallest f-value
            fx, cx, x, y, past = heapq.heappop(d)
            self.expanded_frontier += 1
            
            if (x, y) == end: return past + [(x, y)]
            
            # search the neighbors of the expanded node
            for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                if 0 <= x + dx < len(maps) and 0 <= y + dy < len(maps[0]) and (x + dx, y + dy) not in gn and maps[x + dx][y + dy] != 1 and maps[x + dx][y + dy] != 3 and cx + 1 < cost.get((x + dx, y + dy), float('inf')):
                    new = manhattan([x + dx, y + dy], end) + cx + 1
                    cost[x + dx, y + dy] = cx + 1
                    heapq.heappush(d, (new, cx + 1, x + dx, y + dy, past + [(x, y)]))
        
        return None


    # solver
    def astar_solve(self):

        queue = collections.deque(self.treasures)
        res = []
        moves = []
        
        # continue until finding all the treasures
        while queue:

            # initialize the path
            path = self.astar(self.maps.maps, self.maps.player, queue[0])

            # if path not found, the agent stops
            if not path: return -1, None

            path.reverse()
            path.pop()
            
            # continue until finish the path
            while path:
                
                self.maps.updateGhost()
                next = path.pop()

                # replanning
                if self.maps.nearGhost(next[0], next[1]):
                    path = self.astar(self.maps.maps, self.maps.player, queue[0])

                    if not path: return -1, None

                    path.reverse()
                    path.pop()
                    next = path.pop()
                   
                self.maps.move(next[0], next[1])
                moves.append(next)
                
                res.append(copy.deepcopy(self.maps.maps))
                
            queue.popleft()
            
        return moves, res