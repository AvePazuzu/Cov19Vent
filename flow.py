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

import numpy as np
import math

# Delay array for liniear inpiration flow
def ins_flow(tIns, vAZ, tStp, kPC):
   
    # Calculate inspiration time based on kPC
    dtIns = round(tIns + tIns*(kPC**-1 - 1), 4)
    
    # Set dtIns to a max of 1.15*tIns if necessary
    if dtIns > tIns * 1.15:
        dtIns = (tIns * 1.15)
    
    vps = (vAZ)/tStp # supplied volume per micro step
    vsr = np.arange(0, vAZ+vps, vps) # volume stesp array
    
    # Determine acceleration for first half of movement of inspiration    
    aIns = (2*(0.5*vAZ)) / ((0.5*dtIns)*(0.5*dtIns))
        
    # calculate roots with p-q formular
    rtIns = []
    for j in vsr:
        if j < vAZ*0.5: 
            x = math.sqrt((j/(0.5*aIns)))
        else:
            x = -(0.5*(-2*dtIns)) - math.sqrt((math.pow((2*dtIns*0.5),2)-((2*(vAZ+j)))/aIns))
        rtIns.append(x)    
        
    # Time deltas between volume steps 
    tdIns = []
    for i in range(len(rtIns)):
        if i > 0:
            td = rtIns[i]-rtIns[i-1]
            tdIns.append(td) 
    return tdIns

# Delay array for linear expriartion flow
def exp_flow(tExp, vAZ, tStp):
    
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
    