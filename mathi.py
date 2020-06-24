#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:01:48 2020

@author: eugen
"""
import math
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# Step by step implimentation of flow
# =============================================================================
vAZ = .500 # [l] 1l = 1000000 mm³

kPC = 0.9

tIns = 5

tStp = 1000

# Calculated new inspiration time with respect of kPC
dt = round(tIns + tIns*(math.pow(kPC, -1) -1), 4)

# isperation flow    
y = []
for i in range(1, tStp+1):
    # print(i)
    q = (dt/tStp)*i
    # print(q)
    vflr = 6*vAZ*((-1/kPC*(math.pow(dt, (-3)))*math.pow(q,2)) + ((1/kPC*(math.pow(dt, -2)))*q)) 
    y.append(vflr)

t = 3
d = round(t + t*(math.pow(kPC, -1) -1), 2)
k = np.arange(0, d+(d/tStp), d/tStp)    
m = []
for i in k:
    # print(i)
    # q = (dt/tStp)*i
    # print(q)
    vflr = 6*vAZ*kPC*((-(1/kPC)*(math.pow(d, (-3)))*math.pow(i,2)) + ((1/kPC*(math.pow(d, -2)))*i)) 
    m.append(vflr)



# m1, k1 = func(1)
# m2, k2 = func(.8)

plt.plot(k, m, "b")
plt.plot(k, y2, "r")
plt.show()

    
# cummulated sum
y2 = []
j = 0
for i in m:
    j =j+i*(d/tStp)   
    y2.append(j)
max(y2)
# calculate percentage of cummulated sum steps
y2p = []
for i in range(len(y2)):
    if i < (len(y2)-2):
        j = (y2[i+1]-y2[i])/vAZ*d
        # print(j)
        y2p.append(j)

sum(y2p)
we = int((len(y2p)-1)/2)
wee = y2p[we]

g1 = y2p[we:]
g2 = []
# g1[-2]
for i in range(1, len(g1)+1):
    j=g1[-i]
    # print(j)
    g2.append(j)
    
g = g1 + g2
sum(g)

# min(g)
# sum(g)
x1 = list(range(tStp))
x = list(range(tStp))
xx = list(range(3))
# p1 = plt.plot(hh, x)
p2 = plt.plot(x1, g)

plt.figure(1)
plt.plot(x, y, "r")    
plt.plot(x, y2, "b")
plt.plot(x, y2, "b")
plt.show()

# =============================================================================
# Implementation of Speed [mm/s]
# =============================================================================
t = 3
dia = 10 # Diameter of pump = 10cm
z = 8 # Step of spindle: 8mm
fi = 9
d = round(t + t*(math.pow(kPC, -1) -1), 2)
k = np.arange(0, d+(d/tStp), d/tStp)    
m = []
for i in k:
    # print(i)
    # q = (dt/tStp)*i
    # print(q)
    nM = ((48*vAZ)/((math.pow(dia,2)*fi*z)))*kPC*((-(1/kPC)*(math.pow(d, (-3)))*math.pow(i,2)) + ((1/kPC*(math.pow(d, -2)))*i)) 
    m.append(nM)

