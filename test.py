import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.sparse as scs # sparse matrix construction 
import scipy.linalg as scl # linear algebra algorithms
import scipy.optimize as sco # for minimization use
import matplotlib.pylab as plt # for visualization

from cvxopt import solvers, matrix
import time
solvers.options['show_progress'] = False

data = pd.read_csv("data/small1.csv") 

corr_cnt = 0
start = time.time()
for i in range(len(data)):
    quiz = data["quizzes"][i]
    solu = data["solutions"][i]
    z = solver(quiz, solu)
    D = np.reshape(np.array([np.argmax(d)+1 for d in z]), (9,9) ) \
        - np.reshape([int(c) for c in solu], (9,9))
    if np.linalg.norm(D, np.inf) > 0: # Checking if solution is correct
        New = np.array([np.argmax(d)+1 for d in z]) # sudoku solution in 1d array form
        D = D.reshape(-1) # array with zero or nonzero
        for j in range(len(D)):
            if D[j] != 0: 
                New[j] = 0 # replace repeated variable with zero
        new_z = solver(New, solu) # solve new puzzle using LP 
        if np.linalg.norm(np.reshape(np.array([np.argmax(d)+1 for d in new_z]), (9,9) ) \
        - np.reshape([int(c) for c in solu], (9,9)), np.inf) > 0:
            pass
        else:
            #print("CORRECT",i)
            corr_cnt += 1
        
    else:
        #print("CORRECT",i)
        corr_cnt += 1
    
    if (i+1) % 20 == 0:
        end = time.time()
        print("Aver Time: {t:6.2f} secs. Success rate: {corr} / {all} ".format(t=(end-start)/(i+1), corr=corr_cnt, all=i+1) )
end = time.time()
print("Aver Time: {t:6.2f} secs. Success rate: {corr} / {all} ".format(t=(end-start)/(i+1), corr=corr_cnt, all=i+1) )
