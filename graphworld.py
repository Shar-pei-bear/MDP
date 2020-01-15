import sys
import networkx as nx
from MDP import *
import matplotlib.pyplot as plt
import json
import csv

class GraphworldGui(object):
    def __init__(self, initial=0, nstates=0, edges=[], actlist=[], targets_path=[[]], obstacles=[],  task_type='sequential'):
        self.current = initial
        self.nstates = nstates
        self.edges = edges
        self.actlist = actlist
        self.targets_path = np.asarray(targets_path)

        self.task_type = task_type

        self.horizon = nstates - 1
        self.target_index = 0
        self.time_index = 0
        self.obstacles = obstacles
        self.configuration_index = 0
        self.p = 0.5

        acc = []
        if self.task_type == 'sequential':
            acc = self.targets_path[self.target_index, :]
        elif self.task_type == 'disjunction':
            acc = self.targets_path[:, self.time_index:self.time_index + self.horizon]
        self.targets = self.targets_path[:, self.time_index]

        self.mdp = MDP(initial, self.actlist, range(self.nstates), acc=acc,
                       obstacles=np.ones((self.horizon, 2), dtype=np.int)*self.obstacles[self.time_index, :], horizon=self.horizon)
        self.prolist = [0.9, 0.9, 0.9, 0.9]
        self.mdp.prob = self.getProbs(self.configuration_index)

        self.dg = nx.DiGraph()
        self.dg.add_nodes_from(range(nstates))
        self.construct_graph()

    def construct_graph(self):
        self.dg.remove_edges_from(list(self.dg.edges()))
        self.dg.add_edges_from(self.edges[self.configuration_index])

    def getProbs(self, configuration_index):
        prob = {a: np.eye(self.nstates) for a in self.actlist}

        if configuration_index == 0:
            prob[self.actlist[0]][0, 1] = self.prolist[0]
            prob[self.actlist[0]][0, 0] = 1 - self.prolist[0]
            prob[self.actlist[1]][0, 2] = self.prolist[1]
            prob[self.actlist[1]][0, 0] = 1 - self.prolist[1]

            prob[self.actlist[1]][1, 2] = self.prolist[1]
            prob[self.actlist[1]][1, 1] = 1 - self.prolist[1]

            prob[self.actlist[0]][2, 3] = self.prolist[0]
            prob[self.actlist[0]][2, 2] = 1 - self.prolist[0]

            prob[self.actlist[0]][3, 4] = self.prolist[0]
            prob[self.actlist[0]][3, 3] = 1 - self.prolist[0]
            prob[self.actlist[1]][3, 4] = self.prolist[1]
            prob[self.actlist[1]][3, 3] = 1 - self.prolist[1]

            prob[self.actlist[0]][4, 6] = self.prolist[0]
            prob[self.actlist[0]][4, 4] = 1 - self.prolist[0]
            prob[self.actlist[1]][4, 5] = self.prolist[1]
            prob[self.actlist[1]][4, 4] = 1 - self.prolist[1]

            prob[self.actlist[1]][5, 6] = self.prolist[1]
            prob[self.actlist[1]][5, 5] = 1 - self.prolist[1]

            prob[self.actlist[0]][6, 7] = self.prolist[0]
            prob[self.actlist[0]][6, 6] = 1 - self.prolist[0]
        else:
            prob[self.actlist[2]][0, 1] = self.prolist[2]
            prob[self.actlist[2]][0, 0] = 1 - self.prolist[2]

            prob[self.actlist[3]][1, 2] = self.prolist[3]
            prob[self.actlist[3]][1, 1] = 1 - self.prolist[3]

            prob[self.actlist[2]][2, 3] = self.prolist[2]
            prob[self.actlist[2]][2, 2] = 1 - self.prolist[2]

            prob[self.actlist[2]][3, 4] = self.prolist[2]
            prob[self.actlist[2]][3, 3] = 1 - self.prolist[2]
            prob[self.actlist[3]][3, 5] = self.prolist[3]
            prob[self.actlist[3]][3, 3] = 1 - self.prolist[3]

            prob[self.actlist[3]][4, 5] = self.prolist[3]
            prob[self.actlist[3]][4, 4] = 1 - self.prolist[3]

            prob[self.actlist[2]][5, 6] = self.prolist[2]
            prob[self.actlist[2]][5, 5] = 1 - self.prolist[2]
            prob[self.actlist[3]][5, 7] = self.prolist[3]
            prob[self.actlist[3]][5, 5] = 1 - self.prolist[3]

            prob[self.actlist[2]][6, 7] = self.prolist[2]
            prob[self.actlist[2]][6, 6] = 1 - self.prolist[2]

        return prob

    def follow(self, policy):
        action = str(np.random.choice(a=self.actlist, p=policy))
        print(action)
        self.move(action)
        #time.sleep(1)

    def move(self, act, obs=False):
        self.current = self.mdp.sample(self.current, act)

    def mainloop(self):
        """
        The robot moving in the Graph world with respect to the specification in DRA.
        """
        target_path = []

        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()
        pos = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (2, 1), 4: (3, 1), 5: (3, 0), 6: (4, 1), 7: (4, 0)}
        while True:

            fig.clear()
            values = np.ones(self.nstates) * 0.25
            values[self.current] = 1
            values[self.obstacles[self.time_index, :]] = 0.5
            nx.draw(self.dg, pos=pos, cmap=plt.get_cmap('viridis'), node_color=values, with_labels=True,
                    font_color='white', font_weight='bold')

            fig.axes[0].axis('equal')
            plt.pause(1)
            fig.canvas.draw()

            if self.task_type == 'sequential':
                if self.current == self.targets[self.target_index]:
                    print "reached ", self.target_index + 1, " goal"
                    if self.target_index < (len(self.targets_path) - 1):
                        self.target_index = self.target_index + 1
                    else:
                        print "completed sequential task"
            elif self.task_type == 'disjunction':
                if np.isin(self.current, self.targets):
                    print "completed disjunction task"

            #self.mdp.prob = self.getProbs(np.random.choice(2, p=[1 - self.p, self.p]))
            #self.mdp.prob = self.getProbs(self.configuration_index)
            self.time_index = self.time_index + 1
            self.mdp.obstacles = np.ones((self.horizon, 2), dtype=np.int)*self.obstacles[self.time_index, :]
            self.mdp.update_reward()
            self.mdp.update_alpha(self.current)
            x = self.mdp.primal_linear_program()

            # if self.time_index % 2 == 0:
            #     self.configuration_index = np.random.choice(2)
            #     self.construct_graph()
            # self.mdp.prob = self.getProbs(self.configuration_index)

            policy = x[0, self.current, :] / np.sum(x[0, self.current, :])
            policy[policy < 0] = 0
            self.follow(policy)
            #raw_input('Press Enter to continue ...')

            self.p = (self.p*(self.time_index - 1) + self.configuration_index)/self.time_index
            if self.current in self.obstacles[self.time_index, :]:
                # hitting the obstacles
                print "Detected, restarting ..."
                # raw_input('Press Enter to restart ...')
                self.current = self.mdp.init  # restart the game
                self.target_index = 0
                self.time_index = 0
                self.configuration_index = 0
                self.p = 0.5
                self.construct_graph()
                print "the current state is {}".format(self.current)

