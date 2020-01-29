from graphworld import *
initial = 17  # 0
targets = [7]  # 7
num_obstacles = 3
task_type = 'sequential'
network_file = 'network_topology'
T = 3
decoys_set = range(20)
decoys_set.remove(7)

visualization = False
obstacles_combo = np.load('obstacles_combo.npy')
obstacles_indexes = np.load('obstacles_indexes.npy')

gwg = GraphworldGui(network_file, initial, targets, num_obstacles, T, task_type, visualization, decoys_set)
graph_static_policies = np.load('graph_static_policies.npy')
print graph_static_policies.shape
static_costs = np.zeros([10, gwg.mdp.horizon + 1, len(gwg.mdp.states)])

# terminal cost is set to zero
static_costs[:, -1, :] = 0
static_costs[:, -1, targets[0]] = 1

prob = {a: np.eye(gwg.nstates) for a in gwg.actlist}
action_index = 0
for edge in list(gwg.dg.edges()):
    if not np.in1d(int(edge[0]), gwg.targets):
        prob[gwg.actlist[action_index]][int(edge[0]), int(edge[1])] = 0.9
        prob[gwg.actlist[action_index]][int(edge[0]), int(edge[0])] = 0.1
        action_index = (action_index + 1) % gwg.action_number

for data_index in range(10):
    print data_index
    obstacles_index = obstacles_indexes[data_index, 1:20]
    obstacles = obstacles_combo[obstacles_index]
    gwg.mdp.obstacles = obstacles
    gwg.mdp.update_reward()

    prob_aug = {a: np.repeat(np.eye(gwg.nstates + 1)[np.newaxis, :, :], gwg.mdp.horizon, axis=0) for a in
                gwg.actlist}
    for time_index in range(gwg.mdp.horizon):
        gwg.obstacles = obstacles_combo[obstacles_indexes[data_index, time_index + 1]]
        for a in gwg.actlist:
            for node_num_1 in range(gwg.nstates):
                for node_num_2 in range(gwg.nstates):
                    if np.in1d(node_num_2, gwg.obstacles) and node_num_1 != node_num_2 \
                            and not np.in1d(node_num_1, gwg.targets) and prob[a][node_num_1, node_num_2] > 0:
                        prob_aug[a][time_index, node_num_1, :] = 0
                        prob_aug[a][time_index, node_num_1, -1] = 1
                        break
                    else:
                        prob_aug[a][time_index, node_num_1, node_num_2] = prob[a][node_num_1, node_num_2]
    gwg.mdp.prob = prob_aug
    for time_index in reversed(range(gwg.mdp.horizon)):
        for state_index in range(gwg.nstates):
            static_action = gwg.mdp.actlist[int(graph_static_policies[data_index, time_index, state_index])]
            static_costs[data_index, time_index, state_index] = gwg.mdp.r(state_index, static_action, time_index) + \
                np.log(np.sum(np.exp(static_costs[data_index, time_index + 1, :]) *
                              gwg.mdp.T(state_index, static_action, time_index)))

static_cost = np.exp(static_costs[:, 0, 0:20])

dynamic_cost = np.zeros([10, gwg.nstates])
for data_index in range(10):
    print data_index
    obstacles_index = obstacles_indexes[data_index, 1:20]
    obstacles = obstacles_combo[obstacles_index]
    gwg.mdp.obstacles = obstacles
    gwg.mdp.update_reward()

    prob_aug = {a: np.repeat(np.eye(gwg.nstates + 1)[np.newaxis, :, :], gwg.mdp.horizon, axis=0) for a in
                gwg.actlist}
    for time_index in range(gwg.mdp.horizon):
        gwg.obstacles = obstacles_combo[obstacles_indexes[data_index, time_index + 1]]
        for a in gwg.actlist:
            for node_num_1 in range(gwg.nstates):
                for node_num_2 in range(gwg.nstates):
                    if np.in1d(node_num_2, gwg.obstacles) and node_num_1 != node_num_2 \
                            and not np.in1d(node_num_1, gwg.targets) and prob[a][node_num_1, node_num_2] > 0:
                        prob_aug[a][time_index, node_num_1, :] = 0
                        prob_aug[a][time_index, node_num_1, -1] = 1
                        break
                    else:
                        prob_aug[a][time_index, node_num_1, node_num_2] = prob[a][node_num_1, node_num_2]
    gwg.mdp.prob = prob_aug

    for state_index in range(gwg.nstates):
        gwg.mdp.update_alpha(state_index)
        sol = gwg.mdp.primal_linear_program()
        x = np.array(sol['x']).reshape((gwg.horizon, gwg.nstates + 1))
        dynamic_cost[data_index, state_index] = x[0, state_index]


print dynamic_cost
np.save('graph_dynamic_cost', dynamic_cost)
print static_cost
np.save('graph_static_cost',  static_cost)
