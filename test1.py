from gridworld import *
#targets=[22,62,41]
#obstacles=[35,75,15,25,85,45,55]
#obstacles=[35,15,46,77,58]
targets=[22,38,41]
obstacles=[17,18,28,14,45,55,54,77,62,74]
initial= 67
ncols=10
nrows=10
robotmdp=read_from_file_MDP('robotmdp.txt')
gwg=GridworldGui(initial, ncols, nrows, robotmdp, targets, obstacles)



raw_input("Waiting...")
#G F (loc1 & F (loc2 & F loc3)) & G !loc4
# we label the grid world into different regions
execfile('DFA.py')
region_map={targets[0]:'1', targets[1]: '2', targets[2]:'3'}
for w in obstacles:
    region_map[w] = '4' # never hitting the walls
for s in gwg.mdp.states:
    if s in region_map.keys():
        gwg.mdp.labeling(s,region_map[s])
    else:
        gwg.mdp.labeling(s,'E') # for everything else
gwg.draw_state_labels()
from MDP import *
productmdp=productMDP(gwg.mdp,dra)
from SymbolicSCC import *
from Policy import *
#Win, policy= win_lose(productmdp)
#epsilon=float(0.01)/3
#Vstate1,policyE,T =E_state_value_iter(productmdp,epsilon, (Win,policy))
#Win, Policy= win_lose(productmdp)
#AEC=get_AEC(productmdp)
#policy1, Q, V = best_policy(productmdp)
#print productmdp.prob
import RL_Safe
lrmdp, policyT, iter_count, knownGW=RL_Safe.exploit_explore(gwg,productmdp,dra)
#knownGW=RL.exploit_explore(gwg,productmdp,dra)
gwg.mainloop(dra,policyT)
