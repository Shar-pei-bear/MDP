import numpy as np

metrics = np.load('metrics.npy')
print metrics[:, :, 2]
