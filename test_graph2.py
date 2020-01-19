from graphworld import *

initial = 17  # 0
targets = [7]  # 7
num_obstacles = 0
task_type = 'sequential'
network_file = 'network_topology'
T = 0
gwg = GraphworldGui(network_file, initial, targets, num_obstacles, T, task_type)
gwg.mainloop()
metrics = np.zeros((5, 6, 3))
max_decoy_number = 6
max_T = 6
max_experiment_num = 100
for decoy_number in range(1, max_decoy_number):
    gwg.num_obstacles = decoy_number
    for T in range(max_T):
        count = 0.0
        gwg.T = T
        for index in range(max_experiment_num):
            print 'The decoy number is ', decoy_number
            print 'The period is ', T
            print 'Instance ', index
            gwg.sample_obstacles()
            if gwg.mainloop():
                count = count + 1.0
            gwg.reset()
        metrics[decoy_number - 1, T, 0] = decoy_number
        metrics[decoy_number - 1, T, 1] = T
        metrics[decoy_number - 1, T, 2] = count / max_experiment_num
    np.save('metrics', metrics)
# metrics = np.load('metrics.npy')
# print metrics[0, 0, :]









