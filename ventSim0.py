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
   
vAZ = config["VAZ"]
tIns = config["Tins"]
tExp = config["Texp"]
tStp = config["McS"]

# =============================================================================
# Function definition
# =============================================================================

# retrive pressure
def getPres():
    with open('./bin/prsIs.yaml', 'r') as f:
        presIs = yaml.safe_load(f)
    return presIs["prsIs"]    

# correction factor 
kPC = 1

# Pressure correction factor
def getkP(pi_1, pi, pCrt):
    return pow(min(pi_1, pCrt * 0.9/pi), 1.5)    

# Complience correction factor
def getkC(vAZ, pImax, pEavr):
    #
    #
    return

# based on correction factor inspiration time is determined by
dtIns = round(tIns + tIns*(pow(kPC, -1) -1), 4)

# the correction of inspiration time shell not be greater than 1.15
if dtIns > tIns*1.15:
    dtIns = (tIns * 1.15)
    

# pause to determine movement speed
# slpIn = dtIns/tStp
slpIn = []
for i in range(tStp):
    j = dtIns/tStp
    slpIn.append(j)

# speed for expiration
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
    
    # micro step count inspiration
    msI = 0
    # inpiration pressure list
    pIc = []
    for i in range(tStp):
        msI += 1
        # retrive and append pressure every 20 microsteps
        if msI % 20 == 0:            
            pI = getPres()
            pIc.append(pI)
            # compare pressure and calculate new kPC if necessary
            if pI > config["pCrt"]*0.9:                
                # if presure is to high wait until it is not that high any more
                while pI > config["pCrt"]*0.9:
                    time.sleep(0.001)
                    pI = getPres()
                
                """ this crashes if len(plc) < 2, but is very unlikely to happen"""
                kPC = getkP(pIc[len(pIc)-2], pIc[len(pIc)-1])                                
                
                # calc new function for speed of movement
                ####
                ####
                
                
        time.sleep(slpIn[i])
        # time.sleep(dtIns/tStp)
        
    tI1 = time.time()
    dtI = tI1-tI0

   
    # start expiration
    print("Expiration...")
    tE0 = time.time()
    # micro step count expriration
    msE = 0
    # expriration pressure list
    pEc = []
    for i in range(tStp):
        msE += 1
        if msE % 20 == 0:
            pI = getPres()
            pEc.append(pI)
            
        time.sleep(slpEx)        
    tE1 = time.time()    
    dtE = tE1-tE0

    # print("Ext Time of last cycle: ", dtE)
        
    # calculate complience correction factor
    kPC = getkC(vAZ, max(pIc), sum(pEc)/len(pEc))
    
    # write actual inspiration & expiration time to proc.yaml
    with open('./bin/proc.yaml', "r") as f:
        proc = yaml.safe_load(f)

    proc['vent_cycle'] = n
    proc['ins_time'] = round(dtI, 4)
    proc['exp_time'] = round(dtE, 4)

    with open('./bin/proc.yaml', 'w') as f:
        yaml.dump(proc, f)