import sys
import networkx as nx
from MDP import *
import matplotlib.pyplot as plt
import itertools
import random

class GraphworldGui(object):
    def __init__(self, network_file='network_topology', initial=0, targets=[], num_obstacles=0, T=1,
                 task_type='sequential', visualization=False, decoys_set=[]):
        self.dg = nx.read_gml(network_file)

        edge_number = []
        dead_end = set()
        for index in range(self.dg.number_of_nodes()):
            if self.dg.out_degree(str(index)) == 0:
                dead_end.add(index)
            edge_number.append(len(list(self.dg.neighbors(str(index)))))
        self.action_number = max(edge_number)

        self.current = initial
        self.nstates = self.dg.number_of_nodes()
        self.actlist = ["a" + str(e) for e in range(self.action_number)]
        self.T = T
        self.num_obstacles = num_obstacles
        self.task_type = task_type
        self.visualization = visualization
        self.decoys_set = decoys_set

        self.obstacles_combo = []
        self.obstacles = np.asarray([])
        self.sample_obstacles()

        self.horizon = self.nstates - 1
        self.target_index = 0
        self.time_index = 0
        self.configuration_index = 0
        self.p = 0.5

        self.targets = np.asarray(targets)
        if self.task_type == 'sequential':
            self.dead_end = dead_end.difference([self.targets[self.target_index]])
            acc = np.full(self.horizon, self.targets[self.target_index], dtype=np.int)
        else:
            self.dead_end = dead_end.difference(self.targets)
            acc = np.ones((self.horizon, self.targets.size), dtype=np.int)*self.targets

        self.mdp = MDP(initial, self.actlist, range(self.nstates), acc=acc,
                       obstacles=np.ones((self.horizon, self.obstacles.size), dtype=np.int)*self.obstacles, horizon=self.horizon)

        self.mdp.prob = self.getProbs()

    def sample_obstacles(self):
        if self.num_obstacles:
            decoys_set = list(self.decoys_set)
            if self.current in decoys_set:
                decoys_set.remove(self.current)
            self.obstacles_combo = list(itertools.combinations(decoys_set, self.num_obstacles))
            random.shuffle(self.obstacles_combo)
            obstacles_index = np.random.choice(range(len(self.obstacles_combo)))
            self.obstacles = np.asarray(self.obstacles_combo[obstacles_index])

    def construct_graph(self):
        self.dg.remove_edges_from(list(self.dg.edges()))
        self.dg.add_edges_from(self.edges[self.configuration_index])

    def getProbs(self):
        prob = {a: np.eye(self.nstates) for a in self.actlist}
        action_index = 0
        for edge in list(self.dg.edges()):
            if (not np.isin(int(edge[0]), self.obstacles)) and (not np.isin(int(edge[0]), self.targets)):
                prob[self.actlist[action_index]][int(edge[0]), int(edge[1])] = 0.9
                prob[self.actlist[action_index]][int(edge[0]), int(edge[0])] = 0.1
                action_index = (action_index + 1) % self.action_number

        return prob

    def follow(self, policy):
        action = str(np.random.choice(a=self.actlist, p=policy))
        #print 'current state is ', self.current
        #print 'current action is ', action
        self.move(action)
        #time.sleep(1)

    def move(self, act, obs=False):
        self.current = self.mdp.sample(self.current, act)

    def reset(self):
        self.current = self.mdp.init  # restart the game
        self.target_index = 0
        self.time_index = 0
        self.configuration_index = 0
        self.p = 0.5

    def mainloop(self):
        """
        The robot moving in the Graph world with respect to the specification in DRA.
        """
        target_path = []
        if self.visualization:
            fig = plt.gcf()
            fig.show()
            fig.canvas.draw()
        # pos = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (2, 1), 4: (3, 1), 5: (3, 0), 6: (4, 1), 7: (4, 0)}
        while True:
            if self.visualization:
                fig.clear()
                values = np.ones(self.nstates) * 0.25
                values[self.current] = 1
                if self.num_obstacles:
                    values[self.obstacles] = 0.5
                nx.draw_kamada_kawai(self.dg, cmap=plt.get_cmap('viridis'), nodelist=[str(e) for e in range(self.nstates)],
                                     node_color=values, with_labels=True, font_color='white', font_weight='bold')

                fig.axes[0].axis('equal')
                plt.pause(1)
                fig.canvas.draw()

            if self.task_type == 'sequential':
                if self.current == self.targets[self.target_index]:
                    print 'the current time instant is ', self.time_index
                    self.reset()
                    return True
                    # print "reached ", self.target_index + 1, " goal"
                    # if self.target_index < (len(self.targets) - 1):
                    #     self.target_index = self.target_index + 1
                    # else:
                    #     print "completed sequential task"
            elif self.task_type == 'disjunction':
                if np.isin(self.current, self.targets):
                    print "completed disjunction task"

            # self.mdp.prob = self.getProbs(np.random.choice(2, p=[1 - self.p, self.p]))
            # self.mdp.prob = self.getProbs(self.configuration_index)

            self.time_index = self.time_index + 1
            if self.time_index > 100:
                print 'I am stuck'
                self.reset()
                return False

            if self.T and self.num_obstacles and self.time_index % self.T == 0:
                self.sample_obstacles()

            self.mdp.update_alpha(self.current)
            sol = self.mdp.primal_linear_program()
            self.mdp.prob = self.getProbs()
            self.mdp.obstacles = np.ones((self.horizon, self.obstacles.size), dtype=np.int)*self.obstacles
            self.mdp.update_reward()

            if sol['status'] == 'optimal':
                x = np.array(sol['z']).reshape((self.horizon, self.nstates, self.action_number))
            else:
                print 'optimization failed'
                print 'the current state is ', self.current
                print 'the current obstacles is ', self.obstacles

                self.reset()
                return False

            # if self.time_index % 2 == 0:
            #     self.configuration_index = np.random.choice(2)
            #     self.construct_graph()
            # self.mdp.prob = self.getProbs(self.configuration_index)

            policy = x[0, self.current, :] / np.sum(x[0, self.current, :])
            policy[policy < 0] = 0
            self.follow(policy)
            # raw_input('Press Enter to continue ...')

            # self.p = (self.p*(self.time_index - 1) + self.configuration_index)/self.time_index
            if np.isin(self.current, self.obstacles) or self.current in self.dead_end:
                # hitting the obstacles
                print 'the current time instant is ', self.time_index
                self.reset()
                return False
                # print "Detected, restarting ..."
                # # raw_input('Press Enter to restart ...')
                # # self.construct_graph()
                # print "the current state is {}".format(self.current)

