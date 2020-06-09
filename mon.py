#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:59:29 2020

@author: eugen
"""

import yaml
import time
import os
import psutil

clear = lambda: os.system('clear')

while True:

    print("Welcome to the Cov-19 artificial vent experience!\n")
    print("Session Monitor:\n")
    
    with open(r'./bin/config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        
    with open(r'./bin/proc.yaml') as file:
        proc = yaml.load(file, Loader=yaml.FullLoader)

    with open(r'./bin/prsIs.yaml') as file:
        pre = yaml.load(file, Loader=yaml.FullLoader)        

    with open(r'./bin/param.yaml') as file:
        param = yaml.load(file, Loader=yaml.FullLoader)   
         
    # retriev process id and check if process is still alive
    pid = proc['pid']    
    # returns bool
    pids = psutil.pid_exists(pid)   
        
    cs = config['status']
    se = config['session']   
    cy = proc['vent_cycle']
    st = proc['proc']
    ps = pre['prsIs']
    psT = param['Pre']
         
    print("Session: ", se)
    print("\nProcess active: ", pids)
    print("\nCycle: ", cy)
    print("\nPressure actual: ", ps)
    print("\nPressure setpoint: ", psT)
    print("\nPressure status: Okay")
   
    time.sleep(0.5)
    
    clear()
    