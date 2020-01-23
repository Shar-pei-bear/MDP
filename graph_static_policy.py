from graphworld import *
import math

initial = 17  # 0
targets = [7]  # 7
num_obstacles = 1
task_type = 'sequential'
network_file = 'network_topology'
T = 0
N = math.factorial(20)/math.factorial(20 - num_obstacles)/math.factorial(num_obstacles)
obstacles_indexes = np.random.choice(range(N), (100, 19))
np.save('obstacles_indexes', obstacles_indexes)
gwg = GraphworldGui(network_file, initial, targets, num_obstacles, T, task_type)
# graph_static_policies = np.zeros([gwg.mdp.horizon, len(gwg.mdp.states)])
#
# for time_index in range(gwg.mdp.horizon):
#     gwg.mdp.obstacles = obstacles[time_index, :]
#     gwg.mdp.update_reward()
#     print 'time index is ', time_index
#     for state_index in gwg.mdp.states:
#         gwg.mdp.update_alpha(state_index)
#         x = gwg.mdp.primal_linear_program()
#         temp = np.argmax(x, axis=2)
#         graph_static_policies[time_index, state_index] = temp[0, state_index]
# np.save('graph_static_policies', graph_static_policies)
