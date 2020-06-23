#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:18:06 2020

@author: eugen
"""

# =============================================================================
# Module for simulation of GPIO controlled RasPi
# =============================================================================

import yaml
import time
import os
from math import pow

# retriev id of process
pid = os.getpid()

# read params from config & prsIs
with open('./bin/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
# Set input parameters
with open('./bin/param.yaml', 'r') as f:
    param = yaml.safe_load(f)

vAZ = param["VAZ"]    
tIns = param["Tins"]
tStp = config["McS"]
kPC = 1

# Calculated new inspiration time with respect of kPC
dt = round(tIns + tIns*(pow(kPC, -1) -1), 4)

# Calculated list y of time steps vflr
y = []
for i in range(tStp+1):
    # ispiration time devided amount of steps
    q = round((dt/tStp)*i, 4)
    # print(q)
    vflr = 6*vAZ*((-1/kPC*(pow(dt, (-3)))*pow(q,2)) + ((1/kPC*(pow(dt, -2)))*q)) 
    y.append(vflr)
   
# cummulated sum
y2 = []
j = 0
for i in y:
    j =j+i*(dt/tStp)   
    y2.append(j)
sum(y2)
# calculate percentage of cummulated sum steps
y2p = []
for i in range(len(y2)):
    if i < (len(y2)-2):
        j = (y2[i+1]-y2[i])/vAZ*dt
        y2p.append(j)

# calculate list g of sleep lenght         
we = int((len(y2p)-1)/2)
# wee = y2p[we]

g1 = y2p[we:]
g2 = []
# g1[-2]
for i in range(2, len(g1)+1):
    j=g1[-i]
    # print(j)
    g2.append(j)
    
g = g1 + g2        
sum(g)#- g[759]
len(g)
# n = ventilation cycle count       
n = 0        
while config['status'] == "running":
    # increase venticaltion cycle count
    n += 1  
    print(n)

    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # if config['McS'] == 100:
        # print("Exeting after n = ", n)
        # break
        
    # ms = micro steps counter
    # ms = 0    
    print("Inspiration Started")
    a = time.time()
    for i in list(range(config['McS'])):
    #     ms += 1    
    #     if ms % 100 == 0:
    #         # print("Ms: ", ms)
    #         with open('prsIs.yaml', 'r') as f:
    #             prsIs = yaml.safe_load(f)
            
    #         if prsIs['prsIs'] >= config['pres']:
    #             # print("Yes")

    #             # print('New value: ', ms)
                
    #             # with open(r'config.yaml') as file:
    #             #     config = yaml.load(file, Loader=yaml.FullLoader)
                
    #             config["McS"] = ms   
                
    #             with open('config.yaml', 'w') as f:
    #                     yaml.dump(config, f)
    #             # print("Reseting at: ", ms)
    #             break
        time.sleep(g[i])
    b = time.time()
    print(g[i])
    c = (b-a) - g[i] 
    print("ins time: ", c)                                              

        # clear()
    print("Ins finished")
        
    # print("up")
    for j in list(range(config['McS'])):
    
        time.sleep(config['exT']/config['McS'])
    
    with open(r'proc.yaml') as file:
        proc = yaml.load(file, Loader=yaml.FullLoader)
    
    proc['vent_cycle'] = n
    proc['pid'] = pid
    
    with open('proc.yaml', 'w') as f:
        yaml.dump(proc, f)
      