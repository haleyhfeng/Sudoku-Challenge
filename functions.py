import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.sparse as scs # sparse matrix construction 
import scipy.linalg as scl # linear algebra algorithms
import scipy.optimize as sco # for minimization use
import matplotlib.pylab as plt # for visualization

from collections import defaultdict

def boxes():

    index = defaultdict(list)
    ind = []
    for i in range(9):
        for j in range(9):
            ind.append([i,j])
    res1 = []
    res2 = []
    res3 = []
    res4 = []
    res5 = []
    res6 = []
    res7 = []
    res8 = []
    res9 = []
    for item in ind:
        i = item[0]
        j = item[1]
        if i%9>=0 and i%9<=2:
            if j%9>=0 and j%9<=2:
                res1.append(item)
        if i%9>=0 and i%9<=2:
            if j%9>=3 and j%9<=5:
                res2.append(item)
        if i%9>=0 and i%9<=2:
            if j%9>=6 and j%9<=8:
                res3.append(item)
        if i%9>=3 and i%9<=5:
            if j%9>=0 and j%9<=2:
                res4.append(item)

        if i%9>=3 and i%9<=5:
            if j%9>=3 and j%9<=5:
                res5.append(item)
        if i%9>=3 and i%9<=5:
            if j%9>=6 and j%9<=8:
                res6.append(item)
        if i%9>=6 and i%9<=8:
            if j%9>=0 and j%9<=2:
                res7.append(item)

        if i%9>=6 and i%9<=8:
            if j%9>=3 and j%9<=5:
                res8.append(item)
        if i%9>=6 and i%9<=8:
            if j%9>=6 and j%9<=8:
                res9.append(item)
    box = [res1, res2, res3, res4, res5, res6, res7, res8, res9]
    return box

from collections import defaultdict

def repeats(matrix, original):
    #print(matrix)
    temp = defaultdict(list)
    marked_matrix = np.ones((9,9))
    for i in range(9):
        for j in range(9):
            mark = False
            val = matrix[i][j]
            temp[val].append([i,j])
            #print(val)
            
            for l in range(9):
                if matrix[l][j] == val and i!= l:
                    mark = True

                    marked_matrix[l][j] = 0
                    temp[val]
        
    
                    #print(marked_matrix)
            for k in range(9):
                if matrix[i][k]== val and k!= j:
                    mark = True
                    marked_matrix[i][k] = 0
                    
            for res in boxes():
                if [i,j] in res:
                    for each_sq in res:
                        a = each_sq[0]
                        b = each_sq[1]
                        if matrix[a][b] == val and [a,b] != [i,j] :
                            mark = True
                            marked_matrix[a][b] = 0
                        
                    if mark == True:
                        marked_matrix[i][j] = 0
                    
    for i in range(9):
        for j in range(9):
            if marked_matrix[i][j] ==0:
                matrix[i][j] = 0
    for i in range(9):
        for j in range(9):
            if original[i][j] != 0 :
                matrix[i][j] = original[i][j]
                

    return matrix
            


def convert_stringtoarray(quiz):
    #can work for original and solution
    res = []
    count = 0
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append(int(quiz[count]))
            count+=1
        res.append(temp)

    return res

def convert_matrixtolist(after_del):
    res = []
    for i in after_del:
        for j in i:
            res.append(j)
    
    return res

