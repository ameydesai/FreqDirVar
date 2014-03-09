import numpy as np

rand_mat = np.random.random((50, 100)) * np.random.randint(0, 1000)
u,s, v = np.linalg.svd(rand_mat)
print u.shape, np.diagflat(s).shape, v.shape
u,s, v = np.linalg.svd(rand_mat, full_matrices = False)
print u.shape, np.diagflat(s).shape, v.shape
