from __future__ import division
from MDP import *
import math
import time
from Policy import *
from gridworld import *
from SymbolicSCC import *
import copy
#import scipy


__author__ = 'Jie Fu, jief@seas.upenn.edu'
"""
Exploration-exploitation for PAC-MDP.
input: 
epsilon --- the approximation factor
delta --- the confidence interval is 1-delta
Data from the MDP --- the data collected from the product MDP
"""
#todo: the structure of the MDP.
global count
global count_sum
global known
global e
global d
global T
# first experiment
e=0.01
d=0.05
#with new epsilon and confidence level.
#e=0.02
#d=0.05
#third experiement
#e=0.05
#d=0.05
T=10
global m
#ep = e/(N*math.pow(T,2))
#m=((2+ep)/math.pow(ep,2))*math.log(2/d) 
#todo:iteration
count=dict([])
count_sum=dict([])

def known_trans(robotmdp,s,a,next_s, T):
    global count
    global count_sum
    N=1 # There is only one state in the robot mdp.
    k=1.96 # the confidence parameter for 95%
    # this uses center limit theorem, which requires the sample is sufficiently large.
    # hence, return false if the sample is too small.
    if count[(s,a,next_s)] < 50 or count_sum[(s,a)] == 0:
        return False
    # else, we need to compute the mean and var.
    mean= count[(s,a,next_s)]/count_sum[(s,a)]
    var= count[(s,a,next_s)]*(count_sum[(s,a)]-count[(s,a,next_s)])/(math.pow(count_sum[(s,a)],2)*(count_sum[(s,a)]+1))
    if var*k <= e/(3*N*T): 
        return True
    else:
        return False

def known_state(robotmdp,s,T):
    # if a is not enabled from the state s and the system knows it, then we have (s,a) to be true
    for a in robotmdp.actlist:
        if a == 'N':
            possible_next=[1,2,4]
        if a == 'E':
            possible_next=[2,1,3]
        if a == 'W':
            possible_next=[4,1,3]
        if a == 'S':
            possible_next=[3,4,2]
        for next_s in possible_next:
            if not known_trans(robotmdp,s, a, next_s,T):
                return False
    return True
        


def update_mdp(robotmdp,H,s,a,T):
    """
    This function update the learned robot MDP. 
    """
    global count
    global count_sum
    for next_s in robotmdp.states:
        i=robotmdp.states.index(s)
        j=robotmdp.states.index(next_s)
        if count_sum[(s,a)] !=0:
            robotmdp.prob[a][i,j] = count[(s,a,next_s)]/count_sum[(s,a)]
        else:
            robotmdp.prob[a][i,j]=0
    if known_state(robotmdp,s,T):
        H.add(s)
    else:
        if s in H: #If discovering a new transition, the state can become unknown again.
            H.remove(s)     
    return robotmdp,H

            

def update_count(gwg,current_s,act,next_s):
    global count
    global count_sum
    if current_s in gwg.walls or next_s==current_s:
        return
    if next_s == current_s-gwg.ncols:
        count[(0,act,1)]= count[(0,act,1)]+1
    if next_s == current_s+1:
        count[(0,act,2)]=count[(0,act,2)]+1
    if next_s == current_s-1:
        count[(0,act,4)] = count[(0,act,4)] +1
    if next_s == current_s+gwg.ncols:
        count[(0,act,3)] = count[(0,act,3)]+1
    count_sum[(0,act)]=count_sum[(0,act)]+1
    return

def beSafe(safe, safeCtrl,policyT,knownProductMDP):
    newPolicy=dict([])
    for (s,t) in knownProductMDP.states:
        if policyT.has_key((s,t)):
            pass
        else:
            policyT[(s,t)]=set(knownProductMDP.actlist)
        X=set(policyT[(s,t)]).intersection(safeCtrl[s])
        if  X== set([]):
            newPolicy[(s,t)]=policyT[(s,t)] # if no action can keep the system safe, then follow the current policyT.
        else:
            newPolicy[(s,t)]=X
    return newPolicy
            

