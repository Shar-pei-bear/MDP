__author__ = 'Jie Fu, jief@seas.upenn.edu'
"""
Generate the set of SCC components in the graph of MDP.
"""

import os
def is_safe(mdp,s,a,Unsafe):
    for next_s in mdp.states:
        if mdp.P(s,a,next_s) != 0 and next_s in Unsafe:
            return False
    return True

def get_BDD(mdp):
    S=[]
    S1=set([]) # the set of player 1's states
    Sr=set([]) # the set of random states (player2)
    edges=set([]) # the set of edges
    Unsafe=set([])
    for J,K in mdp.acc:
        Unsafe=Unsafe.union(J)
    print Unsafe
    for s in mdp.states:
        S1.add(s)
        if s not in S:
            S.append(s)        
        for a in mdp.actlist:
            if not is_safe(mdp,s,a,Unsafe):
                break
            for next_s in mdp.states:
                if mdp.P(s,a,next_s) != 0:
                    if next_s not in S:
                        S.append(next_s)
                    Sr.add((s,a)) # the state s is player1's state and the state (s,a) is player 2's state.
                    if (s,a) not in S:
                        S.append((s,a))
                    edges.add((s,(s,a)))
                    edges.add(((s,a),next_s)) 
    return S1, Sr, S, edges

import networkx as nx
def get_SCCsubGs(edges):
    #generate the set of strongly connected components.
    G=nx.DiGraph()
    G.add_edges_from(list(edges))
    subGs=nx.strongly_connected_component_subgraphs(G) 
    return subGs

def is_accepting(mdp,A):
    for (J,K) in mdp.acc:
        if A.intersection(J) == set([]) and A.intersection(K) != set([]):
            return True
        else:
            return False

def is_complete(mdp,subG):
    for (s,t) in subG.edges():
        if s in mdp.states:
            a=t[1]
            for next_s in mdp.states:
                if mdp.P(s, a, next_s) != 0 and next_s not in subG.nodes():
                    return False
    return True
        
def get_AECs(mdp):
    """
    Given a MDP, return a tuple (A, policy)
    A: includes all states in one of accepting end components.
    policy: the policy for states in A.
    """
    S1, Sr,S, edges =get_BDD(mdp)
    subGs=get_SCCsubGs(edges)
    AECs=[]
    for subG in subGs:
        if not is_complete(mdp,subG):
            print "Not complete"
        aec=set([])
        policy=dict([])
        for (s,t) in subG.edges():
            if s in S1:
                aec.add(s)
            policy[s]= t[1]
        if policy != dict([]) and is_accepting(mdp,aec):
            AECs.append((aec,policy))
        else:
            pass
    return AECs
        
