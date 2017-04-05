import scipy.integrate as integrate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm

def phi(x):
    return 1 - x / 2


def f(x):
    return x


def g(t):
    return 1+t


def rho(x):
    return x*x - x

L = 1
count = 10
h = L / count
solution = [[0]*(count+1) for i in range(count+1)]

def solveDirectProblem():
    for i in range(count+1):
        for j in range(count+1):
            if(i <= j):
                x = j * h;
                t = i * h;
                solution[i][j] = phi(x-t) - integrate.quad(lambda z: f(z)*g(t-x+z), x-t, x)[0]
    for i in range(count+1):
        for j in range(count+1):
            
                
                 
                          
                
solveDirectProblem()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.grid(True)

#plt.ylim((0.0, 1.0))
#plt.xlim((0, 0.5))
#ax.plot(solution, split_y, color='b', label='y')
for i in range(count+1):
    for j in range(count+1):
        ax.scatter(i/count+1, j/count+1, solution[i][j], c='r', marker='o')
#ax.plot(k1_array, x_array, color='r', label='x')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.legend()
plt.show()

            


