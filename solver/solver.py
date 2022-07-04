import numpy as np

import solver.neuville as nv

def euler_explicit(Yn, F, h):
    Yn1 = Yn + h * np.dot(F, Yn)
    return Yn1

def point_milieu(Yn, F, h):
    k1 = h * np.dot(F, Yn)
    k2 = h * np.dot(F, Yn+0.5*k1)
    return Yn+k2

def point_milieu_modified(Yn, F, H, m):
    h = H/m
    u = Yn
    v = u + h * np.dot(F, u)
    for i in range(1, m):
        w = u + 2 * h * np.dot(F, v)
        u = v
        v = w
    return 0.5 * (v + u + h * np.dot(F, v))

def bulirsch_old(Yn, F, H, j_max):
    ms = []
    for j in range(j_max):
        ms.append(2*(j+1))
    Yn1s  = []
    hs = []

    for m in ms:
        h = H/m
        u = Yn
        v = u + h * np.dot(F, u) # TO MOD
        for i in range(1, m):
            w = u + 2 * h * np.dot(F, v) # TO MOD
            u = v
            v = w
        hs.append(h)
        Yn1s.append(0.5 * (v + u + h * np.dot(F, v))) # TO MOD
    return nv.interpolation_neuville(hs, Yn1s, 0)

def bulirsch(Yn, system_function, H, j_max):
    ms = []
    for j in range(j_max):
        ms.append(2*(j+1))
    Yn1s  = []
    hs = []

    for m in ms:
        h = H/m
        u = Yn
        v = u + h * system_function(u) # TO MOD
        for i in range(1, m):
            w = u + 2 * h * system_function(v) # TO MOD
            u = v
            v = w
        hs.append(h)
        Yn1s.append(0.5 * (v + u + h * system_function(v))) # TO MOD
    return nv.interpolation_neuville(hs, Yn1s, 0)