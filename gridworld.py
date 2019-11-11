import MDP
import os, sys, getopt, pdb, string
import time

import pygame
import pygame.locals as pgl

import numpy as np
# import random as pr
from random import choice
import random
from MDP import *


def coords(nrows, ncols, s):
    return (s / ncols, s % ncols)


def wall_pattern(nrows, ncols, endstate=0, pattern="comb"):
    """Generate a specific wall pattern for a particular gridworld."""

    goal = coords(nrows, ncols, endstate)
    walls = []

    if goal[1] % 2 == 0:
        wmod = 1
    else:
        wmod = 0

    for i in range(ncols):
        for j in range(nrows):
            if i % 2 == wmod and j != nrows - 1:
                walls.append((i, j))

    return walls


class Gridworld():
    def __init__(self, current=0, nrows=8, ncols=8, robotmdp=MDP(), targets=[], obstacles=[]):
        # walls are the obstacles. The edges of the gridworld will be included into the walls.
        self.nrows = nrows
        self.ncols = ncols
        self.robotmdp = robotmdp
        self.nstates = nrows * ncols
        self.actlist = robotmdp.actlist
        self.nactions = len(self.actlist)
        self.targets = targets
        self.left_edge = []
        self.right_edge = []
        self.top_edge = []
        self.bottom_edge = []
        self.obstacles = obstacles
        for x in range(self.nstates):
            # note that edges are not disjoint, so we cannot use elif
            if x % self.ncols == 0:
                self.left_edge.append(x)
            if 0 <= x < self.ncols:
                self.top_edge.append(x)
            if x % self.ncols == self.ncols - 1:
                self.right_edge.append(x)
            if (self.nrows - 1) * self.ncols <= x <= self.nstates:
                self.bottom_edge.append(x)
        self.edges = self.left_edge + self.top_edge + self.right_edge + self.bottom_edge
        self.walls = self.edges + obstacles
        prob = {a: np.zeros((self.nstates, self.nstates)) for a in self.actlist}
        for s in range(self.nstates):
            for a in self.actlist:
                prob = self.getProbs(s, a, prob)
        self.mdp = MDP(current, self.actlist, range(self.nstates), acc=self.targets)
        self.mdp.prob = prob

    def coords(self, s):
        return (s / self.ncols, s % self.ncols)  # the coordinate for state s.

    def __isAllowed(self, state):
        if state in self.edges or state not in range(self.nstates):
            return False
        return True

    def getProbs(self, state, action, prob):
        successors = []
        if state in self.walls:
            successors = [(state, 1)]
            for (next_state, p) in successors:
                prob[action][state, next_state] = p
            return prob

        northState = (self.__isAllowed(state - self.ncols) and state - self.ncols) or state
        westState = (self.__isAllowed(state - 1) and state - 1) or state
        southState = (self.__isAllowed(state + self.ncols) and state + self.ncols) or state
        eastState = (self.__isAllowed(state + 1) and state + 1) or state
        centerState = state

        successors.append((northState, self.robotmdp.P(0, action, 1)))
        successors.append((westState, self.robotmdp.P(0, action, 4)))
        successors.append((southState, self.robotmdp.P(0, action, 3)))
        successors.append((eastState, self.robotmdp.P(0, action, 2)))
        successors.append((centerState, self.robotmdp.P(0, action, 0)))

        for (next_state, p) in successors:
            prob[action][state, next_state] += p
        return prob

    def rcoords(self, coords):
        s = coords[0] * self.ncols + coords[1]
        return s


