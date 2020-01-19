import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.read_gml("network_topology")
values = np.ones(G.number_of_nodes()) * 0.25
values[0] = 1

fig = plt.figure()
ax1 = nx.draw_kamada_kawai(G, cmap=plt.get_cmap('viridis'), nodelist=[str(e) for e in range(20)], node_color=values, with_labels=True,
        font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.show()
print G.in_degree('0')
for node in list(G.nodes):
    if G.in_degree(node) == 0:
        print 'graph not fully connected'
        break
