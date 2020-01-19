import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
nstates = 8
static_cost = np.load('graph_static_cost.npy')
dynamic_cost = np.load('graph_dynamic_cost.npy')
print static_cost
print dynamic_cost

edges = [[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7)],
         [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)]]

dg = nx.DiGraph()
dg.add_nodes_from(range(nstates))
dg.add_edges_from(edges[0])
pos = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (2, 1), 4: (3, 1), 5: (3, 0), 6: (4, 1), 7: (4, 0)}

values = np.log(dynamic_cost)
print values
fig = plt.figure()
ax1 = nx.draw(dg, pos=pos, cmap=plt.get_cmap('Wistia'), node_color=values, with_labels=True,
        font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.savefig('graph_dynamic_map.png', format = 'png', dpi = 300)
plt.show()

fig = plt.figure()
values = np.log(static_cost)
ax2 = nx.draw(dg, pos=pos, cmap=plt.get_cmap('Wistia'), node_color=values, with_labels=True,
        font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.savefig('graph_static_map.png', format='png', dpi=300)
plt.show()

print dynamic_cost - static_cost