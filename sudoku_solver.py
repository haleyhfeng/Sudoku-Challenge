import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.sparse as scs # sparse matrix construction 
import scipy.linalg as scl # linear algebra algorithms
import scipy.optimize as sco # for minimization use
import matplotlib.pylab as plt # for visualization

from constraint import fixed_constraints, clue_constraint
from cvxopt import solvers, matrix
import time

def solver(quiz, solu):
    A0 = fixed_constraints()
    A1 = clue_constraint(quiz)

    # Formulate the matrix A and vector B (B is all ones).
    A = scs.vstack((A0,A1))
    A = A.toarray()
    B = np.ones(A.shape[0])

    # Because rank defficiency. We need to extract effective rank.
    u, s, vh = np.linalg.svd(A, full_matrices=False)
    K = np.sum(s > 1e-12)
    S_ = np.block([np.diag(s[:K]), np.zeros((K, A.shape[0]-K))])
    A = S_@vh
    B = u.T@B
    B = B[:K]

    c = matrix(np.block([ np.ones(A.shape[1]), np.ones(A.shape[1]) ]))
    G = matrix(np.block([[-np.eye(A.shape[1]), np.zeros((A.shape[1], A.shape[1]))],\
                         [np.zeros((A.shape[1], A.shape[1])), -np.eye(A.shape[1])]]))
    h = matrix(np.zeros(A.shape[1]*2))
    H = matrix(np.block([A, -A]))
    b = matrix(B)

    sol = solvers.lp(c,G,h,H,b)
    X = np.array(sol['x']).T[0]
    x = X[:A.shape[1]] - X[A.shape[1]:]

    # map to board
    z = np.reshape(x, (81, 9))


    return z
