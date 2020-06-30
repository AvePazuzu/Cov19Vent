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
vAZ = 0.0005 # [m³] 1l = 1000000 mm³

kPC = 1
tIns = 5


tStp = 1950

# Calculated new inspiration time with respect of kPC
dt = round(tIns + tIns*(math.pow(kPC, -1) -1), 4)

# isperation flow    

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


(1100/20)*620/1100
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
t = 5
dia = .1 # Diameter of pump = 10cm
z = .008 # Step of spindle: 8mm
fi = 1.8
d = t + t*(math.pow(kPC, -1) -1)

vAZ = 0.0005 # [m³] 1l = 1000000 mm³
# Total hight per vent cycle: h[m] = v[m³]/(pi*r[m]²) with 1[ml] = 1000[mm²]
hVc = vAZ/(math.pi*math.pow(dia/2, 2)) *1000

mst = int(200/8 * hVc)
k = np.arange(0, d+(d/mst), d/mst)    

nm = []
ft0 = []
ft1 = []
for i in k:
    t0 = (48*vAZ)/((dia*dia)*fi*z)
    ft0.append(t0)
    t1 = kPC*((-(1/kPC)*(math.pow(d, (-3)))*math.pow(i,2)) + ((1/kPC*(math.pow(d, -2)))*i))
    ft1.append(t1)
    nM = t0*t1*z
    nm.append(nM)

sum(nm)/1592    
ll=0
for i in range(1,len(nm[:-1])):
    j =  .04/1000/nm[i]
    ll+=j

plt.plot(k, nm, "r")

# test of speed
gg=[]
for i in nm[1:-1]:
    n = 0.04/1000/i
    gg.append(n)
sum(gg) 
plt.plot(k[1:-1], gg, "r")
   

ii = [1,2,4,8]
hh = []
for i in ii: 
    n = 1/i
    hh.append(n)
sum(hh)    
0.04/1000/nm[2500]    
gg[3]


k=[]
for i in range(1,11):
    j = 2*i*(5/10)
    print(j)
    k.append(j)

l=0
for i in k:
    l+=1/i
3/4+.5+2

# =============================================================================
# tri func
# =============================================================================
vAZ = .7
dt = 5
nr = np.arange(0, dt+.1, .1)    

nk = []
for i in nr:
    y = math.pow(vAZ,3)/1.5*(dt/2-abs(dt/2-i))
    nk.append(y)

sum(nk)
plt.plot(nr, nk, "b")


sm = []
d=0
for i in nk:
    d = d+ i
    sm.append(d)

plt.plot(nr, sm, "r")
