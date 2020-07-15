#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:23:57 2020

@author: eugen
"""

# =============================================================================
# Module to store major controll functions
# =============================================================================

import yaml
import subprocess
import datetime as dt
import os
import math
# from time import sleep
# import RPi.GPIO as GPIO
               
# =============================================================================
# Retrieve parameter set points        
# =============================================================================

def getStats():
    
    with open('./bin/config.yaml') as f:
        config = yaml.safe_load(f)        
        print("\nConfig:")
        
        for key in config:
            print(key,": ",config[key])
            
        print()
        
    with open('./bin/proc.yaml') as f:
        proc = yaml.safe_load(f)            
        print("Proc:")
        print(proc)
        
# =============================================================================
# Stop current ventilation session        
# =============================================================================

def stop():
    
    print('Stopping ventilation...')
    
    with open('./bin/config.yaml', "r") as f:
        config = yaml.safe_load(f)
    
    config['start'] = False
    config['optSet'] = False
    
    with open('./bin/config.yaml', 'w') as f:
        yaml.dump(config, f)

# =============================================================================
# Check parameters end invoke ventilation process
# =============================================================================

def start():
    # clear previous session in proc.yaml
    
    with open('./bin/proc.yaml', "r") as f:
        proc = yaml.safe_load(f)
    
    proc['exp_time'] = 0
    proc['ins_time'] = 0
    proc['pid'] = 0
    proc['vent_cycle'] = 0
    
    with open('./bin/proc.yaml', 'w') as f:
        yaml.dump(proc, f) 
    
    with open('./bin/config.yaml', "r") as f:
        config = yaml.safe_load(f)

    # if config['status'] == 'running':
    #     print("Divice already running.\n"
    #           "To restart enter 'stop' and recalibrate the device.")
        
    if config['optSet'] != True:
        print("Please set parameters before starting.")
       
    else:
        # declare variable for subprocesss
        # config['status'] = 'running'
        config["start"] = True
        config['session'] = dt.datetime.now()
        # config['optSet'] = False
        with open('./bin/config.yaml', 'w') as f:
            yaml.dump(config, f)
        print("Starting ventilation...")
        
        subprocess.run(['gnome-terminal', '--', './mon.py'])
        # on raspbian the following works:
        # os.system('lxterminal -e ./mon.py &') 
        
        os.system('nohup ./ventSim0.py &') 
        
        print("Start successful. Returning to Command & Control Center...")
                       
# =============================================================================
# set configuration parameters
# =============================================================================
""" 
# Volume status [%] - reflecting changes due to pressure reduction:
VolStat: 100

