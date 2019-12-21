# Pac-Man Solver

Build an intelligent Pac-Man agent using A*, LPA* and Q-Learning.
![Astar solver](demo/astar.gif)

## Example Usage

All algorithms in the repository could be used as a python package. If using custom maps, please save the map as a txt file and input the filename as the parameter.

```python
from astar import Astar
from q_learning import QLearning
from LPA import LPA

# initialize solver class
astar = Astar(ghostsPosition = set([(5, 3)]), treasuresPosition = [(1, 7), (6, 0)])
lpa = LPA(ghostsPosition = set([(5, 3)]), treasuresPosition = [(1, 7), (6, 0)])
qlearner = QLearning(ghostsPosition = set(), iterations = 1000)

# q-learning needs to be trained first
qlearner.train()

# return a solution
path_astar, maps_astar = astar.astar_solve()
path_lpa, maps_lpa = lpa.LPA()
path_q, maps_q = qlearner.move()
```
