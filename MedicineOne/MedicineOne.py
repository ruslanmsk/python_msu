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

# уравнение относительно y для нахождения точек бифрукации
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




def pend(y, t):
    par_y, par_x = y
    loc_eq1  = 0.12 * (1-par_x-par_y) - 0.005 * par_x - 1.05 * par_x * (1-par_x-par_y) ** 2
    loc_eq2 = 0.0032 * (1-par_x-par_y) ** 2 - 0.002 * par_y ** 2
    dydt = [loc_eq1, loc_eq2]
    return dydt


print(bifurcation_array)
x_bif = bifurcation_array[0][1]
y_bif = bifurcation_array[0][0]
k_bif = bifurcation_array[0][2]


init_y0 = [x_bif, y_bif]
t = np.linspace(0, 800, 10000)
sol = sci.odeint(pend, init_y0, t)
print(sol)

plt.plot(t, sol[:, 0], 'b', label='theta(t)')
plt.plot(t, sol[:, 1], 'g', label='omega(t)')
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
plt.ylim((-1200, 600))
plt.xlim((-50, 1500))
plt.xlabel('x')
plt.ylabel('y')
ay.plot(x_array, y_array, color='b')
ay.plot([x_bif], [y_bif], 'ro', color='c')
ay.legend()
plt.show()


# plt.figure("one-parameter analysis")
# ax = plt.subplot(111)
# plt.subplot(111)
# plt.grid(True)
# plt.xlabel('k1')
# plt.ylabel('x, y')
# plt.ylim((0.0, 1.0))
# plt.xlim((0, 0.5))
# ax.plot(k1_array, split_y, color='b', label='y')
# ax.plot(k1_array, x_array, color='r', label='x')
# ax.plot([bifurcation_array[0][2]], [bifurcation_array[0][1]], 'ro', color='c', label='bifurcation')
# ax.plot([bifurcation_array[0][2]], [bifurcation_array[0][0]], 'ro', color='c')
# ax.plot([bifurcation_array[1][2]], [bifurcation_array[1][1]], 'ro', color='c')
# ax.plot([bifurcation_array[1][2]], [bifurcation_array[1][0]], 'ro', color='c')
# plt.legend()
#
# k1_draw_array = []
# k2_draw_array = []
#
# k1_draw_array_ = []
# k2_draw_array_ = []
#
#
# determinant_x_y = determinant.subs(x, res[1][x])
# k1_on_k2_y = sympy.solve(determinant_x_y, k1)
# k2_on_y = sympy.solve(k1_on_k2_y[0] - res[1][k1], k2)
# for i in split_y:
#     local_k2_y = k2_on_y[0].subs(k_1, init_k_1).subs(k3,init_k3).subs(k_3,init_k_3).subs(y,i)
#     local_k1_k2_y = k1_on_k2_y[0].subs(k_1, init_k_1).subs(k3,init_k3).subs(k_3,init_k_3).subs(y,i).subs(k2,local_k2_y)
#     k1_draw_array.append(local_k1_k2_y)
#     k2_draw_array.append(local_k2_y)
#
# plt.figure("two-parameter analysis")
# ay = plt.subplot(111)
# plt.grid(True)
# plt.ylim((0, 4))
# plt.xlim((0, 33))
# plt.xlabel('k2')
# plt.ylabel('k1')
# ay.plot(k2_draw_array, k1_draw_array, color='b')
# ay.legend()
# plt.show()
#
#
