# a* solver
import heapq
import collections
import copy

from maps import Maps

class Astar(object):

    def __init__(self):
        self.maps = Maps()
        self.treasures = self.maps.treasures


    def astar(self, maps, start, end):
        cost = {}
        cost[start[0], start[1]] = 0
        
        gp = [(x, y) for x in range(len(maps)) for y in range(len(maps[0])) if maps[x][y] == 3]
        gn = set()
        for x, y in gp:
            for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]:
                gn.add((dx + x, dy + y))
        
        def manhattan(x, y):
            return abs(x[0] - y[0]) + abs(x[1] - y[1])
        
        d = [(manhattan(start, end), 0, start[0], start[1], [])]
        while d:
            fx, cx, x, y, past = heapq.heappop(d)
            
            if (x, y) == end: return past + [(x, y)]
            
            for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                if 0 <= x + dx < len(maps) and 0 <= y + dy < len(maps[0]) and (x + dx, y + dy) not in gn and maps[x + dx][y + dy] != 1 and maps[x + dx][y + dy] != 3 and cx + 1 < cost.get((x + dx, y + dy), float('inf')):
                    new = manhattan([x + dx, y + dy], end) + cx + 1
                    cost[x + dx, y + dy] = cx + 1
                    heapq.heappush(d, (new, cx + 1, x + dx, y + dy, past + [(x, y)]))
        
        return None


    def astar_solve(self):

        queue = collections.deque(self.treasures)
        res = []
        c = 0
        
        while queue:

            path = self.astar(self.maps.maps, self.maps.player, queue[0])

            while not path:
                print("No path found. Waiting...")
                self.maps.updateGhost()
                res.append(copy.deepcopy(self.maps.maps))
                path = self.astar(self.maps.maps, self.maps.player, queue[0])

            path.reverse()
            path.pop()
            
            while path:
                
                self.maps.updateGhost()
                next = path.pop()

                if self.maps.nearGhost(next[0], next[1]):
                    path = self.astar(self.maps.maps, self.maps.player, queue[0])

                    if not path:
                        print("No path found. Waiting...")
                        res.append(copy.deepcopy(self.maps.maps))
                        c += 1
                        continue

                    path.reverse()
                    path.pop()
                    next = path.pop()
                   
                self.maps.move(next[0], next[1])
                c += 1
                
                res.append(copy.deepcopy(self.maps.maps))
                
            queue.popleft()
            
        return c, res