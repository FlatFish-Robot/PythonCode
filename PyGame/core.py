import pygame
import sys
from pygame.locals import *
import time
import smbus
import os
import hcsr04
import piconzero as pz
from gpiozero import Button
import I2C_LCD_driver

#I2C LCD driver from http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

#kill if developer active
MAINRUN = 1
DEVELOPER = Button(22) #assign developer switch to variable
if DEVELOPER == 1:
    sys.exit(0)


#_____________________________________________________________________________
#lcd at startup
mylcd = I2C_LCD_driver.lcd() #assign LCD to variable for ease of use

COUNTDOWN = 10
while COUNTDOWN > 0:
    mylcd.lcd_display_string("Starting up.... ", 1)
    mylcd.lcd_display_string("       T - %d   " % COUNTDOWN, 2)
    time.sleep(1)
    COUNTDOWN = COUNTDOWN - 1
mylcd.lcd_display_string("Script on       ", 1)
mylcd.lcd_display_string("                ", 2)



#____________________________________________________________________________________
#pygame setup

pygame.init()
screen = pygame.display.set_mode((100,100))
pygame.display.set_caption("Hello World")

#____________________________________________________________________________________
#hardware setup

pz.init() #initiate hardware

pz.setInputConfig(0,0) #right IR sensor is input 0 and digital
pz.setInputConfig(1,0) #left IR sensor is input 1 and digital
pz.setInputConfig(2,0) #right line sensor is input 2 and digital
pz.setInputConfig(3,0) #left line is input 3 and digital


RIGHTIR = pz.readInput(0) #assign right IR to a variable
LEFTIR = pz.readInput(1) #assign left IR to a variable
RIGHTLINE = pz.readInput(2) #assign right line sensor to a variable
LEFTLINE = pz.readInput(3) #assign left line sensor to a variable

hcsr04.init() #initiate hardware
RANGE = hcsr04.getDistance() #assign HC-SR04 range to variable

#____________________________________________________________________________________
#functions for individual tasks


def remotecontrolf():
    SPEEDFR = 50
    SPEEDT = 100
    mylcd.lcd_display_string("Remote Control F", 1)
    mylcd.lcd_display_string("Press 1 to End  ", 2)
    time.sleep(2)
    RUN = 1
    while RUN == 1:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESC]: # exit program
            RUN = 0
        if keys[K_UP]:
            pz.forward(SPEEDFR)
        if keys[K_DOWN]:
            pz.reverse(SPEEDFR)
        if keys[K_RIGHT]:
            pz.spinRight(SPEEDT)
        if keys[K_LEFT]:
            pz.spinLeft(SPEEDT)
        if keys[K_SPACE]:
            pz.stop()

def remotecontrols():
    SPEEDFR = 50
    SPEEDT = 45
    mylcd.lcd_display_string("Remote Control S", 1)
    mylcd.lcd_display_string("Press 1 to End  ", 2)
    time.sleep(2)
    RUN = 1
    while RUN == 1:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESC]: # exit program
            RUN = 0
        if keys[K_UP]:
            pz.forward(SPEEDFR)
        if keys[K_DOWN]:
            pz.reverse(SPEEDFR)
        if keys[K_RIGHT]:
            pz.spinRight(SPEEDT)
        if keys[K_LEFT]:
            pz.spinLeft(SPEEDT)
        if keys[K_SPACE]:
            pz.stop()
       





#____________________________________________________________________________________
#main loop

#Main program

pz.stop()

    
#Main loop - using this for the menu system
while MAINRUN == 1:
    mylcd.lcd_display_string("Main Menu       ", 1)
    mylcd.lcd_display_string("Select Program  ", 2)
    pz.stop()
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    #print("in main loop")
    if DEVELOPER == 1: 
        mylcd.lcd_display_string("Killing         ", 1)
        mylcd.lcd_display_string("Program         ", 2)
        time.sleep(5)
        MAINRUN = 0
    elif keys[K_1]: #when one pressed
        remotecontrolf()
    elif keys[K_2]: #when one pressed
        remotecontrols()
    else:
        time.sleep(0.1)

mylcd.lcd_display_string("Program         ", 1)
mylcd.lcd_display_string("Dead            ", 2)
time.sleep(2)
pz.stop()
pz.cleanup()
mylcd.lcd_clear()

    
