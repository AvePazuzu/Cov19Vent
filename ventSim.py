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

# retriev id of process
pid = os.getpid()

# read params from config & prsIs
with open('./bin/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
# Set input parameters
with open('./bin/config.yaml', 'r') as f:
    param = yaml.safe_load(f)

vAZ = param["VAZ"]    
kPC = 1 # Correction factors not included yet
tIns = param["Tins"]
tStp = config["McS"]

# n = ventilation cycle count       
n = 0        
while config['status'] == "running":
    # increase venticaltion cycle count
    n += 1  
    # print(n)

    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # if config['McS'] == 100:
        # print("Exeting after n = ", n)
        # break
        
    # ms = micro steps counter
    ms = 0    
    # print("Down")
    for i in list(range(config['McS'])):
        ms += 1    
        if ms % 100 == 0:
            # print("Ms: ", ms)
            with open('prsIs.yaml', 'r') as f:
                prsIs = yaml.safe_load(f)
            
            if prsIs['prsIs'] >= config['pres']:
                # print("Yes")

                # print('New value: ', ms)
                
                # with open(r'config.yaml') as file:
                #     config = yaml.load(file, Loader=yaml.FullLoader)
                
                config["McS"] = ms   
                
                with open('config.yaml', 'w') as f:
                        yaml.dump(config, f)
                # print("Reseting at: ", ms)
                break
                                                    
        time.sleep(config['inT']/config['McS'])
        # clear()
        
    # print("up")
    for j in list(range(config['McS'])):
    
        time.sleep(config['exT']/config['McS'])
        

    
    with open(r'proc.yaml') as file:
        proc = yaml.load(file, Loader=yaml.FullLoader)
    
    proc['vent_cycle'] = n
    proc['pid'] = pid
    
    with open('proc.yaml', 'w') as f:
        yaml.dump(proc, f)
      