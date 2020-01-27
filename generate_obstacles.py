from graphworld import *
import math

# graph_static_policies = np.load('data/graph_static_policies.npy')
# print graph_static_policies.shape

num_obstacles = 3
T = 3
visualization = False
decoys_set = [0, 12, 2, 8, 1, 13, 15, 10, 9, 5]
obstacles_combo = list(itertools.combinations(range(20), num_obstacles))
random.shuffle(obstacles_combo)
obstacles_combo = np.asarray(obstacles_combo)
np.save('obstacles_combo', obstacles_combo)

N = math.factorial(10)/math.factorial(10 - num_obstacles)/math.factorial(num_obstacles)
obstacles_indexes = np.random.choice(range(N), (100, 7))
obstacles_indexes = np.repeat(obstacles_indexes, 3, axis=1)
obstacles_indexes = obstacles_indexes[:, 0:19]
np.save('obstacles_indexes', obstacles_indexes)
