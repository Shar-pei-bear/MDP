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
x = gw.mdp.primal_linear_program()
print(x.shape)