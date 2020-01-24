from graphworld import *
initial = 0
nstates = 8

obstacles = np.load('data/obstacles.npy')
targets_path = [[7, 7, 7, 7, 7, 7, 7]]
task_type ='sequential'
edges = [[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7)],
         [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)]]
actlist = ['a1', 'a2', 'a3', 'a4']
gwg = GraphworldGui(initial, nstates, edges, actlist, targets_path, obstacles,  task_type)

graph_static_policies = np.load('data/graph_static_policies.npy')
static_costs = np.zeros([gwg.mdp.horizon + 1, len(gwg.mdp.states)])

# terminal cost is set to zero
static_costs[-1, :] = 0

gwg.mdp.obstacles = obstacles[0:gwg.mdp.horizon, :]
gwg.mdp.update_reward()

for time_index in reversed(range(gwg.mdp.horizon)):
    for state_index in range(len(gwg.mdp.states)):
        static_action = gwg.mdp.actlist[int(graph_static_policies[time_index, state_index])]
        static_costs[time_index, state_index] = gwg.mdp.r(state_index, static_action, time_index) + np.log(
            np.sum(np.exp(static_costs[time_index + 1, :]) * gwg.mdp.T(state_index, static_action)))

static_cost = np.exp(static_costs[0, :])
dynamic_cost = np.zeros(len(gwg.mdp.states))
for state_index in range(len(gwg.mdp.states)):
    gwg.mdp.update_alpha(state_index)
    x = gwg.mdp.primal_linear_program()
    dynamic_cost[state_index] = x[0, state_index]

print dynamic_cost
print static_cost
np.save('graph_dynamic_cost', dynamic_cost)
np.save('graph_static_cost',  static_cost)
