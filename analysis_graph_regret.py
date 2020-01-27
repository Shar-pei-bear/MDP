import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

nstates = 8
static_cost = np.exp(np.load('graph_static_cost.npy'))
dynamic_cost = np.load('graph_dynamic_cost.npy')
print np.max(dynamic_cost  - static_cost)

dynamic_cost = dynamic_cost[8, :]
static_cost = static_cost[8, :]

network_file = 'network_topology'
dg = nx.read_gml(network_file)

values = dynamic_cost
fig = plt.figure()
ax1 = nx.draw_circular(dg,  nodelist=[str(i) for i in range(20)], cmap=plt.get_cmap('coolwarm'), vmin=1, vmax=2.72,
                       node_color=values, with_labels=True, font_color='white', font_weight='bold')

fig.axes[0].axis('equal')
plt.savefig('graph_dynamic_map.png', format = 'png', dpi = 300)

plt.show()

fig = plt.figure()
values = static_cost
ax2 = nx.draw_circular(dg,  nodelist=[str(i) for i in range(20)], cmap=plt.get_cmap('coolwarm'), vmin=1, vmax=2.72,
                       node_color=values, with_labels=True, font_color='white', font_weight='bold')
fig.axes[0].axis('equal')
plt.savefig('graph_static_map.png', format='png', dpi=300)
plt.show()

# print dynamic_cost
# print static_cost
# print np.max(dynamic_cost - static_cost)
# print np.argmax(dynamic_cost - static_cost)

