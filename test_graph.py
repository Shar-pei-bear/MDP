from graphworld import *
import itertools
import random

initial = 0
nstates = 8

# obstacles_combo = list(itertools.combinations(range(nstates), 2))
# random.shuffle(obstacles_combo)
# obstacles_index = np.random.choice(range(len(obstacles_combo)), 30)
# obstacles_index = list(obstacles_index)
# obstacles_combo = np.asarray(obstacles_combo)
# obstacles = obstacles_combo[obstacles_index]
# np.save('obstacles', obstacles)

# obstacles = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
obstacles = np.load('data/obstacles.npy')
print obstacles
targets_path = [[7, 7, 7, 7, 7, 7, 7]]
task_type ='sequential'
edges = [[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7)],
         [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)]]
actlist = ['a1', 'a2', 'a3', 'a4']
gwg = GraphworldGui(initial, nstates, edges, actlist, targets_path, obstacles,  task_type)
gwg.mainloop()




