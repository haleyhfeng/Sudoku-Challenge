import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.sparse as scs # sparse matrix construction 
import scipy.linalg as scl # linear algebra algorithms
import scipy.optimize as sco # for minimization use
import matplotlib.pylab as plt # for visualization

from constraint import fixed_constraints, clue_constraint
from functions import boxes, repeats, convert_stringtoarray, convert_matrixtolist
import time
from collections import defaultdict

def solver(input_):
    
    quiz = input_
    constraint_ = input_
    iter_ = 0
    X_re = 0
    while(iter_<=10):
        
        A0 = fixed_constraints()
        A1 = clue_constraint(constraint_)
        # Formulate the matrix A and vector B (B is all ones).
        A = scs.vstack((A0,A1))
        A = A.toarray()
        B = np.ones(A.shape[0])
        # Because rank defficiency. We need to extract effective rank.

        u, s, vh = np.linalg.svd(A, full_matrices=False)
        K = np.sum(s > 1e-12)
        S = np.block([np.diag(s[:K]), np.zeros((K, A.shape[0]-K))])
        A = S@vh
        B = u.T@B
        B = B[:K]
        c = np.block([ np.ones(A.shape[1]), np.ones(A.shape[1]) ])

        G = np.block([[-np.eye(A.shape[1]), np.zeros((A.shape[1], A.shape[1]))],\
                             [np.zeros((A.shape[1], A.shape[1])), -np.eye(A.shape[1])]])
        h = np.zeros(A.shape[1]*2)
        H = np.block([A, -A])
        b = B
        L = 20
        epsilon = 10**-10
        x_top = np.zeros(A.shape[1])
        x_bottom = np.zeros(A.shape[1])
        x_ori = x_top - x_bottom
        for j in range(L):
            Weight = 1/(abs(x_ori)+0.7)
            W = np.block([Weight,Weight])
            cW = np.matrix(c*W)
            ret = sco.linprog(cW, G, h, H, b, method='interior-point', options={'tol':1e-10})
            x_new = ret.x[:A.shape[1]] - ret.x[A.shape[1]:]
            #x_new = np.reshape(x, (81, 9))
            if LA.norm((x_new - x_ori)) <epsilon:
                break
            else:
                x_ori = x_new
    
        x_re = np.reshape(x_new, (81, 9))
        X_re = x_re
        u = np.array([np.argmax(d)+1 for d in x_re])
        after_del = repeats(convert_stringtoarray(u), convert_stringtoarray(quiz))  # starting x's    
        new_x_ori = np.array(convert_matrixtolist(after_del))
        constraint_ = new_x_ori
        iter_+=1
    ans =  np.array([np.argmax(d)+1 for d in X_re])
    return ''.join([str(c) for c in ans]) 
    
