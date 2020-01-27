from graphworld import *
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
graph_static_policies = np.load('graph_static_policies.npy')
# static_costs = np.zeros([10, gwg.mdp.horizon + 1, len(gwg.mdp.states)])
#
# # terminal cost is set to zero
# static_costs[:, -1, :] = 0
# static_costs[:, -1, targets[0]] = 1
# for data_index in range(10):
#     print data_index
#     obstacles_index = obstacles_indexes[data_index, :]
#     obstacles = obstacles_combo[obstacles_index]
#     gwg.mdp.obstacles = obstacles
#     gwg.mdp.update_reward()
#     for time_index in reversed(range(gwg.mdp.horizon)):
#         prob = {a: np.eye(gwg.nstates) for a in gwg.actlist}
#         action_index = 0
#         gwg.obstacles = obstacles_combo[obstacles_indexes[data_index, time_index]]
#         for edge in list(gwg.dg.edges()):
#             if (not np.isin(int(edge[0]), gwg.obstacles)) and (not np.isin(int(edge[0]), gwg.targets)):
#                 prob[gwg.actlist[action_index]][int(edge[0]), int(edge[1])] = 0.9
#                 prob[gwg.actlist[action_index]][int(edge[0]), int(edge[0])] = 0.1
#                 action_index = (action_index + 1) % gwg.action_number
#         gwg.mdp.prob = prob
#         for state_index in range(len(gwg.mdp.states)):
#             static_action = gwg.mdp.actlist[int(graph_static_policies[data_index, time_index, state_index])]
#             static_costs[data_index, time_index, state_index] = gwg.mdp.r(state_index, static_action, time_index) + np.log(
#                 np.sum(np.exp(static_costs[data_index, time_index + 1, :]) * gwg.mdp.T(state_index, static_action)))
#
# static_cost = np.exp(static_costs[:, 0, :])

dynamic_cost = np.zeros([10, gwg.nstates])
for data_index in range(10):
    print data_index
    obstacles_index = obstacles_indexes[data_index, :]
    obstacles = obstacles_combo[obstacles_index]
    gwg.mdp.obstacles = obstacles
    gwg.mdp.update_reward()
    prob = {a: np.repeat(np.eye(gwg.nstates)[np.newaxis, :, :], gwg.mdp.horizon, axis=0) for a in gwg.actlist}
    for time_index in range(gwg.mdp.horizon):
        gwg.obstacles = obstacles_combo[obstacles_indexes[data_index, time_index]]
        action_index = 0
        for edge in list(gwg.dg.edges()):
            if (not np.isin(int(edge[0]), gwg.obstacles)) and (not np.isin(int(edge[0]), gwg.targets)):
                prob[gwg.actlist[action_index]][time_index, int(edge[0]), int(edge[1])] = 0.9
                prob[gwg.actlist[action_index]][time_index, int(edge[0]), int(edge[0])] = 0.1
                action_index = (action_index + 1) % gwg.action_number
    gwg.mdp.prob = prob

    for state_index in range(gwg.nstates):
        gwg.mdp.update_alpha(state_index)
        sol = gwg.mdp.primal_linear_program()
        x = np.array(sol['x']).reshape((gwg.horizon, gwg.nstates))
        dynamic_cost[data_index, state_index] = x[0, state_index]


print dynamic_cost
#print static_cost
np.save('graph_dynamic_cost', dynamic_cost)
# print static_cost
#np.save('graph_static_cost',  static_cost)
