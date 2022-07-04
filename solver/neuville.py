import numpy as np

def interpolation_neuville(xi, yi, x):
    N = len(xi)
    return recur(xi, yi, x, 0, N-1)

def recur(xi, yi, x, i, m):
    if m == 0:
        return yi[i]
    else:
        return ((x-xi[i+m])*recur(xi, yi, x, i, m-1) + (xi[i]-x)*recur(xi, yi, x, i+1, m-1))/(xi[i]-xi[i+m])



