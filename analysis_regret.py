import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
static_cost = np.load('static_cost.npy')
static_map = static_cost.reshape([8, 10])
dynamic_cost = np.load('dynamic_cost.npy')
dynamic_map = dynamic_cost.reshape([8, 10])

fig = plt.figure()
ax1 = sns.heatmap(static_map, vmin=0, vmax=1.5, linewidth=0.5)
plt.savefig('static_map.png', format = 'png', dpi = 300)
plt.show()

ax2 = sns.heatmap(dynamic_map, vmin=0, vmax=1.5, linewidth=0.5)
plt.savefig('dynamic_map.png', format = 'png', dpi = 300)
plt.show()

print(static_cost[45])
print(dynamic_cost[45])