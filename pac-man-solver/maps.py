import random
from functools import reduce


class Maps(object):

    def __init__(self, filename="default_map.txt", player=[0, 0], numGhosts = 10, numTeasures = 5):
        self.maps = []

        with open(filename, "r") as file:
            for line in file:
                self.maps.append(list(map(int, line.replace('\n', '').split(','))))

        self.player = player
        self.ghosts = set(random.sample([(x, y) for x in range(len(self.maps)) for y in range(
            len(self.maps[0])) if self.maps[x][y] != 1], numGhosts))
        self.teasures = random.sample([(x, y) for x in range(len(self.maps)) for y in range(len(self.maps[0])) if self.maps[x][y] != 1 and (x, y) not in self.ghosts and (x, y) != self.player], numTeasures)

        for x, y in self.ghosts:
            self.maps[x][y] = 3
        
        for x, y in self.teasures:
            self.maps[x][y] = 4
        
        self.maps[self.player[0]][self.player[1]] = 2
        self.flatten = lambda x, y: x + y


    def nearGhost(self, x, y):
        return any([self.maps[x + dx][y + dy] == 3 for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]] if 0 <= x + dx < len(self.maps) and 0 <= y + dy < len(self.maps[0])])


    def updateGhost(self):
        visited = set()
        for i, j in self.ghosts:

            directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            random.shuffle(directions)

            for di, dj in directions:
                if 0 <= i + di < len(self.maps) and 0 <= j + dj < len(self.maps[0]) and self.maps[i + di][j + dj] == 0:
                    self.maps[i][j], self.maps[i + di][j + dj] = self.maps[i + di][j + dj], self.maps[i][j]
                    visited.add((i + di, j + dj))
                    break

        self.ghosts = visited


    def returnFlatten(self):
        return tuple(reduce(self.flatten, self.maps))


    def returnPartial(self, d):
        observed = []
    
        d //= 2
        x, y = self.player

        for dx in range(-d, d + 1):
            temp = []
            if 0 <= x + dx < len(self.maps):
                for dy in range(-d, d + 1):
                    if 0 <= y + dy < len(self.maps[0]):
                        temp.append(self.maps[x + dx][y + dy])
                    else:
                        temp.append(1)
            else:
                temp = [1] * (d * 2 + 1)

            observed.append(temp)

        return observed


    def returnPartialFlatten(self, d):
        return tuple(reduce(self.flatten, self.returnPartial(d)))


    def move(self, x, y):
        self.maps[x][y], self.maps[self.player[0]][self.player[1]] = 2, 0
        self.player = [x, y]


    def draw(self):
        plt.imshow(self.maps)
        plt.show()
