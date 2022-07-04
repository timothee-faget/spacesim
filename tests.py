import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import date

from solver.neuville import interpolation_neuville
from solver.solver import euler_explicit
from objects import Planet, System
from utils import import_system, my_plot_2d

test_neuville = False
test_planet = False
test_system = False
test_utils = False
test_euler_explicit = False

print("Starting Test")

# print(np.empty([2, 1]))
# def test():
#     return [1, 2.1234, 'lol']

# print(test())
# a, b, c = test()
# print(c)

# a = [1, 2, 3, 4, 5, 6]
# print(a[1:-1])
# for a_ in a:
#     print(a_.index())

# def testing(a, b, c, d):
#     print(a)
#     print(b)
#     print(c)
#     print(d)

# ab = ('a', 'b')
# cd = (1, 2)
# testing(*ab, *cd)

def function_test(num, func):
    return func(num)

def test_1(num):
    return 2*num

def test_2(num):
    return 10*num

print(function_test(10, test_1))
print(function_test(10, test_2))

if test_neuville:
    xi = [0, 2.5, 5, 7.5]
    yi = [2, 22.625, 162, 513.875]
    x = 5
    y = interpolation_neuville(xi, yi, x)
    print(y)

if test_planet:
    terre = Planet('Terre', 2e3, (1.23213, -3.45677, 0.00067), (1.23213, -3.45677, 0.00067))
    terre.get_info()
    print(terre.get_y_matrix())

if test_system:
    solarSystem = import_system()
    solarSystem.get_info()
    # print(solarSystem.get_y_matrix())
    print(solarSystem.get_f_matrix())
    print(solarSystem.get_f_matrix().shape)

if test_utils:
    solarSystem = import_system()
    solarSystem.get_info()
    dist = solarSystem.planets[0].get_distance(solarSystem.planets[1])
    print(dist)
    print(solarSystem.planets[2].is_sun)

if test_euler_explicit:
    T = 10
    t = 0
    h = 0.001
    w2 = (2*np.pi)**2
    Y = [1, 0]
    F = [[0, 1],[-w2, 0]]
    tableau_Y = np.array([Y])
    tableau_t = np.array([t])

    while t < T:
        Y = euler_explicit(Y, F, h)
        t += h
        tableau_Y = np.append(tableau_Y, [Y], axis=0)
        tableau_t = np.append(tableau_t, [t])

    my_plot_2d(tableau_t, tableau_Y[:, 0], "Pendulum", [0, T, -5, 5], ['temps', 'y'])
    