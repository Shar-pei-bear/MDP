from graphworld import *
import math

graph_static_policies = np.load('data/graph_static_policies.npy')
print graph_static_policies.shape
# initial = 17  # 0
# targets = [7]  # 7
# num_obstacles = 1
# task_type = 'sequential'
# network_file = 'network_topology'
# T = 0
# obstacles_combo = list(itertools.combinations(range(20), num_obstacles))
# random.shuffle(obstacles_combo)
# obstacles_combo = np.asarray(obstacles_combo)
# np.save('obstacles_combo_1', obstacles_combo)
#
# N = math.factorial(20)/math.factorial(20 - num_obstacles)/math.factorial(num_obstacles)
# obstacles_indexes = np.random.choice(range(N), (100, 19))
# np.save('obstacles_indexes_1', obstacles_indexes)
# gwg = GraphworldGui(network_file, initial, targets, num_obstacles, T, task_type)
# graph_static_policies = np.zeros([100, gwg.mdp.horizon, gwg.nstates])
# data_index = 0
# for index in range(100):
#     flag = True
#     for time_index in range(gwg.mdp.horizon):
#         obstacles_index = obstacles_indexes[index, time_index]
#         obstacles = obstacles_combo[obstacles_index]
#         gwg.mdp.obstacles = np.ones((gwg.horizon, num_obstacles), dtype=np.int) * obstacles
#         gwg.mdp.update_reward()
#         print 'time index is ', time_index
#         for state_index in gwg.mdp.states:
#             gwg.mdp.update_alpha(state_index)
#             sol = gwg.mdp.primal_linear_program()
#             if sol['status'] == 'optimal':
#                 x = np.array(sol['z']).reshape((gwg.horizon, gwg.nstates, gwg.action_number))
#             else:
#                 flag = False
#                 break
#             temp = np.argmax(x, axis=2)
#             graph_static_policies[data_index, time_index, state_index] = temp[0, state_index]
#     if flag:
#         data_index = data_index + 1
# graph_static_policies = graph_static_policies[0:data_index, :, :]
# np.save('graph_static_policies', graph_static_policies)
