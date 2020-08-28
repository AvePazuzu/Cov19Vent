#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:39:10 2020

@author: eugen
"""

"""
Flow functions linear inpiration and expiration air flow.
Based on the total air volume to be supplied and the initial inspiration
and expiration time the functions retrun an arreay with micro step delays in [s]. 
"""

import yaml
import numpy as np
import math

# Delay array for liniear inpiration flow
def ins_flow():

    # load config and params
    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    vAZ = config["VAZ"] # maximum volume supplied [l]
    tIns = config["Tins"] # insperation time [s]
    tStp = config["McS"] # Micro steps for total volume
    
    vps = (vAZ)/tStp # supplied volume per micro step
    vsr = np.arange(0, vAZ+vps, vps) # volume stesp array
    
    # Determine acceleration for first half of movement of inspiration    
    aIns = (2*(0.5*vAZ)) / ((0.5*tIns)*(0.5*tIns))
        
    # calculate roots with p-q formular
    rtIns = []
    for j in vsr:
        if j < vAZ*0.5: 
            x = math.sqrt((j/(0.5*aIns)))
        else:
            x = -(0.5*(-2*tIns)) - math.sqrt((math.pow((2*tIns*0.5),2)-((2*(vAZ+j)))/aIns))
        rtIns.append(x)    
        
    # Time deltas between volume steps 
    tdIns = []
    for i in range(len(rtIns)):
        if i > 0:
            td = rtIns[i]-rtIns[i-1]
            tdIns.append(td) 
    return tdIns

# Delay array for linear expriartion flow
def exp_flow():
    
    # load config and params
    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    vAZ = config["VAZ"] # maximum volume supplied [l]
    tExp = config["Texp"] # insperation time [s]
    tStp = config["McS"] # Micro steps for total volume
    
    vps = (vAZ)/tStp # supplied volume per micro step
    vsr = np.arange(0, vAZ+vps, vps) # volume stesp array
    
    # Determine acceleration for first half of movement of expiration   
    aExp = (2*(0.5*vAZ)) / ((0.5*tExp)*(0.5*tExp))
    
    # calculate roots with p-q formular
    rtIns = []
    for i in vsr:
        if i < vAZ*0.5: 
            y = math.sqrt((i/(0.5*aExp)))
        else:
            y = -(0.5*(-2*tExp)) - math.sqrt((math.pow((2*tExp*0.5),2)-((2*(vAZ+i)))/aExp))
        rtIns.append(y)    
        
    # Time deltas between volume steps 
    tdExp = []
    for i in range(len(rtIns)):
        if i > 0:
            td = rtIns[i]-rtIns[i-1]
            tdExp.append(td) 
    return tdExp
    
    
# delays1 = exp_flow()
# sum(delays1)
# delays2= ins_flow()

# # Test run for microstep activation
# tI0 = time.time()
# for i in range(tStp): 

#     time.sleep(tdIns[i]-0.00018)
# tI1 = time.time()
# dtI = tI1-tI0; print(dtI)



# def exp_flow(vol, tIns):
#     delay = []
#     return delay

# tExp = config["Texp"] # expiration time [s]