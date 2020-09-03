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
import sympy
import scipy

# x = sympy.Symbol('x')
# k = sympy.solve(x**2 - 4, x)
# l = float(k[0])

# =============================================================================
# Step by step implimentation of flow - 1l = 0.001m³
# =============================================================================
vAZ = .55 # [l] 1l = 1000000 mm³
# vAZ = 0.0006 # [m³] 1l = 1000000 mm³

kPC = 1
# tIns = 5

hVc = vAZ/(math.pi*math.pow(0.1/2, 2))

# tStp = int(200/8 * hVc)
tStp = 100

# Calculated new inspiration time with respect of kPC
# dt = round(tIns + tIns*(math.pow(kPC, -1) -1), 4)

t0 = 5 # = Tins
d = round(t0 + t0*(math.pow(kPC, -1) - 1), 2)
k0 = np.arange(0, d+(d/tStp), d/tStp)    

# =============================================================================
# Quadratic Flow-function
# =============================================================================
# Volume flowrate
m = []
for i in k0:
    vflr = 6*vAZ*kPC*((-(1/kPC)*(d**-3)*i**2) + ((1/kPC*(d**-2))*i)) 
    m.append(vflr)
plt.plot(k0, m, "r")# plot: Quadratic volume flow

# Supplied vol over time: Integrated flow function
mm = []
for i in k0:
    vflr = 6*vAZ*kPC*((1/3)*(-(1/kPC)*(math.pow(d, (-3)))*math.pow(i,3)) + ((1/2)*(1/kPC*(math.pow(d, -2)))*(i*i))) 
    mm.append(vflr)
plt.plot(k0, mm, "b") # plot: Cubic volume supply

# max(mm)

hVc = vAZ/(math.pi*math.pow(0.1/2, 2)) # vertical hight 
stp = int(200/8 * hVc) # amount per steps
vps = (vAZ)/stp # supplied volume per micro step
vsr = np.arange(0, vAZ+vps, vps) # volume range

# Define sympy symbol
x = sympy.Symbol('x')
tI0 = time.time()

# Solve with SymPy
res = []
for i in vsr:
    k = sympy.solve(6*vAZ*kPC*((1/3)*(-(1/kPC)*(d**(-3))*x**3) + ((1/2)*(1/kPC*(math.pow(d, -2)))*(x**2))) - i, x)
    res.append(k)
tI1 = time.time()
dtI = tI1-tI0; print(dtI)


# # solve with numpy.roots
# tI0 = time.time()
# res = []
# for i in vsr:
#     k = np.roots([(6*vAZ*kPC*((1/3)*(-(1/kPC)*(d**(-3))))), ((1/2)*(1/kPC*d**(-2))), 0, -i])
#     res.append(k)
# tI1 = time.time()
# dtI = tI1-tI0; print(dtI)

# Use SymPy method to convert add type to tuple
res0 = []    
for i in res:    
    l = i[1].as_coeff_add()
    m1 = float(l[1][0])
    res0.append(m1)
    res0[0] = 0
plt.plot(vsr, res0, "b") # plot: Cubic time over volume

# Solve with numpy.roots

res1 = np.roots([(6*vAZ*kPC*((1/3)*(-(1/kPC)*(d**(-3))))), ((1/2)*(1/kPC*(math.pow(d, -2)))),0, -.2 ])
res2 = sympy.solve(6*vAZ*kPC*((1/3)*(-(1/kPC)*(d**(-3))*x**3) + ((1/2)*(1/kPC*(math.pow(d, -2)))*(x**2))) -.2, x)
res3 = scipy.optimize.root(6*vAZ*kPC*((1/3)*(-(1/kPC)*(d**(-3))*i[0]**3) + ((1/2)*(1/kPC*(math.pow(d, -2)))*(i[0]**2))) -.2)
res2[1].as_coeff_add()

np.float(res1[1])

jiC = []
ij = 0
for i in range(len(res0)):
    if i > 0:
        ij = res0[i]-res0[i-1]
        jiC.append(ij)  
plt.plot(vsr[:-1], jiC, "r") # Time delta between micro volume steps Cubic

sum(jiC)
min(jiC)

# Test run for microstep activation
tI0 = time.time()
for i in range(stp): 
    time.sleep(jiC[i]-0.00014)
tI1 = time.time()
dtI = tI1-tI0; print(dtI)

# =============================================================================
# Triangle function
# =============================================================================

mh = 0.55 # maximum supplied vol in [l]
mt = 5 # maximum time range

hVc = mh/(math.pi*math.pow(0.1/2, 2))/1000 # vertical hight 
stp = 200/0.008 * hVc # steps
vps = (mh)/stp # supplied volume per micro step
# vps2 = (math.pi*(math.pow(0.05, 2) * 0.04/1000)*1000)


vsr = np.arange(0, mh+vps, vps) # volume

