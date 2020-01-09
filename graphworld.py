import sys
import networkx as nx
from MDP import *
import matplotlib.pyplot as plt

class GraphworldGui(object):
    def __init__(self, initial=0, nstates=0, edges=[], actlist=[], targets_path=[[]], obstacles=[],  task_type='sequential'):
        self.current = initial
        self.nstates = nstates
        self.prolist = [0.9, 0.9, 0.9, 0.9]
        self.actlist = actlist
        self.nactions = len(self.actlist)
        self.targets_path = np.asarray(targets_path)

        self.obstacles = obstacles
        prob = {a: np.eye(self.nstates) for a in self.actlist}

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

        self.horizon = nstates - 1
        self.target_index = 0
        self.time_index = 0

        acc = []
        self.task_type = task_type

        if self.task_type == 'sequential':
            acc = self.targets_path[self.target_index, :]
        elif self.task_type == 'disjunction':
            acc = self.targets_path[:, self.time_index:self.time_index + self.horizon]
        self.targets = self.targets_path[:, self.time_index]

        self.mdp = MDP(initial, self.actlist, range(self.nstates), acc=acc, obstacles=obstacles, horizon=self.horizon)
        self.mdp.prob = prob

        self.dg = nx.DiGraph()
        self.dg.add_nodes_from(range(nstates))
        self.dg.add_edges_from(edges)

    def follow(self, policy):
        print(policy)
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

        while True:
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

            self.mdp.update_alpha(self.current)
            x = self.mdp.primal_linear_program()

            policy = x[0, self.current, :] / np.sum(x[0, self.current, :])
            policy[policy < 0] = 0
            self.follow(policy)
            #raw_input('Press Enter to continue ...')
            if self.current in self.obstacles:
                # hitting the obstacles
                print "Hitting the walls, restarting ..."
                # raw_input('Press Enter to restart ...')
                self.current = self.mdp.init  # restart the game
                self.target_index = 0
                self.time_index = 0

                print "the current state is {}".format(self.current)

            fig.clear()
            values = np.ones(self.nstates) * 0.25
            values[self.current] = 1
            nx.draw_kamada_kawai(self.dg, cmap=plt.get_cmap('viridis'), node_color=values, with_labels=True,
                                 font_color='white', font_weight='bold')
            plt.pause(1)
            fig.canvas.draw()
