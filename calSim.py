#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:17:22 2020

@author: eugen
"""

import yaml
from time import sleep
  
# =============================================================================
# Calibration is performed after parameter setting and performs 110% upward 
# and one total turn downward movement
# =============================================================================
print("Calibration started...")
# Loding of manufacturing parameters  
with open('./bin/manSP.yaml', 'r') as f:
    manSP = yaml.safe_load(f)    

# load steps per total turn for downward movement
stepsPT = manSP["stepsPT"]

# Loding of configuration parameters  
with open('./bin/config.yaml', 'r') as f:
    config = yaml.safe_load(f)    

# Calculation of microsteps for upward movement
msCal = int(config["McS"] * 1.10)

# Upward movement
print("moving up")
for i in range(msCal):
    sleep(0.003)

# Downward movement
print("moving down")    
for i in range(stepsPT):
    sleep(0.003)
    
print("\nCalibration finished. Returning to Control Center...\n")    