from graphworld import *

initial = 0
nstates = 8
obstacles = [1, 5]
targets_path = [[7, 7, 7, 7, 7, 7, 7]]
task_type ='sequential'
edges = [[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7)],
         [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)]]
actlist = ['a1', 'a2', 'a3', 'a4']
gwg = GraphworldGui(initial, nstates, edges, actlist, targets_path, obstacles,  task_type)
gwg.mainloop()




