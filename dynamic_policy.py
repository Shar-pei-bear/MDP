from gridworld import *

targets = [11]
targets_path = [[21, 31, 31, 41, 41, 42, 42, 42, 42, 41, 42, 42, 32, 31, 21, 22, 23, 23, 23, 22, 22, 22, 23, 22, 12, 12, 12,
           12, 11, 12, 11, 21, 21, 22, 22, 21, 21, 22, 22, 23, 22, 22, 21, 31, 31, 31, 21, 11, 11, 21, 31, 31, 41, 41,
           41, 42, 41, 42, 42, 42, 43, 43, 43, 53, 43, 43]]
obstacles = [16, 24, 26, 34, 44, 51, 52, 61, 62, 66]

initial = 68
ncols = 8
nrows = 10
robotmdp = read_from_file_MDP('/home/zhentian/MDP/robotmdp.txt')
gw = Gridworld(initial, ncols, nrows, robotmdp, targets, targets_path, obstacles)
expected_costs = 0
terminal_cost = np.zeros(len(gw.mdp.states))
ut = np.zeros([gw.mdp.horizon, len(gw.mdp.states)])
policies_dynamic_goal = np.zeros([gw.mdp.horizon, len(gw.mdp.states)])

for time_index in range(gw.mdp.horizon):
    gw.mdp.update_reward(targets_path[0][time_index:time_index + gw.mdp.horizon])
    print 'time index is ', time_index
    for state_index in range(len(gw.mdp.states)):
        gw.mdp.update_alpha(state_index)
        x = gw.mdp.primal_linear_program()
        temp = np.argmax(x, axis=2)
        policies_dynamic_goal[time_index, state_index] = temp[0, state_index]

np.save('dynamic_policies', policies_dynamic_goal)
# self.mdp.update_reward(self.current_target)

# for time_index in reversed(range(gw.mdp.horizon)):
#     instant_costs = np.zeros(len(gw.mdp.states))
#     for state_index in range(len(gw.mdp.states)):
#         action = gw.mdp.actlist[policies[time_index, state_index]]
#         instant_costs[state_index] = np.sum(gw.mdp.reward[:, time_index] * gw.mdp.T(state_index, action))


