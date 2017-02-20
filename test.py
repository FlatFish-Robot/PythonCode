#core script to run at startup for flatfish robot
#from triangula.input import SixAxis, SixAxisResource
import time
#import smbus
#import os
#import hcsr04
import piconzero as pz
#from gpiozero import Button
#import I2C_LCD_driver

#__________________________________________________________________
#initiate piconzero and display

pz.init() #initiate hardware
pz.forward(100)
time.sleep(5)
pz.stop()
