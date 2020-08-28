#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:12:19 2020

@author: eugen
"""
import ctl
import subprocess

print("\nProgram started...")

cc = ("\nControl commands:\n"
      "--> 'set' to set the parameters\n"
      "--> 'start' to start the divice\n"
      "--> 'stop' to stop the divice\n"
      "--> 'stats' to view config\n"
      "--> 'mon' to to start session monitor\n"
      "--> 'db' to to start mongodb service\n"
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

    elif input1 == 'mon':
        subprocess.run(['gnome-terminal', '--', './mon.py'])
        # on raspbian the following works:
        # os.system('lxterminal -e ./mon.py &')    
    elif input1 == 'db':
        subprocess.run(['gnome-terminal', '--',"mongod", "--dbpath", "/home/eugen/develop/python/Cov19Vent/data/db2"])        
        # on raspbian the following works:
        # os.system('lxterminal -e ./mon.py &')    
       
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
               