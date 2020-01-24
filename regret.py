from gridworld import *

targets = [11]
targets_path = [[21, 31, 31, 41, 41, 42, 42, 42, 42, 41, 42, 42, 32, 31, 21, 22, 23, 23, 23, 22, 22, 22, 23, 22, 12, 12, 12,
           12, 11, 12, 11, 21, 21, 22, 22, 21, 21, 22, 22, 23, 22, 22, 21, 31, 31, 31, 21, 11, 11, 21, 31, 31, 41, 41,
           41, 42, 41, 42, 42, 42, 43, 43, 43, 53, 43, 43]]
obstacles = [16, 24, 26, 34, 44, 51, 52, 61, 62, 66]

initial = 68
ncols = 8
nrows = 10
robotmdp = read_from_file_MDP('robotmdp.txt')
gw = Gridworld(initial, ncols, nrows, robotmdp, targets, targets_path, obstacles)

terminal_cost = np.zeros(len(gw.mdp.states))

static_policies = np.load('data/static_policies.npy')
#dynamic_policies = np.load('dynamic_policies.npy')

static_costs = np.zeros([gw.mdp.horizon + 1, len(gw.mdp.states)])

# terminal cost is set to zero
static_costs[-1, :] = 0


gw.mdp.update_reward(targets_path[0][0:gw.mdp.horizon])
for time_index in reversed(range(gw.mdp.horizon)):
    for state_index in range(len(gw.mdp.states)):
        static_action = gw.mdp.actlist[int(static_policies[time_index, state_index])]
        static_costs[time_index, state_index] = gw.mdp.r(state_index, static_action, time_index) + np.log(
            np.sum(np.exp(static_costs[time_index + 1, :]) * gw.mdp.T(state_index, static_action)))

static_cost = np.exp(static_costs[0, :])
dynamic_cost = np.zeros(len(gw.mdp.states))
for state_index in range(len(gw.mdp.states)):
    gw.mdp.update_alpha(state_index)
    x = gw.mdp.primal_linear_program()
    dynamic_cost[state_index] = x[0, state_index]

np.save('dynamic_cost', dynamic_cost)
np.save('static_cost',  static_cost)
