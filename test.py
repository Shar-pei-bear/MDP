from gridworld import *
#targets=[22,62,41]
targets=[5]
obstacles=[]
initial= [6]
ncols=4
nrows= 4
robotmdp=read_from_file_MDP('robotmdp.txt')

actlist = ['S','S','W','E'];
nstates = nrows*ncols;
gw=Gridworld(initial, ncols, nrows, robotmdp, targets, obstacles)
#x = gw.mdp.primal_linear_program()
print(gw.mdp.prob['S'][0,:])
print(gw.mdp.prob['S'][1,:])
print(gw.mdp.prob['S'][2,:])
print(gw.mdp.prob['S'][3,:])
print(gw.mdp.prob['S'][4,:])
print(gw.mdp.prob['S'][5,:])
print(gw.mdp.prob['S'][6,:])
print(gw.mdp.prob['S'][7,:])
print(gw.mdp.prob['S'][8,:])
print(gw.mdp.prob['S'][9,:])
print(gw.mdp.prob['S'][10,:])
print(gw.mdp.prob['S'][11,:])
print(gw.mdp.prob['S'][12,:])
print(gw.mdp.prob['S'][13,:])
print(gw.mdp.prob['S'][14,:])
print(gw.mdp.prob['S'][15,:])
# print(gw.mdp.prob['E'])
# print(gw.mdp.prob['W'])
# print(gw.mdp.prob['S'])
