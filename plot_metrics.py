import numpy as np
import matplotlib.pyplot as plt


metrics = np.load('data/metrics.npy')
cases = [r'$1\,decoy$', r'$2\,decoys$', r'$3\,decoys$', r'$4\,decoys$', r'$5\,decoys$']
colors = ['#1f77b4',
          '#ff7f0e',
          '#2ca02c',
          '#d62728',
          '#9467bd',
          '#8c564b',
          '#e377c2',
          '#7f7f7f',
          '#bcbd22',
          '#17becf',
          '#1a55FF']

frequency = [0, 1.0/5.0, 1.0/4, 1.0/3, 1.0/2, 1.0/1]
success_rate = np.flip(metrics, axis=1)
success_rate = np.roll(success_rate, 1, axis=1)
fig, ax = plt.subplots()
for i in range(len(cases)):
    ax.plot(frequency, success_rate[i, :, 2], marker='o', color=colors[i], label=cases[i])
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Success rate')
plt.savefig('frequency.png', format='png', dpi=300, bbox_inches='tight')
#plt.title('The relationship between roaming frequency and attacker success rate')
plt.show()

cases = [r'$0Hz$', r'$\frac{1}{5}Hz$', r'$\frac{1}{4}Hz$', r'$\frac{1}{3}Hz$', r'$\frac{1}{2}Hz$', r'$1Hz$']
fig, ax = plt.subplots()
for i in range(len(cases)):
    ax.plot(success_rate[:, i, 0], success_rate[:, i, 2], marker='o', color=colors[i], label=cases[i])
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.xlabel('Number of decoys')
plt.ylabel('Success rate')
plt.savefig('num_decoys.png', format='png', dpi=300, bbox_inches='tight')
#plt.title('The relationship between roaming frequency and attacker success rate')
plt.show()