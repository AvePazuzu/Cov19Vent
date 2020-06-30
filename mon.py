#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:59:29 2020

@author: eugen
"""

import yaml
import time
import os

# function to check prcess existance by pid
def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

# function ot clear the terminal
clear = lambda: os.system('clear')

while True:

    print("Welcome to the Cov-19 artificial vent experience!\n")
    print("Session Monitor:\n")
    
    with open('./bin/config.yaml', "r") as f:
        config = yaml.safe_load(f)
        
    with open('./bin/proc.yaml', "r") as f:
        proc = yaml.safe_load(f)

    # with open(r'./bin/prsIs.yaml') as file:
    #     pre = yaml.load(file, Loader=yaml.FullLoader)        

    with open('./bin/param.yaml', "r") as f:
        param = yaml.safe_load(f)
         
    # retriev process id and check if process is still alive
    pid = proc['pid']    
    # returns bool
    pids = check_pid(pid)
        
    #cs = config['status']
    se = config['session']   
    cy = proc['vent_cycle']
    ti = proc['ins_time']
    te = proc['exp_time']
    # st = proc['proc']
    # ps = pre['prsIs']
    psT = config['pCrt']
         
    print("Session: ", se)
    print("\nProcess active: ", pids)
    print("\nCycle: ", cy+1)
    print("\nTime of last inspiration: ", ti)
    print("\nTime of last expiration: ", te)
    # print("\nPressure actual: ", ps)
    print("\nPressure setpoint: ", psT)
    print("\nPressure status: Okay")
    
    time.sleep(0.5)
    
    clear()
    