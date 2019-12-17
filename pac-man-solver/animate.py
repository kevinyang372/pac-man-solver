from matplotlib import animation, rc
import matplotlib.pyplot as plt
from astar import Astar

_, record = Astar().astar_solve()

fig = plt.figure(figsize = (10, 10))
ax = plt.axes()
img = ax.imshow(record[0])

def init():
    img.set_data(record[0])
    return img,

def animate(i):
    img.set_data(record[i])
    return img,

ani = animation.FuncAnimation(fig, animate, init_func = init, frames = len(record))
ani.save('astar.gif', dpi = 80, writer = 'imagemagick')
