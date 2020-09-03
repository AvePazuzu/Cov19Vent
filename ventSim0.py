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
import datetime
import os
import pymongo
from ctl import pushToDB
from math import pow
from flow import ins_flow, exp_flow
# import RPi.GPIO as GPIO

# =============================================================================
# Setup process and configurations
# =============================================================================
   
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
sID = config["session"]
c = config["c"]

# =============================================================================
# Connect to database
# =============================================================================
try:
    client = pymongo.MongoClient()
    # Initiate database
    db = client.cov19Vent
    # Set collection for the sesstion with the session ID
    col = db.sID
except:
    print("Connecting to database failed.")

# =============================================================================
# Function definition
# =============================================================================

# retrive pressure
def getPres():
    with open('./bin/prsIs.yaml', 'r') as f:
        presIs = yaml.safe_load(f)
    return presIs["prsIs"]    

# correction factor is initiated with 1
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
dtIns = round(tIns + tIns*(kPC**-1 - 1), 4)

# the correction of inspiration time shell not be greater than 1.15
if dtIns > tIns * 1.15:
    dtIns = (tIns * 1.15)
    
# Micro step delay array to determine movement speed 
slpIn = ins_flow() # delays for inspiration
slpEx = exp_flow() # delays for expiration

# Factor to account for computational time; is substracted from delay
cT = 0.00029

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

# =============================================================================
# Initiate ventilation
# =============================================================================

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
        if msI % 50 == 0:            
            tI = datetime.datetime.now()
            pI = getPres()
            pIc.append(pI)
            # compare pressure to 90% of setpoint and calculate new kPC
            # via pressure correction function if necessary
            if pI > config["pCrt"]*0.9:                
                # if presure is to high --> wait 
                while pI > config["pCrt"]*0.9:
                    time.sleep(0.001)
                    pI = getPres()
                
                """ len(pIc) must be > 2 """
                if len(pIc)>2:
                    kPC = getkP(pIc[len(pIc)-2], pIc[len(pIc)-1])                                
                
                # calc new function for speed of movement
                ####
                ####
                
            # Get values to push to database
            rec = {"timestamp": tI,
                   "vent_cycle": n,
                   "step": msI,
                   "pressure": pI,
                   "kPC": kPC}
            
            # Push values to database
            # try:    
            #     col.insert_one(rec).inserted_id
            # except:
            #     print("Pushing record to database failed.")
            
           # pushToDB(col, config["session"], rec)
                                           
        """ Each micro stepp takes ca. 0.0003s of calculation, 
            this time needs to be substracted from the sleeping time 
        """    
        # Puls modeling wiht half of pause
        # GPIO.output(PUL, GPIO.HIGH)
        time.sleep((slpIn[i]-cT)/2)

        # GPIO.output(PUL, GPIO.LOW)
        time.sleep((slpIn[i]-cT)/2)
        
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
        if msE % 50 == 0:
            pE = getPres()
            pEc.append(pE)
            
        # Puls modeling
        # GPIO.output(PUL, GPIO.HIGH)
        time.sleep((slpEx[i]-cT)/2)          

        # GPIO.output(PUL, GPIO.LOW)
        time.sleep((slpEx[i]-cT)/2)                               
    
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