__author__ = 'Jie Fu, jief@seas.upenn.edu'
"""
Generate the set of SCC components in the graph of MDP.
"""

import os
import random
import networkx as nx
def get_BDD(mdp):
    S=[]
    S1=set([]) # the set of player 1's states
    Sr=set([]) # the set of random states (player2)
    edges=set([]) # the set of edges
    G=set([]) 
    goals=set([])
    if mdp.acc ==None:
        G=set([])
    else:
        for (J,K) in mdp.acc:
            G=G.union(K) # G is the union of all states that we aim to visit infinitely often.

    for s in mdp.states:
        S1.add(s)
        if s in G:
            goals.add(s)

        for a in mdp.actlist:
            for next_s in mdp.states:
                if mdp.P(s,a,next_s) != 0:
                    Sr.add((s,a)) # the state s is player1's state and the state (s,a) is player 2's state.
                    edges.add((s, (s,a)))
                    edges.add(((s,a), next_s))
    S=list(S1)+list(Sr)
    #edges_indx= {(S.index(s),S.index(t)) for (s,t) in edges}
    #goals_indx={S.index(s) for s in goals}
    return S1, Sr,S, edges, goals

        
def generate_input_mdp(S1,Sr,S,edges,goals, filename):
    inputf= open(filename,'w+')
    inputf.write('{}\n'.format(len(S1)))
    inputf.write('{}\n'.format(len(Sr)))

    for e in edges:
        inputf.write('{} {}\n'.format(e[0], e[1]))
    inputf.write('-1')

    for g in goals:
        inputf.write('{}\n'.format(g))
    inputf.write('-1')

def is_accepting(mdp,A):
    for (J,K) in mdp.acc:
        if A.intersection(J) == set([]) and A.intersection(K) != set([]):
            return True
        else:
            return False

def win_lose(mdp):

    S1, Sr,S, edges, goals =get_BDD(mdp)
    G=nx.DiGraph()
    G.add_edges_from(edges)

    W1=set([])
    W2=set([])
    W=W1.union(W2)
        
    while True:
        inducedSet=set(S)-W
        #print "The remainning set is {}".format(len(inducedSet))
        inducedG=G.subgraph(list(inducedSet))
        SCCs=scc_decompose(inducedG,S)
        for C in SCCs:
            #print "the SCC is {}".format(C)
            if Post(G,C).issubset(C.union(W)): # to check if C is a bottom SCC in the graph induced by S\W.
                if Post(G,C).intersection(W1) !=set([])  or C.intersection(goals) != set([]):
                    W1=W1.union(C)
                else:
                    W2=W2.union(C)
        W1=Attr1(G,S1,Sr,W1)
        W2=AttrR(G,S1,Sr,W2)
        W=W1.union(W2)
        if W == set(S):
            break
    print "The length of W1 is {}".format(len(W1))
    print "The length of W2 is {}".format(len(W2))

    Win,Policy=get_AEC(G, S1,Sr, W1,W2)
    return Win, Policy

def get_AEC(G, S1,Sr, W1, W2):
    
    subG=G.subgraph(list(W1-W2))
    Win=set([])
    Policy=dict([])

    for (s,t) in subG.edges():
        if s in S1:
            Win.add(s)
            if Policy.has_key(s):
                Policy[s].add(t[1])
            else:
                Policy[s]=set([t[1]])

    return Win, Policy
            
            

def Post(G,C):
    Post=set([])
    for (x,y) in G.edges():
        if x in C:
            Post.add(y)
    return Post
        
def Pre(G,U):
    Pre=set([])
    for (x,y) in G.edges():
        if y in U:
            Pre.add(x)
    return Pre
        
def Attr1(G,S1,Sr,U):        
    X=U.copy()
    #print "The size of X is {}".format(len(X))
    new_X =set([])
    while True:
        new_X=X.copy()
        for s in Sr:
            Y=set([])
            for (x,y) in G.edges():
                if x == s:
                    Y.add(y)
            if Y.issubset(X):
                new_X.add(s)
        for s in S1:
            for (x,y) in G.edges():
                if x==s and y in X:
                    new_X.add(s)
                    break
        if new_X != X:
            X=new_X.copy()
        else:
            break
    return new_X

def AttrR(G,S1,Sr,U):        
    return Attr1(G,Sr,S1,U)

def Safe(gwg):
    
    S1, Sr,S, edges, goals =get_BDD(gwg.mdp)
    G=nx.DiGraph()
    G.add_edges_from(edges)
    Safe=set([])
    
    for s in S1:
        if s not in gwg.obstacles:
            Safe.add(s)
    for s in Sr:
        if s[0] not in gwg.obstacles:
            Safe.add(s)
    Unsafe=AttrR(G,S1,Sr, set(S)-Safe)
    newSafe=set(S)-Unsafe

    safe=set([])
    safeCtrl=dict([])
    safeG=G.subgraph(newSafe)
    for (s,t) in safeG.edges():
        if s in S1:
            safe.add(s)
            if safeCtrl.has_key(s):
                safeCtrl[s].add(t[1])
            else:
                safeCtrl[s]=set([t[1]])
    #print "The safe region of grid world is {}".format(safe)
    for s in gwg.mdp.states:
        if s not in safe:
            safeCtrl[s]=set([])
    return safe, safeCtrl
    
    
def generate_input(G,S,filename):
    inputf= open(filename,'w+')
    inputf.write('{}\n'.format(len(S)))

    for (s,t) in G.edges():
        inputf.write('{} {}\n'.format(S.index(s), S.index(t)))
    inputf.write('-1')
    inputf.close()
    return
    

def scc_decompose(G,S):
    generate_input(G,S,"input.txt")
    os.system("scc/./scc < input.txt")
    outputf=open("SCC_Decomposition.txt", 'r')
    lines=[line.rstrip('\n') for line in outputf]
    indx_sccs= [l.split() for l in lines]
    SCCs=[]
    for scc in indx_sccs:
        A=set([S[int(i)] for i in scc])
        SCCs.append(A)
    return SCCs
