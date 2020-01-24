import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.read_gml("network_topology")
values = np.ones(G.number_of_nodes()) * 0.25
values[17] = 1
values[7] = 0.5

fig = plt.figure()
ax1 = nx.draw_shell(G, cmap=plt.get_cmap('viridis'), nodelist=[str(e) for e in range(20)], node_color=values, with_labels=True,
        font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.savefig('graph.png', format='png', dpi=300)
plt.show()
# print G.in_degree('0')
# for node in list(G.nodes):
#     if G.in_degree(node) == 0:
#         print 'graph not fully connected'
#         break
