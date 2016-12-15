import sympy
import numpy as np
import matplotlib.pyplot as plt

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

# бифрукация
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
k1_y_init = det_y.subs(k2, init_k2).subs(k3,init_k3).subs(k_3,init_k_3).subs(k1,init_k1).subs(k_1, init_k_1)

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
        bifurcation_array.append([i,x_res])
    determinant_last = determinant_current
    trace_array.append(trace_function(x_res, i, k1_res, init_k2, init_k3, init_k_1, init_k_3))
    k1_array.append(k1_res)
    x_array.append(x_res)
print(bifurcation_array)
print(k1_array)

plt.figure(1)
ax = plt.subplot(111)
plt.subplot(111)
plt.grid(True)
plt.xlabel('k1')
plt.ylabel('x, y')
plt.ylim((0.0, 1.0))
plt.xlim((0, 0.5))
ax.plot(k1_array, split_y, color='b', label='y')
ax.plot(k1_array, x_array, color='r', label='x')
plt.legend()
plt.show()

