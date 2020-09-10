#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:12:19 2020

@author: eugen
"""
import ctl
import subprocess
import yaml
import logging
import datetime

# =============================================================================
# Set up logging for software usage errors
# =============================================================================

# Set logging session ID
logID = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
# Set basic configuration for logging
logging.basicConfig(filename='errlog/cont/'+logID+'.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d-%m-%Y %I:%M:%S')

print("\nProgram started...")

with open('./bin/config.yaml', "r") as f:
    config = yaml.safe_load(f)

# Database service will be started after setting parameters if required    
print("\nDB active: "+ str(config["db_active"]))    

cc = ("\nControl commands:\n"
      "--> 'set' to set the parameters\n"
      "--> 'start' to start the divice\n"
      "--> 'stop' to stop the divice\n"
      "--> 'stats' to view config\n"
      "--> 'mon' to to start session monitor\n"
      "--> 'db' to toggle mongodb service\n"
      "--> 'e' to exit\n")

print(cc)

while True:
    print("\nCommand & Control Center")
    input1 = input("Enter Key: \n")
    
    if input1 == 'e':
        print("\nTerminating program...")
        break
    
    elif input1 == 'help':
        print(cc)
        logID = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Set basic configuration for logging
        logging.basicConfig(filename='errlog/'+logID+'.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d-%m-%Y %I:%M:%S')

    elif input1 == 'mon':
        try:
            subprocess.run(['gnome-terminal', '--', './mon.py'])
        except Exception as e:
            logging.error(e)
            print("Starting monitor failed.")
        # on raspbian the following works:
        # os.system('lxterminal -e ./mon.py &')    
    elif input1 == 'db':
        if config["db_active"] == False:
            config["db_active"] = True
            print("\nDB active: "+ str(config["db_active"]))
        else:
            config["db_active"] = False
            print("\nDB active: "+ str(config["db_active"]))
       
    elif input1 == 'start':
        ctl.start()     
        
    elif input1 == 'stop':
        ctl.stop()
        
    elif input1 == 'set':
        ctl.setParam()
       
    elif input1 == 'stats': 
        ctl.getStats()

    elif input1 == 'stats': 
        ctl.getStats()
       
    else:
        print("\nNot an option, please enter valid option or 'help' to view the commands.\n")
               