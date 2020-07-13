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
# import RPi.GPIO as GPIO
   
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
c = config["c"]

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
    # complience based on the last breathing cycle
    cB_1 = vAZ/(pImax-pEavr)
    if cB_1 >= c:
        kC = c/cB_1
    else:
        kC = cB_1/c
    return kC

# based on correction factor inspiration time is determined by
dtIns = round(tIns + tIns*(pow(kPC, -1) -1), 4)

# the correction of inspiration time shell not be greater than 1.15
if dtIns > tIns*1.15:
    dtIns = (tIns * 1.15)
    

# pause to determine movement speed
# slpIn = dtIns/tStp
slpIn = []
for i in range(tStp):
    j = (dtIns-0.00027*tStp)/tStp
    slpIn.append(j)

# speed for expiration
slpEx = (tExp-0.00027*tStp)/tStp

# =============================================================================
# Set up GPIO
# =============================================================================
"""
# GPIO setup
GPIO.setmode(GPIO.BOARD)

# Raspberry Pi pin set for TB6600 driver
ENA = 37
DIR = 35
PUL = 33

# set upward movement 
#up = GPIO.HIGH
# set down ward movemnt 
#down = GPIO.LOW

ENA_Locked = GPIO.LOW
# ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# activate and hold motor
GPIO.output(ENA, ENA_Locked)
"""
# Vent cycle count
n = 0
while config["start"] == True:
    
    # load config to check for status updates
    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # set GPIO for downward movement
    # GPIO.output(DIR, GPIO.LOW)
    
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
            # compare pressure to 90% of setpoint and calculate new kPC
            # via pressure correction function if necessary
            if pI > config["pCrt"]*0.9:                
                # if presure is to high wait 
                while pI > config["pCrt"]*0.9:
                    time.sleep(0.001)
                    pI = getPres()
                
                """ this crashes if len(plc) < 2, but is very unlikely to happen"""
                kPC = getkP(pIc[len(pIc)-2], pIc[len(pIc)-1])                                
                
                # calc new function for speed of movement
                ####
                ####                
                
        """ Each micro stepp takes ca. 0.0003s of calculation 
            this needs to be substracted from the sleeping time 
        """    
        # Puls modeling wiht half of pause
        # GPIO.output(PUL, GPIO.HIGH)
        time.sleep(slpIn[i]/2)
        # time.sleep(0)

        # GPIO.output(PUL, GPIO.LOW)
        time.sleep(slpIn[i]/2)
        # time.sleep(0)
        
        # time.sleep(slpIn[i])
        # time.sleep(dtIns/tStp)
        
    tI1 = time.time()
    dtI = tI1-tI0
   
    print("Ins Time of last cycle: ", dtI)
    
    # set GPIO for upward movement
    # GPIO.output(DIR, GPIO.HIGH)
   
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
            
        # Puls modeling
        # GPIO.output(PUL, GPIO.HIGH)
        time.sleep(slpEx/2)
        # time.sleep(0)            

        # GPIO.output(PUL, GPIO.LOW)
        time.sleep(slpEx/2)            
        # time.sleep(0)            
    
    tE1 = time.time()    
    dtE = tE1-tE0

    print("Ext Time of last cycle: ", dtE)
        
    # calculate complience correction factor
    # kPC = getkC(vAZ, max(pIc), sum(pEc)/len(pEc))
    
    # write actual inspiration & expiration time of last cycle to proc.yaml
    with open('./bin/proc.yaml', "r") as f:
        proc = yaml.safe_load(f)

    proc['vent_cycle'] = n
    proc['ins_time'] = round(dtI, 4)
    proc['exp_time'] = round(dtE, 4)

    with open('./bin/proc.yaml', 'w') as f:
        yaml.dump(proc, f)