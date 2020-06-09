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

# =============================================================================
# Device callibration
# =============================================================================

def calibrate():
    
    print('\nCalibrating divice...\n')
    
    with open('./bin/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    if config['status'] != 'stop':
        print('Cannot calibrate running cycle')
        
    else:        
        subprocess.run("./dtp/calSim.py")
        
        config['calibrate'] = True
        
        with open('./bin/config.yaml', 'w') as f:
            yaml.dump(config, f)
        print('Calibration sucessful.')
               
# =============================================================================
# Retrieve parameter set points        
# =============================================================================

def getStats():
   
    with open('./bin/config.yaml') as f:
        config = yaml.safa_load(f)        
        print("Config:")
        
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
    
    with open(r'./bin/config.yaml') as f:
        config = yaml.safe_load(f)
    
    config['status'] = 'stop'
    config['calibrate'] = False
    
    with open('./bin/config.yaml', 'w') as f:
        yaml.dump(config, f)

# =============================================================================
# Check parameters end invoke ventilation process
# =============================================================================

def start():
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    if config['status'] == 'running':
        print("Divice already running.\n"
              "To restart enter 'stop' and recalibrate the device.")
        
    elif config['optSet'] != True:
        print("Please set parameters before starting.")
       
    else:
        # declare variable for subprocesss
        config['status'] = 'running'
        config['session'] = dt.datetime.now()
        # config['optSet'] = False
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
        print("Starting ventilation...")
        
        subprocess.run(['gnome-terminal', '--', './mon.py'])
        
        with open(r'proc.yaml') as f:
            proc = yaml.safe_load(f)
        proc['proc'] = 'yes'
        
        with open('proc.yaml', 'w') as f:
            yaml.dump(proc, f) 
        
        os.system('nohup ./sim.py &')  
               
# =============================================================================
# set configuration parameters
# =============================================================================
""" 
# Compliance [l/Pa] range: 0 - 1.25 +/-15%
Comp: 0

# Inspiration time in [s] range: +/-20%
Tins: 0

# Cycle frequency in rounds per min [rpm] range: 0.05 - 0.15
cFrq: 0

# Pressure limit [Pa]:
pMax: 175

# Volume status [%] - reflecting changes due to pressure reduction:
VolStat: 100

# safty factor: max inspiration time [1]
TiSF: 1.15
"""

def setParam():      

    # 0. Maximum air volume mVAZ based on pump geometry: pi*r²*hmax
    with open('./bin/manSP.yaml') as f:
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
    
    # Load binary and set parameters        
    with open('./bin/param.yaml') as f:
        param = yaml.safe_load(f)
       
    param["mPAT"] = mPAT
    param["VAZ"] = iVAZ
    param["vRst"] = vRst
    param["Tins"] = iTin
    param["Texp"] = iTex
    param["bFrq"] = bFrq
    param["C"] = iCpl
    param["pCrt"] = pCrt
    
    with open('./bin/param.yaml', 'w') as f:
        yaml.dump(param, f)    

    # Derive and set amount of micro steps from volume    
    # Total hight per vent cycle: h[mm] = v/(pi*r²) with 1[ml] = 1000[mm²]
    h = int((iVAZ*1000*1000)/(math.pi * math.pow((geo['dmtP']*1000/2), 2)))
    
    # Microsteps per vent cycle: 1mm = 400[mcs]/8[mm] * h[mm]
    mcs = int(geo['stepsPT']/geo['grad'] * h/1000)
    
    with open('./bin/config.yaml') as f:
        config = yaml.safe_load(f)
        
    config['McS'] = mcs
    config['optSet'] = True
 
    with open('./bin/config.yaml', 'w') as f:
        yaml.dump(config, f)   


    print("\nOptions set.\n")    

    # Device calibration
    # calibrate()

    # print("\nDevice calibrated. Returning....\n")    
