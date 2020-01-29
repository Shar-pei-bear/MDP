import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import matplotlib.cbook as cbook
# import seaborn as sns

nstates = 8
static_cost = np.load('graph_static_cost.npy')
dynamic_cost = np.load('graph_dynamic_cost.npy')
#print np.max(dynamic_cost - static_cost)
# 7, 13, 9, 11, 10, 0, 19
conf_intervals = np.zeros((7, 2))
conf_intervals[:, 1] = 1
box_colors = ['darkkhaki', 'royalblue']
regret_mean = np.mean(dynamic_cost[:, [7, 13, 9, 11, 10, 0, 19]] - static_cost[:, [7, 13, 9, 11, 10, 0, 19]], axis=0)
regret = dynamic_cost[:, [7, 13, 9, 11, 10, 0, 19]] - static_cost[:, [7, 13, 9, 11, 10, 0, 19]]

regret_std = np.std(regret, axis = 0)
labels = ['0', '1', '2', '3', '4', '5', '6']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x, regret_mean, width, label='Mean')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Regret')
ax.set_xlabel('Distance to target')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(np.round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)

fig.tight_layout()
plt.savefig('regret_bar.png', format='png', dpi=300)
plt.show()

# stats = cbook.boxplot_stats(regret, whis=1.5, labels=range(7))
# fig1, ax1 = plt.subplots()
# bp = ax1.boxplot(regret, showmeans=True, labels=range(7))
# plt.setp(bp['boxes'], color='black')
# plt.setp(bp['whiskers'], color='black')
# plt.setp(bp['fliers'], color='red', marker='+')
#
# ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
#                alpha=0.5)
#
# # Hide these grid behind plot objects
# ax1.set_axisbelow(True)
# ax1.set_xlabel('Distance to target')
# ax1.set_ylabel('Regret')
# top = 1.8
# bottom = 0
# ax1.set_ylim(bottom, top)
#
# num_boxes = 7
# pos = np.arange(num_boxes) + 1
# upper_labels = [str(np.round(s, 2)) for s in regret_mean]
# weights = ['bold', 'semibold']
# for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
#     k = tick % 2
#     ax1.text(pos[tick], .97, upper_labels[tick],
#              transform=ax1.get_xaxis_transform(),
#              horizontalalignment='center', size='medium',
#              weight=weights[k], color=box_colors[k])
#
# plt.savefig('regret.png', format='png', dpi=300)
# plt.show()
# dynamic_cost = dynamic_cost[8, :]
# static_cost = static_cost[8, :]
#
# network_file = 'network_topology'
# dg = nx.read_gml(network_file)
#
# values = dynamic_cost
# fig = plt.figure()
# ax1 = nx.draw_circular(dg,  nodelist=[str(i) for i in range(20)], cmap=plt.get_cmap('coolwarm'), vmin=1, vmax=2.72,
#                        node_color=values, with_labels=True, font_color='white', font_weight='bold')
#
# fig.axes[0].axis('equal')
# plt.savefig('graph_dynamic_map.png', format = 'png', dpi = 300)
#
# plt.show()
#
# fig = plt.figure()
# values = static_cost
# ax2 = nx.draw_circular(dg,  nodelist=[str(i) for i in range(20)], cmap=plt.get_cmap('coolwarm'), vmin=1, vmax=2.72,
#                        node_color=values, with_labels=True, font_color='white', font_weight='bold')
# fig.axes[0].axis('equal')
# plt.savefig('graph_static_map.png', format='png', dpi=300)
# plt.show()

# print dynamic_cost
# print static_cost
# print np.max(dynamic_cost - static_cost)
# print np.argmax(dynamic_cost - static_cost)

optimal_success = (dynamic_cost[:, [7, 13, 9, 11, 10, 0, 19]] - 1) / (np.exp(1) - 1)
optimal_success_mean = np.mean(optimal_success, axis=0)

online_success = (static_cost[:, [7, 13, 9, 11, 10, 0, 19]] - 1) / (np.exp(1) - 1)
online_success_mean = np.mean(online_success, axis=0)

# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, optimal_success_mean, width, label='Optimal')
# rects2 = ax.bar(x + width/2, online_success_mean, width, label='Online')
#
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Success rate')
# ax.set_xlabel('Distance to target')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.set_ylim(0, 1.25)
# ax.legend(loc='upper left')
#
#
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(np.round(height, 2)),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
#
# autolabel(rects1)
# autolabel(rects2)
#
# fig.tight_layout()
# plt.savefig('success_rate.png', format='png', dpi=300)
# plt.show()
#
# #online_success_mean = online_success_mean[2: ]
# obs = np.vstack((online_success_mean, 1 - online_success_mean))*100
# obs = np.round(obs)
# #obs = np.array([[10, 20, 30, 40, 50], [50, 40, 30, 20, 10]])
# print obs
# chi2, p, dof, ex = chi2_contingency(obs)
# print p
# print dof
