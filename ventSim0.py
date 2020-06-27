#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 11:13:39 2020

@author: eugen
"""

import yaml
import time
import os
from math import pow

# retriev id of process
pid = os.getpid()

# load config and params
with open('./bin/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
with open('./bin/param.yaml', 'r') as f:
    param = yaml.safe_load(f)

vAZ = param["VAZ"]    
tIns = param["Tins"]
tExp = param["Texp"]
tStp = config["McS"]
kPC = 1   

