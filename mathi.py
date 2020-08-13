#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:01:48 2020

@author: eugen
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import time

# =============================================================================
# Step by step implimentation of flow - 1l = 0.001m³
# =============================================================================
vAZ = .500 # [l] 1l = 1000000 mm³
# vAZ = 0.0006 # [m³] 1l = 1000000 mm³

kPC = 1
tIns = 5

hVc = vAZ/(math.pi*math.pow(0.1/2, 2))

tStp = int(200/8 * hVc)


# Calculated new inspiration time with respect of kPC
dt = round(tIns + tIns*(math.pow(kPC, -1) -1), 4)

# isperation flow    

t = 3
d = round(t + t*(math.pow(kPC, -1) - 1), 2)
k0 = np.arange(0, d+(d/tStp), d/tStp)    


# =============================================================================
# 
# =============================================================================
# Calculated list y of time steps vflr
# y = []
# for i in range(tStp+1):
#     # ispiration time devided amount of steps
#     q = round((dt/tStp)*i, 4)
#     # print(q)
#     vflr = 6*vAZ*((-1/kPC*(pow(dt, (-3)))*pow(q,2)) + ((1/kPC*(pow(dt, -2)))*q)) 
#     y.append(vflr)
   
# # cummulated sum
# y2 = []
# j = 0
# for i in y:
#     j =j+i*(dt/tStp)   
#     y2.append(j)
# sum(y2)

# =============================================================================
# 
# =============================================================================
# Volume flowrate
m = []
for i in k0:
    vflr = 6*vAZ*kPC*((-(1/kPC)*(math.pow(d, (-3)))*math.pow(i,2)) + ((1/kPC*(math.pow(d, -2)))*i)) 
    m.append(vflr)

# Commulated sum of supplied volume
n = []
j=0
for i in m:
    j+=i*(d/tStp)
    n.append(j)

plt.plot(k0, m, "b")
plt.plot(k0, n, "r")
plt.show()

# Vertical movement in [m/s] based on volume supplied
# 1950 micro steps are (0.008/200)*1950 [m] vertical movement    
tStp * (0.008/200)
k = []
kl = 0
for i in m:
    kl = (i*0.001)/((math.pi/4)*math.pow(0.1,2))
    k.append(kl)

# commulated sum of vertical movement
l = []
ln=0
for i in k:
    ln+=i*(d/tStp)
    l.append(ln)
    
plt.plot(k0, k, "b")
plt.plot(k0, l, "r")
plt.show()


# vertical movement in micro steps 

vms = []
for i in k:
    vm = i*(200/0.008)
    vms.append(vm)

lv = []
lh=0
for i in vms:
    lh+=i*(d/tStp)
    lv.append(lh)

hh = []    
for i in vms[1:-1]:
    h = k[1]*i
    hh.append(h)
plt.plot(k0[1:-1], hh, "b")


sum(hh)    
max(lv)


plt.plot(k0, vms, "b")
plt.plot(k0, lv, "r")
plt.show()    
    
# speed based on speed function: v[m/s] = s / t
vi = []
for i in range(len(k0[1:])):
    v = k[1:][i]/k0[1]
    vi.append(v)
plt.plot(k0[1:], vi, "r")

for i in range(len(k0[1:])):
    print(k[1:][i])
   
# time 
tmp = []
for i in vi[1:-1]:
    t = (.008/200)/i
    tmp.append(t)
        

nk = []
jk=0
for i in tmp:
    jk+=i
    nk.append(jk)
sum(tmp)
max(nk)

0.0018/17.5


0.008/200


plt.plot(k, m, "b")
plt.plot(k, l, "r")
plt.plot(k, tmp, "r")
plt.plot(k, nk, "r")
plt.plot(k[1:-1], l, "g")
plt.show()




# Divide by zylinder profile [m²] to get speed at m/s
n = []
for i in k:
    # print(i)
    # q = (dt/tStp)*i
    # print(q)
    vflr = 6*vAZ*kPC*((-(1/kPC)*(math.pow(d, (-3)))*math.pow(i,2)) + ((1/kPC*(math.pow(d, -2)))*i)) 
    sflr = (vflr)/(math.pi*(0.05*0.005))
    n.append(sflr)

# distance divided by speed to get duration in s between the microsteps
tm = []
for i in n[1:-1]:
    t = 0.08/i
    tm.append(t)

sum(tm)

(1100/20)*620/1100
# m1, k1 = func(1)
# m2, k2 = func(.8)

plt.plot(k, m, "b")
plt.plot(k, n, "r")
# plt.plot(k[1:-1], tm, "g")
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
# Implementation of Speed [m/s]
# =============================================================================
t = 5 # in [s]
dia = .1 # in [m] - Diameter of pump = 10cm
z = .008 # in [m]Step of spindle: 8mm
fi = 1.8
kPC = 1
d = t + t*(math.pow(kPC, -1) -1)
vAZ = 0.0005 # in [m³] - 1l = 0.001m³

# Total hight per vent cycle: h[m] = v[m³]/(pi*r[m]²) with 1[ml] = 1000[mm²]
hVc = vAZ/(math.pi*math.pow(dia/2, 2)) *1000
0.1*0.1
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
    nM = t0 * t1
    # nM = (1/.2)*(t0*t1)*z
    nm.append(nM)

sp = []
for i in nm:
    s = (fi/(2*math.pi))*i*z
    sp.append(s)
    
(math.pi/4)*(0.1*0.1)    
math.pi*(0.05*0.05)
# plot
k = np.arange(0, d+(d/tStp), d/tStp)    

plt.plot(k, nm, "b")
plt.plot(k, sp, "r")
plt.plot(k[1:-1], ll, "g")
plt.show()

(0.008/400)/0.02
    
ll= []
for i in sp[4:-4]:
    t =  (z/200)/i
    ll.append(t)

sum(ll)
min(ll)
j=0
for i in ll:
    j+=i

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


# =============================================================================
# Microsteps calculation
# =============================================================================
# Total hight per vent cycle: h[mm] = v[mm³]/(pi*r[mm²]) with 1[ml] = 1000[mm²]
h = int((.35*1000*1000)/(math.pi * math.pow((0.1*1000/2), 2)))
    
# Microsteps per vent cycle: 1mm = 200[mcs]/0.008[m] * h[mm]/1000
mcs2 = int(200/0.002 * h/1000)
mcs1 = int(200/0.008 * h/1000)

tin = 3.5*0.85

p = tin/mcs2
tI0 = time.time()
for i in range(mcs2):
    time.sleep(p)
tI1 = time.time()
dtI = tI1-tI0   

print(dtI) 

(4.85-3.5)/4400
0.035/4400

3 <= 4 


kk = 0
for i in range(tStp):
    kk+=d/tStp

print(kk)