def exploit_explore(gwg,productmdp,dra):
    """
    Given the learned mdp, compute the exploitation-exploration policy.
    In this algorithm, we fix a finite horizon T for value iteration.
    """
    global count
    global count_sum
    start = time.clock()
    robotmdp=read_from_file_MDP("robotmdp.txt")
    count ={(s,a,next_s) : 0 for s in robotmdp.states for a in robotmdp.actlist for next_s in robotmdp.states }
    count_sum= {(s,a) : 0 for s in robotmdp.states for a in robotmdp.actlist }
    T=8
    log=open('log','w')
    evaluate=open('evaluate','w')
    self_evaluate=open('self_evaluate','w')
    V=dict([]) #initialize the value function.
    policyT=dict([])  #initialize the policy.
    iter_count=0
    lrmdp=MDP()
    lrmdp.states=[0,1,2,3,4]
    lrmdp.actlist=list(gwg.mdp.actlist)
    
    lrmdp.prob={a: np.zeros((len(lrmdp.states),len(lrmdp.states))) for a in lrmdp.actlist} 

    iter_count =0
    limit = 200000
    H=set([])
    Hpre=H.copy() # record the set of known states. 
    knownGW=Gridworld(int(gwg.current), int(gwg.nrows),int(gwg.ncols), lrmdp,list( gwg.targets), list(gwg.obstacles))
    for s in knownGW.mdp.states:
        knownGW.mdp.labeling(s, gwg.mdp.L[s])
    current_s=productmdp.init    
    productmdpcopy=copy.deepcopy(productmdp)
    knownProductStates=set([])
    knownProductMDP=productMDP(knownGW.mdp, dra)
    subproductmdp=sub_MDP(knownProductMDP, knownProductStates)
    Win, policy= win_lose(subproductmdp)
    V, policy_init = T_step_value_iter(subproductmdp,T, (Win,policy))
    policyT=dict([])
    for s in set(knownProductMDP.states)- knownProductStates: 
        policyT[s]=policy_init[-1]
    for s in knownProductStates:
        policyT[s]=policy_init[s]
    safe, safeCtrl=Safe(gwg)
    policyT=beSafe(safe, safeCtrl,policyT,knownProductMDP)
    while iter_count <= limit:
        iter_count=iter_count+1
        log.write('{} {}\n'.format(iter_count,H))
        if H==Hpre:
            pass
        else:
            knownGW=Gridworld(int(gwg.current), int(gwg.nrows),int(gwg.ncols), lrmdp,list( gwg.targets), list(gwg.obstacles))
            knownProductMDP=productMDP(knownGW.mdp,dra)
            Win, policy= win_lose(knownProductMDP)
            knownProductStates={(h,s) for h in H for s in dra.states}
            print "Update policy"
            subproductmdp=sub_MDP(knownProductMDP, knownProductStates)
            
            V, policy_init = T_step_value_iter(subproductmdp,T, (Win,policy))

            for s in set(knownProductMDP.states)- knownProductStates: 
                policyT[s]=policy_init[-1]
            for s in knownProductStates:
                policyT[s]=policy_init[s]

            if H == {0}:
                break
        Hpre=H.copy()
        lrmdp,H, current_s = aux_ex2(lrmdp,productmdpcopy,current_s,H,policyT,T,knownProductStates,gwg)
    knownGW=Gridworld(int(gwg.current), int(gwg.nrows),int(gwg.ncols), lrmdp,list( gwg.targets), list(gwg.obstacles))
    knownProductMDP=productMDP(knownGW.mdp,dra)
    Win, policy= win_lose(knownProductMDP)
    markWin(gwg,Win)
    V, policyT = T_step_value_iter(knownProductMDP,T, (Win,policy))
            
    elapsed = (time.clock() - start)
    print elapsed
    log.close()
    evaluate.close()
    self_evaluate.close()
    print count
    print count_sum
    return lrmdp, policyT, iter_count, knownGW

def markWin(gwg,Win):
    M=set([])
    for (s, t) in Win:
        if t ==0 and s not in gwg.targets:
            M.add(s)
    gwg.draw_region(M)
    return

def aux_ex2(lrmdp,productmdp,current_s,H,policyT,T,knownProductStates,gwg):
    R=1# the exploration ratio.
    current_mdp_s=current_s[0] 
    if current_s in knownProductStates: # current_s=(s,q)
        next_s,act = exploit(productmdp,current_s, policyT)
    else: # an unknown state is encountered.
        next_s,act = balanced_wandering(productmdp, current_s) # exploration.
    #print "from {} the next state is with action {} - {}".format(current_s,next_s,act)
    next_mdp_s=next_s[0]
    gwg.move_deter(next_mdp_s)
    update_count(gwg,current_mdp_s,act,next_mdp_s)
    lrmdp,H=update_mdp(lrmdp, H,0, act,T)
    if current_mdp_s in gwg.walls:
        current_s=productmdp.init
    else:
        current_s=next_s
    #when all the states becomes known, return the policy and terminate.
    return lrmdp, H, current_s
