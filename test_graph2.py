from graphworld import *

initial = 17  # 0
targets = [7]  # 7
num_obstacles = 0
task_type = 'sequential'
network_file = 'network_topology'
T = 0
visualization = False
# decoys_set = random.sample(range(20), 10)
decoys_set = [0, 12, 2, 8, 1, 13, 15, 10, 9, 5]
gwg = GraphworldGui(network_file, initial, targets, num_obstacles, T, task_type, visualization, decoys_set)
# gwg.mainloop()

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
            gwg.mdp.prob = gwg.getProbs()
            if gwg.mainloop():
                count = count + 1.0
        metrics[decoy_number - 1, T, 0] = decoy_number
        metrics[decoy_number - 1, T, 1] = T
        metrics[decoy_number - 1, T, 2] = count / max_experiment_num
    np.save('metrics', metrics)
# metrics = np.load('metrics.npy')
# print metrics[0, 0, :]









