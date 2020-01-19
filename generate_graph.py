import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.fast_gnp_random_graph(20, 0.1, directed=True)
values = np.ones(G.number_of_nodes()) * 0.25
print values

fig = plt.figure()
ax1 = nx.draw_kamada_kawai(G, cmap=plt.get_cmap('viridis'), node_color=values, with_labels=True,
        font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.show()

flag = True
for node in list(G.nodes):
    if G.degree(node) == 0:
        print 'graph not fully connected'
        flag = False
        break
if flag:
    nx.write_gml(G, "network_topology")