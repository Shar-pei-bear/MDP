from gridworld import *
#targets=[22,62,41]
targets=[22]
obstacles=[17,18,28,14,45,55,54,77,62,74]
initial= [67]
ncols=10
nrows=10
robotmdp=read_from_file_MDP('robotmdp.txt')

actlist = ['N','S','W','E'];
nstates = nrows*ncols;
gw=Gridworld(initial, ncols, nrows, robotmdp, targets, obstacles)
print(gw.mdp.reward);
print(gw.mdp.r(21,0));
gw.mdp.primal_linear_program()
