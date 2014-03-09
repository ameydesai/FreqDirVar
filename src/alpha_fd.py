import traceback
import argparse
import numpy as np
import csv



def alpha_fd(imat, skrows, alpha):
    
    ncols = imat.shape[1]
    nrows = imat.shape[0]

    sketch = np.zeros((skrows, ncols))
    print sketch.shape
    sketch[0 : skrows - 2, : ] = imat[0 : skrows - 2, :]
    i = skrows - 1
    while i < nrows:

        j = skrows - 1
        while j >= 0 and np.all(sketch[j, :] == 0):
                j -= 1
                
        nr = min(skrows-j-1 , nrows-i)
        sketch[j+1:j+nr+1 , :] = imat[i:i+nr, :]
        i = i + nr
        U, s, Vt = np.linalg.svd(sketch, full_matrices = False)    
    
        k = 0
        sl = len(s)
        for k in range(sl - 1, -1):
            if s[k] != 0:
                break
            
        while k < len(s) - 1 and i < nrows:
            #print np.diagflat(s).shape, Vt.shape, U.shape
            sketch = np.dot(np.diagflat(s), Vt)
            nr = min(skrows-1-k , nrows-i)
            sketch[k+1 : k+nr+1,  : ] = imat[i : i+nr, :]
            i = i + nr
            U, s, Vt = np.linalg.svd(sketch, full_matrices = False)            
            for k in range(len(s) - 1, -1):
                if s[k] != 0:
                    break
        if i < nrows:
            leastsv = s[len(s)-1]
            rowIdx = int(np.ceil((1-alpha)*skrows))
            for k in range(rowIdx , skrows):
                s[k] = np.sqrt(s[k] ** 2 - leastsv ** 2)
            s[skrows-1] = 0
            sketch = np.dot(np.diagflat(s),Vt)

    sketch = np.dot(np.diagflat(s),Vt)
    rank_k = np.ceil(0.4*skrows)-1
    return sketch[0:rank_k,:]
        
def generateData(m, n):
    rand_mat = np.random.random((m, n)) * np.random.randint(0, 1000)
    return rand_mat

def error(imat, sketch):
    num = np.linalg.norm(np.dot(imat.transpose(), imat) - np.dot(sketch.transpose(), sketch) , 2)
    den = np.linalg.norm(imat, 'fro') ** 2
    temp = num/den
    print "Error: %s" % temp 
    print num


#data = generateData(500, 100)
#a = alpha_fd(data,20,1) 
#print a
import ast
f = open("../data/batch2.dat", "r")
data = f.readlines()
imat = []
for val in data:
    temp = val.split(' ')[1:]
    row = []
    for val1 in temp:
        row.append(ast.literal_eval(val1.split(":")[1]))

    imat.append(row)
imat = np.array(imat)
a = alpha_fd(imat, 20, 1)
print error(imat, a)
import scipy.io as sp

sp.savemat("batch2.mat", mdict = {'data' : imat})
