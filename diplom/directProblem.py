import scipy.integrate as integrate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from sympy import diff
import math

def phi(x):
    return 1 - x/2

def phi_x(x):
    return -1/2


def f(x):
    return x/2


def g(t):
    #return 1 + math.sin(t)/4
    return 1-t
    
def g_t(t):
    return -1


def rho(x):
    #return 2*math.pi/3 * math.sin(math.pi * x)
    #math.sin(math.pi * x) ** 2
    return 3*x

def getSolution(x,t):
    #print("x",x)
    #print("t",t)
    #print("sol=", solution[round(t)][round(x)])
    return solution[round(t)][round(x)]
                    
               
def c_t(c, i):
    if i != 0 and i != len(c):
        return (c[i+1]-c[i-1])/h
    else:
        if i == 0:
            return (c[1] - c[0]) / h
        else:
            return (c[i] - c[i-1])/h
                  
            
L = 1
count = 50
h = L / count
solution = [[0]*(count+1) for i in range(count+1)]
psi = [phi(0)] * (count+1)
#psi = [0] * (count+1)

def solveDirectProblem():
    for i in range(count+1):
        for j in range(count+1):
            if(i <= j):
                x = j * h
                t = i * h
                solution[i][j] = phi(x-t) - integrate.quad(lambda z: f(z)*g(t-x+z), x-t, x)[0]
                #solution[i][j] = phi(x-t) - 1/12*t*(t**2 + 6*x - 3*t*(1 + x))
    #print("aaaaaaaaaaaaaaaaa", solution)
    
    for tau in range(14):
        norm = 0
        for i in range(count+1):
            t = i * h
            #first_term = integrate.quad(lambda s: rho(s)*getSolution(s,t), t, 1)[0] 
            first_term = 0
            for k in range((int)((1-t)/h)):
                left_dot = t + k * h
                right_dot = t + (k+1)*h
                first_term += h/2 *(rho(left_dot)*solution[i][(int)(left_dot/h)] + rho(right_dot)*solution[i][(int)(right_dot/h)])
            second_term = -integrate.dblquad(lambda n, s: rho(s)*f(n)*g(t-s+n), 0, t, lambda s: 0, lambda s: s)[0]
            #third_term = integrate.quad(lambda s: rho(s)*getPsi(t-s), 0, t)[0]
            third_term = 0
            for k in range(i):
                left_dot = k * h
                right_dot = (k+1)*h
                third_term += h/2 * (rho(left_dot) * psi[k] + rho(right_dot) * psi[k+1])
            '''print("first=",first_term)
            print("second=",second_term)
            print("third=",third_term)
            print("sum_all", first_term + second_term + third_term)
            print("--------------------")'''
            norm += (psi[i] - (first_term + second_term + third_term)) ** 2
            psi[i] =  first_term + second_term + third_term
        print("norm", norm)
        print("------")
    
    
    print("psi = ", psi)
    for i in range(count+1):
        for j in range(count+1):
            if(i > j):
                x = j * h
                t = i * h
                solution[i][j] = getPsi(t-x) - integrate.quad(lambda z: f(z)*g(t-x+z), 0, x)[0]
          
        

def solveReverseProblem(x_0):
    for k in range(1):
        for i in range(x_0+1):
            tau = i * h
            reverse_f[i] = reverse_f[i] - 1/g(0) * (integrate.quad(lambda n: f(n)*g_t(n-tau), tau, x_0*h)[0] + phi_x(tau) + c_t(c, x_0-i) )
                              
                
solveDirectProblem()
min1 = solution[0][0]
max1 = solution[0][0]
min2 = solution[1][0]
max2 = solution[1][0]
for i in range(count+1):
    for j in range(count+1): 
        if(j >= i and solution[i][j] > max1):
            max1 = solution[i][j]
        if(j >= i and solution[i][j] < min1):
            min1 = solution[i][j]
        if(j < i and solution[i][j] > max2):
            max2 = solution[i][j]
        if(j < i and solution[i][j] < min2):
            min2 = solution[i][j]
print("max1=", max1)
print("min1=", min1)
print("max2=", max2)
print("min2=", min2)

#reverse_f = [0] * (count+1)
#x_0 = (int) (count - count / 10)
#c = [row[x_0] for row in solution]
#print("c", c)
#print("x_0 = ", x_0)
#solveReverseProblem(x_0)
#print("reverse_f", reverse_f)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.grid(True)

#plt.ylim((0.0, 1.0))
#plt.xlim((0, 0.5))
#ax.plot(solution, split_y, color='b', label='y')
for i in range(count+1):
    for j in range(count+1):
        if(i > j):
            ax.scatter(i/(count+1), j/(count+1), solution[i][j], c='r', marker='o')
        else:
            ax.scatter(i/(count+1), j/(count+1), solution[i][j], c='b', marker='o')
#ax.plot(k1_array, x_array, color='r', label='x')
ax.set_xlabel('Y Label')
ax.set_ylabel('X Label')
ax.set_zlabel('Z Label')

plt.legend()
plt.show()

          