class GridworldGui(Gridworld, object):
    def __init__(self, initial, nrows=8, ncols=8, robotmdp=MDP(), targets=[], obstacles=[], size=16):
        super(GridworldGui, self).__init__(initial, nrows, ncols, robotmdp, targets, obstacles)
        # compute the appropriate height and width (with room for cell borders)
        self.height = nrows * size + nrows + 1
        self.width = ncols * size + ncols + 1
        self.size = size

        # initialize pygame ( SDL extensions )
        pygame.init()
        pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Gridworld')
        self.screen = pygame.display.get_surface()
        self.surface = pygame.Surface(self.screen.get_size())
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg_rendered = False  # optimize background render

        self.background()
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

        self.build_templates()
        self.updategui = True  # switch to stop updating gui if you want to collect a trace quickly

        self.current = self.mdp.init  # when start, the current state is the initial state
        self.state2circle(self.current)

    def build_templates(self):

        # Note: template already in "graphics" coordinates
        template = np.array([(-1, 0), (0, 0), (1, 0), (0, 1), (1, 0), (0, -1)])
        template = self.size / 3 * template  # scale template

        v = 1.0 / np.sqrt(2)
        rot90 = np.array([(0, 1), (-1, 0)])
        rot45 = np.array([(v, -v), (v, v)])  # neg

        # align the template with the first action.
        t0 = np.dot(template, rot90)
        t0 = np.dot(t0, rot90)
        t0 = np.dot(t0, rot90)

        t1 = np.dot(t0, rot45)
        t2 = np.dot(t1, rot45)
        t3 = np.dot(t2, rot45)
        t4 = np.dot(t3, rot45)
        t5 = np.dot(t4, rot45)
        t6 = np.dot(t5, rot45)
        t7 = np.dot(t6, rot45)

        self.t = [t0, t1, t2, t3, t4, t5, t6, t7]

    def indx2coord(self, s, center=False):
        # the +1 indexing business is to ensure that the grid cells
        # have borders of width 1px
        i, j = self.coords(s)
        if center:
            return i * (self.size + 1) + 1 + self.size / 2, \
                   j * (self.size + 1) + 1 + self.size / 2
        else:
            return i * (self.size + 1) + 1, j * (self.size + 1) + 1

    def accessible_blocks(self, s):
        """
        For a give state s, generate the list of walls around it.
        """
        W = []
        if s in self.walls:
            return W
        if s - self.ncols < 0 or s - self.ncols in self.walls:
            pass
        else:
            W.append(s - self.ncols)
        if s - 1 < 0 or s - 1 in self.walls:
            pass
        else:
            W.append(s - 1)
        if s + 1 in self.walls:
            pass
        else:
            W.append(s + 1)
        if s + self.ncols in self.walls:
            pass
        else:
            W.append(s + self.ncols)
        return W

    def coord2indx(self, (x, y)):
        return self.rcoords((x / (self.size + 1), y / (self.size + 1)))

    def draw_state_labels(self):
        font = pygame.font.SysFont("FreeSans", 10)
        for s in self.mdp.states:
            x, y = self.indx2coord(s, False)
            txt = font.render("%d" % s, True, (0, 0, 0))
            self.surface.blit(txt, (y, x))

        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

    def coord2state(self, coord):
        s = self.coord2indx(coord[0], coord[1])
        return s

    def state2circle(self, state, bg=True, blit=True):
        if bg:
            self.background()

        x, y = self.indx2coord(state, center=True)
        pygame.draw.circle(self.surface, (0, 0, 255), (y, x), self.size / 2)

        if blit:
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()

    def draw_region(self, M):

        for s in M:
            x, y = self.indx2coord(s, False)
            coords = pygame.Rect(y, x, self.size, self.size)
            pygame.draw.rect(self.bg, ((204, 255, 204)), coords)

        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()

    def draw_values(self, vals):
        """
        vals: a dict with state labels as the key
        """
        font = pygame.font.SysFont("FreeSans", 10)

        for s in self.mdp.states:
            x, y = self.indx2coord(s, False)
            v = vals[s]
            txt = font.render("%.1f" % v, True, (0, 0, 0))
            self.surface.blit(txt, (y, x))

        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

    def save(self, filename):
        pygame.image.save(self.surface, filename)

    def redraw(self):
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

    def follow(self, policy):
        action = str(np.random.choice(a=self.actlist, p=policy))
        print(action)
        self.move(action)
        time.sleep(1)

    def move_obj(self, s, bg=True, blit=True):

        """Including A moving object into the gridworld, which moves uniformly at
        random in all accessible directions (including idle), without
        hitting the wall or another other statitic obstacle.  Input: a
        gridworld gui, the current state index for the obstacle and the
        number of steps.

        """
        if bg:
            self.background()
        next_s = choice(self.accessible_blocks(s))
        x, y = self.indx2coord(next_s, center=True)
        pygame.draw.circle(self.surface, (205, 92, 0), (y, x), self.size / 2)

        if blit:
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()
        return next_s

    def move(self, act, obs=False):
        self.current = self.mdp.sample(self.current, act)
        if self.updategui:
            self.state2circle(self.current)
        return

    def move_deter(self, next_state):
        self.current = next_state
        if self.updategui:
            self.state2circle(self.current)
        return

    def background(self):

        if self.bg_rendered:
            self.surface.blit(self.bg, (0, 0))
        else:
            self.bg.fill((0, 0, 0))
            for s in range(self.nstates):
                x, y = self.indx2coord(s, False)
                coords = pygame.Rect(y, x, self.size, self.size)
                pygame.draw.rect(self.bg, ((250, 250, 250)), coords)

            for t in self.targets:
                x, y = self.indx2coord(t, center=True)
                coords = pygame.Rect(y - self.size / 2, x - self.size / 2, self.size, self.size)
                pygame.draw.rect(self.bg, (0, 204, 102), coords)

                # Draw Wall in black color.
            for s in self.edges:
                (x, y) = self.indx2coord(s)
                # coords = pygame.Rect(y-self.size/2, x - self.size/2, self.size, self.size)
                coords = pygame.Rect(y, x, self.size, self.size)
                pygame.draw.rect(self.bg, (192, 192, 192), coords)  # the obstacles are in color grey

            for s in self.obstacles:
                (x, y) = self.indx2coord(s)
                coords = pygame.Rect(y, x, self.size, self.size)
                pygame.draw.rect(self.bg, (255, 0, 0), coords)  # the obstacles are in color red

        self.bg_rendered = True  # don't render again unless flag is set
        self.surface.blit(self.bg, (0, 0))

    def mainloop(self):
        """
        The robot moving in the Grid world with respect to the specification in DRA.
        """
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pgl.QUIT:
                    sys.exit()
                elif event.type == pgl.KEYDOWN and event.key == pgl.K_ESCAPE:
                    sys.exit()
                else:
                    pass

            self.mdp.update_alpha(self.current)
            x = self.mdp.primal_linear_program()
            policy = x[0, self.current, :] / np.sum(x[0, self.current, :])

            self.follow(policy)
            #raw_input('Press Enter to continue ...')
            if self.current in self.walls:
                # hitting the obstacles
                #print "Hitting the walls, restarting ..."
                # raw_input('Press Enter to restart ...')
                self.current = self.mdp.init  # restart the game
                print "the current state is {}".format(self.current)
                self.state2circle(self.current)
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()
