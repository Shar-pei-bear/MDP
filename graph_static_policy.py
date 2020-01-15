from graphworld import *
initial = 0
nstates = 8

obstacles = np.load('obstacles.npy')
targets_path = [[7, 7, 7, 7, 7, 7, 7]]
task_type ='sequential'
edges = [[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7)],
         [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)]]
actlist = ['a1', 'a2', 'a3', 'a4']
gwg = GraphworldGui(initial, nstates, edges, actlist, targets_path, obstacles,  task_type)

ut = np.zeros([gwg.mdp.horizon, len(gwg.mdp.states)])
graph_static_policies = np.zeros([gwg.mdp.horizon, len(gwg.mdp.states)])

for time_index in range(gwg.mdp.horizon):
    gwg.mdp.obstacles = obstacles[time_index, :]
    gwg.mdp.update_reward()
    print 'time index is ', time_index
    for state_index in gwg.mdp.states:
        gwg.mdp.update_alpha(state_index)
        x = gwg.mdp.primal_linear_program()
        temp = np.argmax(x, axis=2)
        graph_static_policies[time_index, state_index] = temp[0, state_index]
np.save('graph_static_policies', graph_static_policies)
