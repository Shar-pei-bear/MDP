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

static_policies = np.load('static_policies.npy')
dynamic_policies = np.load('dynamic_policies.npy')

static_costs = np.zeros([gw.mdp.horizon + 1, len(gw.mdp.states)])
dynamic_costs = np.zeros([gw.mdp.horizon + 1, len(gw.mdp.states)])

# terminal cost is set to zero
dynamic_costs[-1, :] = 0
static_costs[-1, :] = 0

gw.mdp.update_reward(targets_path[0][0:gw.mdp.horizon])

for time_index in reversed(range(gw.mdp.horizon)):
    for state_index in range(len(gw.mdp.states)):
        static_action = gw.mdp.actlist[static_policies[time_index, state_index]]
        dynamic_action = gw.mdp.actlist[dynamic_policies[time_index, state_index]]
        dynamic_costs[state_index, time_index] = gw.mdp.r(state_index, dynamic_action, time_index) + np.log(
            np.sum(self.reward[:, time_index] * self.T(state_index, action)))
        static_costs[state_index, time_index] = gw.mdp.r(state_index, static_action, time_index) + np.log(
            np.sum(self.reward[:, time_index] * self.T(state_index, action)))