# safty factor: max inspiration time [1]
TiSF: 1.15
"""

def setParam():      

    # 0. Maximum air volume mVAZ based on pump geometry: pi*r²*hmax
    with open('./bin/manSP.yaml', "r") as f:
        geo = yaml.safe_load(f)
    
    mVAZ = round(math.pi*(geo["dmtP"]/2)**2*geo["spL"]*1000, 2)
    # Calculated maximum patient mass based on maximum air volume & 1.15 factor
    mPaM = int(mVAZ/0.006/1.15)   
    
    # 1. Mass of patient [kg] range: 20 - mPaM
    phr1 = "\nPlease enter mass of patient (20-"+str(mPaM)+"[kg]): "        
    while True:       
        try: 
            mPAT = float(input(phr1))
        except ValueError: 
            print("Entered value is not valid.")
            continue                   
        if mPAT < 20 or mPAT > 200:
            print("Mass of patient out of bound.")            
        else:
            # Write to param here
            print("Mass of pation set to:", str(mPAT) + "[kg]")
            break
                 
    # 2. Tidal volume iVAZ [l] range: +/-15% of calculated value        
    # calculated tidle volume 
    cVAZ = 0.006 * mPAT
    cVAZmin, cVAZmax  = round((cVAZ*(1-0.15)), 2),round((cVAZ*(1+0.15)), 2)
    # input tidle volume
    phr2 = "\nPlease enter air vlolume "+"("+str(cVAZmin)+"-"+str(cVAZmax)+"[l])"+": "
    while True:       
        try: 
            iVAZ = float(input(phr2))
        except ValueError: 
            print("Entered value is not valid.")
            continue                    
        if iVAZ < cVAZmin or iVAZ > cVAZmax:
            print("Air volume out of bound for patient mass.")            
        else:
            # write to param.yaml here
            print("Air volume set to:", str(iVAZ) + "[l]")
            break    
    
    # 3. Volume flowrate at rest [l/s]
    phr3 = "\nPlease air flowrate (0.05-0.15[l/s]): "
    while True:
        try: 
            vRst = float(input(phr3))
        except ValueError: 
            print("Entered value is not valid.")
            continue                   
        if vRst < 0.05 or vRst > 0.15:
            print("Volume flworate out of bound.")            
        else:
            # Write to param here
            print("Volume flworate set to:", str(vRst) + "[l/s]")
            break    
        
    # 4. Inspiration time as iVAZ/vRest in [s] range: +/-20%
    # Calculated inspiration time values
    cTin = iVAZ / vRst
    cTinmin, cTinmax = round((cTin*(1-0.2)), 2),round((cTin*(1+0.2)), 2)
    # Input inspiration time value
    phr4 = "\nPlease enter inspiration Time "+"("+str(cTinmin)+"-"+str(cTinmax)+"[s])"+": "
    while True:
        try:
            iTin = float(input(phr4))
        except ValueError: 
            print("Entered value is not valid.")
            continue 
        if iTin < cTinmin or iTin > cTinmax:
            print("Inspiration time out of bound.")
        else:
            # write to param
            print("Inspiration time set to:", str(iTin)+ "[s]")
            break
        
    # 5. Expiration time
    # Calculated in a range of 1-2 times fo inspiration time
    cTexmin, cTexmax = iTin, iTin * 2
    phr5 = "\nPlease enter expiration time "+"("+str(cTexmin)+"-"+str(cTexmax)+"[s])"+": "
    while True:
        try:
            iTex = float(input(phr5))
        except ValueError:
            print("Entered value is not valid.")
            continue 
        if iTin < cTexmin or iTin > cTexmax:
            print("Expiration time out of bound.")
        else:
            # write to param
            print("Expiration time set to:", str(iTex)+ "[s]")
            break
    
    # 6. Breath frequency
    # Calculated per minute and based on iTin & iTex [1/min]
    bFrq = round(60 / (iTin + iTex), 2) 
    print("Breath frequency is:", str(bFrq)+ "[1/min]")
    
    # 7. Complience
    # Mean value complience [l/pa]
    mCpl = 1.25
    mCplmin, mCplmax = round(mCpl*(1-0.15), 2), round(mCpl*(1+0.15), 2)
    phr7 = "\nPlease enter compliance "+"("+str(mCplmin)+"-"+str(mCplmax)+"[l/Pa]"+": "
    while True:
        try:
            iCpl = float(input(phr7))
        except:
            print("Entered value is not valid.")
            continue                   
        if  iCpl < mCplmin or iCpl > mCplmax:
            print("Complience out of bound.")            
        else:
            # Write to param here
            print("Complience set to:", str(iCpl) + "[l/Pa]")
            break
                   
    # 8. Maximum airway pressure
    phr8 = "\nPlease enter maximum airway pressure (max 175[Pa]): "        
    while True:       
        try: 
            pCrt = float(input(phr8))
        except ValueError: 
            print("Entered value is not valid.")
            continue                   
        if  pCrt > 175:
            print("Maximum airway pressure to high.")            
        else:
            # Write to param here
            print("Maximum airway pressure set to:", str(pCrt) + "[Pa]")
            break
    
    # 9. Modification time stamp
    tmps = dt.datetime.now()
    print("\nModification time stamp: " + str(tmps))
    
    # Load binary and set parameters        
    with open('./bin/param.yaml', "r") as f:
        param = yaml.safe_load(f)
       
    param["mPAT"] = mPAT
    param["VAZ"] = iVAZ
    param["vRst"] = vRst
    param["Tins"] = iTin
    param["Texp"] = iTex
    param["bFrq"] = bFrq
    param["C"] = iCpl
    param["pCrt"] = pCrt
    param["tmps"] = tmps
    
    with open('./bin/param.yaml', 'w') as f:
        yaml.dump(param, f)    

    # Derive and set amount of micro steps from volume    
    # Total hight per vent cycle: h[mm] = v[mm³]/(pi*r[mm²]) with 1[ml] = 1000[mm²]
    h = int((iVAZ*1000*1000)/(math.pi * math.pow((geo['dmtP']*1000/2), 2)))
    
    # Microsteps per vent cycle: 1mm = 200[mcs]/0.008[m] * h[mm]/1000
    mcs = int(geo['stepsPT']/geo['grad'] * h/1000)
    
    with open('./bin/config.yaml') as f:
        config = yaml.safe_load(f)
           
    config['VAZ'] = iVAZ
    config['Tins'] = iTin
    config['Texp'] = iTex
    config['bFrq'] = bFrq
    config['c'] = iCpl
    config['c'] = iCpl
    config['pCrt'] = pCrt
    config['McS'] = mcs
    config['optSet'] = True
 
    with open('./bin/config.yaml', 'w') as f:
        yaml.dump(config, f)   
        
    print("\nOptions set.\n")    

    # Device calibration
    # calibrate() 

# =============================================================================
# Calibration is performed after parameter setting and performs 110% of upward 
# and two total turns of downward movement
# =============================================================================

# def calibrate():
    
#     print('\nCalibrating divice...\n')
    
#     # GPIO setup
#     GPIO.setmode(GPIO.BOARD)
    
#     # Raspberry Pi pin set for TB6600 driver
#     ENA = 37
#     DIR = 35
#     PUL = 33
    
#     # set upward movement 
#     #up = GPIO.HIGH
#     # set down ward movemnt 
#     #down = GPIO.LOW
    
#     ENA_Locked = GPIO.LOW
#     # ENA_Released = GPIO.HIGH
    
#     GPIO.setwarnings(False)
#     GPIO.setup(DIR, GPIO.OUT)
#     GPIO.setup(PUL, GPIO.OUT)
#     GPIO.setup(ENA, GPIO.OUT)
    
#     # activate and hold motor
#     GPIO.output(ENA, ENA_Locked)
            
#     # set upward movement
#     GPIO.output(DIR, GPIO.HIGH)
    
#     # load and calculate microsteps for upward movement
#     with open('./bin/config.yaml', 'r') as f:
#         config = yaml.safe_load(f)
    
#     mcsCal = int(config["McS"] * 1.10)    
#     for i in range(mcsCal):

#         # Puls modeling
#         GPIO.output(PUL, GPIO.HIGH)
#         sleep(0.001)

#         GPIO.output(PUL, GPIO.LOW)
#         sleep(0.001)
    
#     # set downward movement
#     GPIO.output(DIR, GPIO.LOW)
    
#     # load and calculate microsteps steps of two total turns: ttTu
#     with open('./bin/manSP.yaml', 'r') as f:
#         manSP = yaml.safe_load(f)
    
#     ttTu = manSP["stepsPT"] * 2
#     for i in range(ttTu):
        
#         # Puls modeling
#         GPIO.output(PUL, GPIO.HIGH)
#         sleep(0.001)

#         GPIO.output(PUL, GPIO.LOW)
#         sleep(0.001)
        
#     # clear GPIO signals
#     GPIO.cleanup()
    		
#     # Release motor
#     # GPIO.output(ENA, ENA_Released)
    
#     return print("\nCalibration sucessful. Returning to Control Center...\n")