#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:01:48 2020

@author: eugen
"""
import math
import matplotlib.pyplot as plt
import numpy as np

vAZ = 0.5

kPC = 0.9

tIns = 5

tStp = 100

# Calculated new inspiration time with respect of kPC
dt = round(tIns + tIns*(math.pow(kPC, -1) -1), 4)

# math.pow((175/180), (3/2))

# isperation flow    
y = []
for i in range(1, tStp+1):
    # print(i)
    q = (dt/tStp)*i
    # print(q)
    vflr = 6*vAZ*((-1/kPC*(math.pow(dt, (-3)))*math.pow(q,2)) + ((1/kPC*(math.pow(dt, -2)))*q)) 
    y.append(vflr)

t = 3
def func(kpc): 
    d = round(t + t*(math.pow(kpc, -1) -1), 2)
    k = np.arange(0, d+(d/tStp), d/tStp)    
    m = []
    for i in k:
        # print(i)
        # q = (dt/tStp)*i
        # print(q)
        vflr = 6*vAZ*kpc*((-(1/kpc)*(math.pow(d, (-3)))*math.pow(i,2)) + ((1/kpc*(math.pow(d, -2)))*i)) 
        m.append(vflr)
    return m, k


m1, k1 = func(1)
m2, k2 = func(.9)

plt.plot(k1, m1, "b")
plt.plot(k2, m2, "b")
plt.show()

    
# cummulated sum
y2 = []
j = 0
for i in y:
    j =j+i*(dt/tStp)   
    y2.append(j)
max(y2)
# calculate percentage of cummulated sum steps
y2p = []
for i in range(len(y2)):
    if i < (len(y2)-2):
        j = (y2[i+1]-y2[i])/vAZ*dt
        # print(j)
        y2p.append(j)

sum(y2p)
we = int((len(y2p)-1)/2)
wee = y2p[we]

g1 = y2p[we:]
g2 = []
# g1[-2]
for i in range(2, len(g1)+1):
    j=g1[-i]
    # print(j)
    g2.append(j)
    
g = g1 + g2
sum(g)

# hh = []
# a = time.time()
# for i in range(tStp-1):
#     j = time.time()
#     hh.append(j)
#     time.sleep(g[i])

# b = time.time()
# c = b-a
# g[1500]
# list(range(tStp))

# round(4.7890234, 3)

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



# p1 = plt.plot(x,y)    


y1=[]
for i in range(51):
    y = -5*i*i+ 3*i
    y1.append(y)
    
p2 = plt.plot(x, y1)    

y2 = []
for i in range(51):
    y = -0.5*(-3/5) + math.sqrt(((3*3)/5/4)-(-i/5))
    y2.append(y)
p2 = plt.plot(x, y2)    
5/3500
