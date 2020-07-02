#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:26:07 2020

@author: eugen
"""

import yaml
import RPi.GPIO as GPIO
import time

def calibrate():
    
    with open(r'config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    if config['status'] != 'stop':
        print('Cannot calibrate running cycle')
        
    else:
        
        print('Calibration started...')
        
        config['calibrate'] = True
        
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
        print('Calibration sucessful.')

def runCal():

    GPIO.setmode(GPIO.BOARD)
    
    # Raspberry Pi Pin-Belegung für TB6600 Treiber
    ENA = 37
    DIR = 35
    PUL = 33
    
    # up
    # DIR_Left = GPIO.HIGH
    # down
    DIR_Right = GPIO.LOW
    
    ENA_Locked = GPIO.LOW
    # ENA_Released = GPIO.HIGH
    
    GPIO.setwarnings(False)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    
    # Motor aktivieren und halten
    GPIO.output(ENA, ENA_Locked)
    
    # Richtungen (hoch und herunter)
    direction = []
    # direction.append(DIR_Left)
    direction.append(DIR_Right)
    
    # Geschwindigkeit
    speed = 5 * 0.0001875
    
    for a in range(1):
    
        # Richtung festlegen
        GPIO.output(DIR, GPIO.LOW)
    
        for i in range(1000):
    
            # Puls modulieren
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(speed)
    
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(speed)
    
    # clear GPIO signals
    GPIO.cleanup()
    		
    # Motor freigeben
    # GPIO.output(ENA, ENA_Released)
    
    return print('Calibration sucessful.')
runCal()
