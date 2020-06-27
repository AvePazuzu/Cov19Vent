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
# from math import pow

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

# Vent cycle count
n = 0
while config["start"] == True:
    
    n+=1
    print("Breath Cycle: ", n)   
    # Elapsed time during last cycle
    tI0 = time.time()
    print("Inspiration...")
    
    for i in range(tStp):
        time.sleep(tIns/tStp)
    
    tI1 = time.time()
    dtI = tI1-tI0
    print("Ins Time of last cycle: ", dtI)
    
    print("Expiration...")
    tE0 = time.time()
    for i in range(tStp):
        time.sleep(tExp/tStp)
        
    tE1 = time.time()    
    dtE = tE1-tE0

    print("Ext Time of last cycle: ", dtE)