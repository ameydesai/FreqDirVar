import traceback
import argparse
import numpy as np


def fd(imat, skrows):
    ncols = imat.shape[1]
    nrows = imat.shape[0]
    
    sketch = np.zeros((skrows, ncols))
    sketch[0 :  skrows - 1, : ] = imat[0 : skrows - 1, : ]
    
    U, s, Vt = np.linalg.svd(sketch)    
    new_s = [np.sqrt(cur_s ** 2 - s[len(s) - 1] ** 2) for cur_s in s ]
    
    sketch = np.dot(np.diagflat(new_s), Vt)
    

    for i in range(skrows, nrows):
        sketch[skrows - 1, :] = imat[i, :]
        
        U, s, Vt = np.linalg.svd(sketch)    
        new_s = [np.sqrt(cur_s ** 2 - s[len(s) - 1] ** 2) for cur_s in s ]
    
        sketch = np.dot(np.diagflat(new_s), Vt)

