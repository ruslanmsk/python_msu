import sympy
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

x = sympy.Symbol("x")
y = sympy.Symbol("y")
k1 = sympy.Symbol("k1")
k2 = sympy.Symbol("k2")
k3 = sympy.Symbol("k3")
k_1 = sympy.Symbol("k_1")
k_3 = sympy.Symbol("k_3")

# z=1-x-y
# инициализация уравнений
equation1 = k1 * (1-x-y) - k_1 * x - k2 * x * (1-x-y) ** 2
equation2 = k3 * (1-x-y) ** 2 - k_3 * y ** 2
# надоходим стационарные решения(при каких x и k1 уравнение равно 0)
# два решения
res = sympy.solve([equation1, equation2], x, k1, dict=True)
x_function = sympy.lambdify((y, k3, k_3), res[1][x])
k1_function = sympy.lambdify((y, k_1, k2, k3, k_3), res[1][k1])

A = sympy.Matrix([equation1, equation2])
jacobianMatrix = A.jacobian(sympy.Matrix([x, y]))
determinant = jacobianMatrix.det()
determinant_function = sympy.lambdify((x, y, k1, k2, k3, k_1, k_3), determinant)
trace = jacobianMatrix.trace()
trace_function = sympy.lambdify((x, y, k1, k2, k3, k_1, k_3), trace)


result_det_k1 = sympy.solve([determinant], k1)
k2_y_k1 = result_det_k1[k1].subs(x, res[1][x])
k2_y_k1_func = sympy.lambdify((y, k1, k3, k_1, k2), k2_y_k1)
det_y = k2_y_k1 - res[1][k1]


init_k1 = 0.12
init_k2 = 1.05
init_k3 = 0.0032
init_k_1 = 0.005
init_k_3 = 0.002

# уравнение относительно y для нахождения точек бифуркации
k1_y_init = det_y.subs(k2, init_k2).subs(k3,init_k3).subs(k_3,init_k_3).subs(k_1,init_k_1)


split_y = np.linspace(0.0001, 0.9999, num=1000)

x_res = x_function(split_y[0], init_k3, init_k_3)
k1_res = k1_function(split_y[0], init_k_1, init_k2, init_k3, init_k_3)
determinant_last = determinant_function(x_res, split_y[0], k1_res, init_k2, init_k3, init_k_1, init_k_3)
determinant_array = []
trace_array = []
x_array = []
k1_array = []
bifurcation_array = []
for i in split_y:
    x_res = x_function(i, init_k3, init_k_3)
    k1_res = k1_function(i, init_k_1, init_k2, init_k3, init_k_3)
    determinant_current = determinant_function(x_res, i, k1_res, init_k2, init_k3, init_k_1, init_k_3)
    determinant_array.append(determinant_current)
    if np.sign(determinant_last) != np.sign(determinant_current):
        bifurcation_array.append([i, x_res, k1_res])
    determinant_last = determinant_current
    trace_array.append(trace_function(x_res, i, k1_res, init_k2, init_k3, init_k_1, init_k_3))
    k1_array.append(k1_res)
    x_array.append(x_res)



# http://www.physics.nyu.edu/pine/pymanual/html/chap9/chap9_scipy.html


plt.figure("one-parameter analysis")
ax = plt.subplot(111)
plt.subplot(111)
plt.grid(True)
plt.xlabel('k1')
plt.ylabel('x, y')
plt.ylim((0.0, 1.0))
plt.xlim((0, 0.5))
ax.plot(k1_array, split_y, color='b', label='y')
ax.plot(k1_array, x_array, color='r', label='x')
ax.plot([bifurcation_array[0][2]], [bifurcation_array[0][1]], 'ro', color='c', label='bifurcation')
ax.plot([bifurcation_array[0][2]], [bifurcation_array[0][0]], 'ro', color='c')
ax.plot([bifurcation_array[1][2]], [bifurcation_array[1][1]], 'ro', color='c')
ax.plot([bifurcation_array[1][2]], [bifurcation_array[1][0]], 'ro', color='c')
plt.legend()


k1_draw_array = []
k_1_draw_array = []

k1_draw_array_2 = []
k_1_draw_array_2 = []

determinant_x_y = determinant.subs(x, res[1][x])
trace_x_y = trace.subs(x, res[1][x])

det_k1_on_k_1_y = sympy.solve(determinant_x_y, k1)
tr_k1_on_k_1_y = sympy.solve(trace_x_y, k1)

det_k_1_on_y = sympy.solve(det_k1_on_k_1_y[0] - res[1][k1], k_1)
tr_k_1_on_y = sympy.solve(tr_k1_on_k_1_y[0] - res[1][k1], k_1)

for i in split_y:
    det_local_k_1 = det_k_1_on_y[0].subs(k2, init_k2).subs(k3,init_k3).subs(k_3,init_k_3).subs(y,i)
    tr_local_k_1 = tr_k_1_on_y[0].subs(k2, init_k2).subs(k3,init_k3).subs(k_3,init_k_3).subs(y,i)
    det_local_k1 = k1_function(i, det_local_k_1, init_k2, init_k3, init_k_3)
    tr_local_k1 = k1_function(i, tr_local_k_1, init_k2, init_k3, init_k_3)
    k1_draw_array.append(det_local_k1)
    k_1_draw_array.append(det_local_k_1)
    k1_draw_array_2.append(tr_local_k1)
    k_1_draw_array_2.append(tr_local_k_1)


plt.figure("two-parameter analysis")
ay = plt.subplot(111)
plt.grid(True)
plt.ylim((0, 0.025))
plt.xlim((0, 0.2))
plt.xlabel('k1')
plt.ylabel('k_1')
ay.plot(k1_draw_array, k_1_draw_array, color='b', label="line expansion")  # кратности
ay.plot(k1_draw_array_2, k_1_draw_array_2, color='r', label="line of neutrality")  # нейтральности
ay.legend()
plt.show()


def pend(y, t, ):
    par_x, par_y = y
    loc_eq1 = 0.15 * (1-par_x-par_y) - 0.015 * par_x - 1.05 * par_x * (1-par_x-par_y) ** 2
    loc_eq2 = 0.0032 * (1-par_x-par_y) ** 2 - 0.002 * par_y ** 2
    dydt = [loc_eq1, loc_eq2]
    return dydt


x_bif = bifurcation_array[0][1]
y_bif = bifurcation_array[0][0]
k_bif = bifurcation_array[0][2]


init_y0 = [x_bif, y_bif]
t = np.linspace(0, 3000, 10000)
sol = sci.odeint(pend, init_y0, t)

plt.plot(t, sol[:, 0], 'b', label='x(t)')
plt.plot(t, sol[:, 1], 'g', label='y(t)')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()

x_array = []
y_array = []
for item in sol:
    x_array.append(item[0])
    y_array.append(item[1])


plt.figure("solution with initial bifurcation")
ay = plt.subplot(111)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
ay.plot(x_array, y_array, color='b', label="y(x)")
ay.plot([x_bif], [y_bif], 'ro', color='c', label='bifurcation')
ay.legend()
plt.show()
