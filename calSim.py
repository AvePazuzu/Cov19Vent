#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:17:22 2020

@author: eugen
"""

import yaml

from time import sleep
    
with open(r'./bin/manSP.yaml') as file:
    manSP = yaml.load(file, Loader=yaml.FullLoader)    
    
# max lenght 
maxL = int(manSP["spL"] / manSP["grad"] * manSP["stepsPT"])

# amount fo steps down for 5mm 
dw = int(5/manSP["wpMS"])
dw

# go up
for i in list(range(maxL)):
    sleep(0.002)
   
# go down   
for j in list(range(dw)):
    sleep(0.003)