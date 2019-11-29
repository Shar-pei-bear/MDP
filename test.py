from gridworld import *

# targets=[22,62,41]
#targets = [11]
targets = [11, 67, 18]
obstacles = [16, 24, 26, 34, 44, 51, 52, 61, 62, 66]
#obstacles = []
initial = 68
ncols = 8
nrows = 10
robotmdp = read_from_file_MDP('robotmdp.txt')
gwg = GridworldGui(initial, ncols, nrows, robotmdp, targets, obstacles)
#print(gwg.mdp.prob)
#raw_input("Waiting...")
gwg.mainloop()
# x = gwg.mdp.primal_linear_program()

# policy = x[0, initial, :] / np.sum(x[0, initial, :])
# print(policy)
# print(gw.mdp.T(initial,  2))

#print(x.shape)
# print(x[1, 5, :])
# print(x[1, 6, :])
# print(x[1, 9, :])

# print(gw.mdp.prob['N'][5,:])
# print(gw.mdp.prob['N'][6,:])
# print(gw.mdp.prob['N'][9,:])
# print(gw.mdp.prob['N'][10,:])

# print(gw.mdp.prob['E'])
# print(gw.mdp.prob['E'])
# print(gw.mdp.prob['E'])
