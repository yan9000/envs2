

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__=="__main__":
    inf = open('Data/best4knn.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    
    c = x + y
    
    ax.scatter(x, y, z, c=c)
    plt.show()