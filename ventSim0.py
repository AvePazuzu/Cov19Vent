#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 11:13:39 2020

@author: eugen
"""
# =============================================================================
# Linear movement
# =============================================================================

import yaml
import time
import os
from math import pow

# retrieve and save id of process to proc
pid = os.getpid()
with open('./bin/proc.yaml', 'r') as f:
    proc = yaml.safe_load(f)

proc["pid"] = pid

with open('./bin/proc.yaml', 'w') as f:
    yaml.dump(proc, f) 
  

# load config and params
with open('./bin/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
   
tIns = config["Tins"]
tExp = config["Texp"]
tStp = config["McS"]

# correction factor 
kPC = .7

# based on correction factor inspiration time is determined by
dtIns = round(tIns + tIns*(pow(kPC, -1) -1), 4)

# the correction of inspiration time shell not be greater than 1.15
if dtIns > tIns*1.15:
    dtIns = tIns * 1.15
    

# pause to determine movement speed
slpIn = dtIns/tStp
slpEx = tExp/tStp

# Vent cycle count
n = 0
while config["start"] == True:
    
    # load config to check for status updates
    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # start inspiration
    n+=1
    print("Breath Cycle: ", n)   
    # Elapsed time during last cycle
    tI0 = time.time()
    print("Inspiration...")
    
    # micro step count
    ms = 0
    for i in range(tStp):
        ms += 1
        time.sleep(slpIn)
        
    tI1 = time.time()
    dtI = tI1-tI0
    print("Microsteps: ", ms)
    print("Ins Time of last cycle: ", dtI)
    
    # write actual expiration time to proc.yaml
    with open('./bin/proc.yaml', "r") as f:
        proc = yaml.safe_load(f)

    proc['vent_cycle'] = n
    proc['exp_time'] = round(dtI, 4)

    with open('./bin/proc.yaml', 'w') as f:
        yaml.dump(proc, f)
    
    
    # start expiration
    print("Expiration...")
    tE0 = time.time()
    for i in range(tStp):
        time.sleep(slpEx)
        
    tE1 = time.time()    
    dtE = tE1-tE0

    print("Ext Time of last cycle: ", dtE)
        