# Determine acceleration for first half of movement   
a = (2*(0.5*mh)) / ((0.5*mt)*(0.5*mt))

stt = 100 # Time steps for plotting
ll = np.arange(0, mt+(mt/stt), mt/stt) # Plotting array

# =============================================================================
# Linear volume flow
# =============================================================================

jj=[]
v = 0
for i in k0:
    if i <=mt*0.5:
        v =a*(i)
    else:
        v = a*((mt-i))
    jj.append(v)
plt.plot(k0, jj, "r") # Plot: Linear volume flow

# =============================================================================
# Integral 2
# =============================================================================
nn = []
n = 0
for i in k0:
    if i <= mt*0.5:
        n = 0.5*a*(i*i)
    else:
        n = -(0.5*a)*(i*i) + (a*mt)*i - mh
    nn.append(n)
plt.plot(k0, nn, "b") # Plot: Quadratic volume supply
# max(nn)    

# =============================================================================
# Sum of velocity * way delta
# =============================================================================
uu = []
h = 0
for i in jj:
    h += i*(mt/stt)
    uu.append(h)
plt.plot(ll, uu, "r")
# max(uu)

# =============================================================================
# p-q formular
# =============================================================================
tI0 = time.time()
xx = []
for j in vsr:
    if j < mh*0.5: 
        x = math.sqrt((j/(0.5*a)))
    else:
        x = -(0.5*(-2*mt)) - math.sqrt((math.pow((2*mt*0.5),2)-((2*(mh+j)))/a))
    xx.append(x)    
plt.plot(vsr, xx, "b")# Plot: Quadratic time over volume
max(xx)
tI1 = time.time()
dtI = tI1-tI0; print(dtI)

ji = []
ij = 0
for i in range(len(xx)):
    if i > 0:
        ij = xx[i]-xx[i-1]
        ji.append(ij)    
plt.plot(vsr[:-1], ji, "r") # Time delta between micro volume steps Quadratic

sum(ji)
min(ji)

# Test run for microstep activation
tI0 = time.time()
for i in range(stp): 

    time.sleep(ji[i]-0.000145)
tI1 = time.time()
dtI = tI1-tI0; print(dtI)

# =============================================================================
# SymPy solution
# =============================================================================

x = sympy.Symbol('x')
k = sympy.solve(-0.5*a*x**2 + a*mt*x - (mh + 0.25), x)
sympy.solve(-0.5*a*x**2 + a*mt*x - (mh + 0.39), x)
sympy.solve(-0.5*a*x**2 + a*x -(mh + 0.3), x)
l = float(k[0])

# =============================================================================
# Plot comparison
# =============================================================================

plt.plot(k0, m, "black")# plot: Quadratic volume flow
plt.plot(k0, jj, "g") # Plot: Linear volume flow

plt.plot(k0, mm, "black") # plot: Cubic volume supply
plt.plot(k0, nn, "g") # Plot: Quadratic volume supply

plt.plot(vsr, res0, "black") # plot: Cubic time over volume
plt.plot(vsr, xx, "g")# Plot: Quadratic time over volume

plt.plot(vsr[:-1], jiC, "black") # Time delta between micro volume steps Cubic
plt.plot(vsr[:-1], ji, "y") # Time delta between micro volume steps Quadratic

# =============================================================================
# Error calculation
# =============================================================================

# Relative average error: Sum of Deltas devided by ammount of values
rae = []
for i in range(len(ji)):
    ras = ji[i] + jiC[i]
    rae.append(ras)
   
sum(rae)/len(rae)*100    

# =============================================================================
# Linear Flow Function
# =============================================================================

t = sympy.solve((-1/27)*x**3+(1/6)*x**2-0.15, x)
ll = t[1].as_coeff_add()
nn = float(ll[1][0])

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
# tStp * (0.008/200)
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
plt.plot(k0, lv, "b")


gg = []
i = 0
while i < len(lv[1:]):
    h = (lv[i+1]-lv[i])
    i += 1
    gg.append(h)
plt.plot(k0[1:], gg, "b")

hh = []    
for i in gg[1:-1]:
    h = k0[1]*(i/(d/tStp))
    hh.append(h)
plt.plot(k0[2:-1], hh, "b")

sum(hh)
len(lv[1:])
    
tI0 = time.time()
for i in range(len(k0[3:])):
    time.sleep(hh[i])
tI1 = time.time()
dtI = tI1-tI0
print(dtI)

hh2 = []
h2 = 0
for i in hh:
    h2+=i*(d/tStp)
    hh2.append(h2)


plt.plot(k0[1:-1], hh2, "r")

sum(hh)
max(hh2)    
k0[1]/(max(vms)*k0[1])


plt.plot(k0, vms, "b")
plt.plot(k0, lv, "r")
plt.show()
    
# =============================================================================
#     
# =============================================================================

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
