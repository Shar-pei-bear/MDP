import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.read_gml("network_topology")
values = np.ones(G.number_of_nodes()) * 0.25

fig = plt.figure()
ax1 = nx.draw_kamada_kawai(G, cmap=plt.get_cmap('Wistia'), node_color=values, with_labels=True,
        font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.show()