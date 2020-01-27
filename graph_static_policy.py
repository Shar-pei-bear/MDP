from graphworld import *
import math

# graph_static_policies = np.load('graph_static_policies.npy')
# print graph_static_policies[0, 0, :]

initial = 17  # 0
targets = [7]  # 7
num_obstacles = 3
task_type = 'sequential'
network_file = 'network_topology'
T = 3
decoys_set = [0, 12, 2, 8, 1, 13, 15, 10, 9, 5]
visualization = False
obstacles_combo = np.load('obstacles_combo.npy')
obstacles_indexes = np.load('obstacles_indexes.npy')

gwg = GraphworldGui(network_file, initial, targets, num_obstacles, T, task_type, visualization, decoys_set)
graph_static_policies = np.zeros([10, gwg.mdp.horizon, gwg.nstates])

for data_index in range(10):
    print data_index
    for time_index in range(gwg.horizon):
        obstacles_index = obstacles_indexes[data_index, time_index]
        obstacles = obstacles_combo[obstacles_index]
        gwg.obstacles = obstacles
        gwg.mdp.prob = gwg.getProbs()
        gwg.mdp.obstacles = np.ones((gwg.horizon, num_obstacles), dtype=np.int) * obstacles
        gwg.mdp.update_reward()
        print 'time index is ', time_index
        for state_index in gwg.mdp.states:
            gwg.mdp.update_alpha(state_index)

            sol = gwg.mdp.primal_linear_program()
            if sol['status'] == 'optimal':
                x = np.array(sol['z']).reshape((gwg.horizon, gwg.nstates, gwg.action_number))
                temp = np.argmax(x, axis=2)
                graph_static_policies[data_index, time_index, state_index] = temp[0, state_index]

np.save('graph_static_policies', graph_static_policies)
