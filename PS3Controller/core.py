import pygame
import time
import smbus
import os
import hcsr04
import piconzero as pz
from gpiozero import Button
import I2C_LCD_driver

#_____________________________________________________________________________
#lcd at startup
mylcd = I2C_LCD_driver.lcd() #assign LCD to variable for ease of use

COUNTDOWN = 30
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
pygame.joystick.init()
pad = pygame.joystick.Joystick(0)

#____________________________________________________________________________________
#hardware setup

pz.init() #initiate hardware



pz.setInputConfig(0,0) #right IR sensor is input 0 and digital
pz.setInputConfig(1,0) #left IR sensor is input 1 and digital
pz.setInputConfig(2,0) #right line sensor is input 2 and digital
pz.setInputConfig(3,0) #left line is input 3 and digital

DEVELOPER = Button(22) #assign developer switch to variable
RIGHTIR = pz.readInput(0) #assign right IR to a variable
LEFTIR = pz.readInput(1) #assign left IR to a variable
RIGHTLINE = pz.readInput(2) #assign right line sensor to a variable
LEFTLINE = pz.readInput(3) #assign left line sensor to a variable

hcsr04.init() #initiate hardware
RANGE = hcsr04.getDistance() #assign HC-SR04 range to variable


#initiate pad
pad.init()

#swap these if it turns the wrong way



#____________________________________________________________________________________
#functions for individual tasks

def fineremotecontrol():
    RUN = 1
    mylcd.lcd_display_string("Remote Control F", 1)
    mylcd.lcd_display_string("Select Ends     ", 2)
    time.sleep(2)
    LEFTMOTOR = 1
    RIGHTMOTOR = 0
    while RUN == 1:
        pygame.event.pump()
        x = pad.get_axis(0) 
        y = pad.get_axis(1)
        mylcd.lcd_display_string("X: %f " % x, 1)
        mylcd.lcd_display_string("Y: %f " % y, 2)
        if pad.get_button(0) == 1: #exit program
            RUN = 0
        elif 0.1 >= x >= -0.1 and 0.1 >= y >= -0.1: #stop
            x = abs(x)
            y = abs(y)
            r = 0
            l = 0
            pz.stop()    
        elif 0.1 >= x >= -0.1 and y <= -0.1: #full speed forwards
            x = abs(x)
            y = abs(y)
            r = int(100 * y)
            l = int(100 * y)
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r)
        elif 0.1 >= x >= -0.1 and y >= 0.1: #full speed backwards
            x = abs(x)
            y = abs(y)
            r = int(100 * y)
            l = int(100 * y)
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r) 
        elif x <= -0.1 and 0.1 >= y >= -0.1: #spin right
            x = abs(x)
            y = abs(y)
            r = int(-100 * x)
            l = int(100 * x)
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r)
        elif x >= 0.1 and 0.1 >= y >= -0.1: #spin left
            x = abs(x)
            y = abs(y)
            r = int(100 * x)
            l = int(-100 * x)
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r) 
        elif -0.9 < x < -0.1 and -0.9 < y < -0.1: #turnR - forwards
            x = abs(x)
            y = abs(y)
            r = int(100 * x * (1-y))
            l = int(100 * x)
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r)
        elif 0.9 > x > 0.1 and -0.9 < y < -0.1: #turnL - forwards
            x = abs(x)
            y = abs(y)
            r = int(100 * x)
            l = int(100 * x * (1-y))
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r)
        elif 0.9 > x > 0.1 and 0.1 > y > 0.1: #turnL - backwards
            x = abs(x)
            y = abs(y)
            r = int(-100 * x)
            l = int(-100 * x * (1-y))
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r)
        elif x < -0.1 and y > 0.1: #turnR - backwards
            x = abs(x)
            y = abs(y)
            r = int(-100 * x * (1-y))
            l = int(-100 * x)
            pz.setMotor(LEFTMOTOR,l)
            pz.setMotor(RIGHTMOTOR,r)
        time.sleep(0.1)

def courseremotecontrol():
    SPEEDFR = 60
    SPEEDT = 100
    mylcd.lcd_display_string("Remote Control C", 1)
    mylcd.lcd_display_string("Select Ends     ", 2)
    time.sleep(2)
    RUN = 1
    while RUN == 1:
        pygame.event.pump()
        if pad.get_button(0) == 1: # exit program
            RUN = 0
        elif pad.get_button(4) == 1:
            pz.forward(SPEEDFR)
        elif pad.get_button(6) == 1:
            pz.reverse(SPEEDFR)
        elif pad.get_button(5) == 1:
            pz.spinRight(SPEEDT)
        elif pad.get_button(7) == 1:
            pz.spinLeft(SPEEDT)
        else:
            pz.stop()
        time.sleep(0.1)





#____________________________________________________________________________________
#main loop


#assign buttons
#setup buttons
DUP = pad.get_button(4)
DDOWN = pad.get_button(6)
DRIGHT = pad.get_button(5)
DLEFT = pad.get_button(7) 
CROSS = pad.get_button(14)
CIRCLE = pad.get_button(13)
TRIANGLE = pad.get_button(12)
SQUARE = pad.get_button(15)
R1 = pad.get_button(10)
R2 = pad.get_button(9)
L1 = pad.get_button(11)
L2 = pad.get_button(8)
SELECT = pad.get_button(0)
START = pad.get_button(3)


#Main program
MAINRUN = 1
pz.stop()

#LCD prompt
COUNTDOWN = 9
while COUNTDOWN > 0:
    mylcd.lcd_display_string("Connect         ", 1)
    mylcd.lcd_display_string("Controller %d   " % COUNTDOWN, 2)
    time.sleep(1)
    COUNTDOWN = COUNTDOWN - 1


    
#Main loop - using this for the menu system
while MAINRUN == 1:
    pygame.event.pump()
    mylcd.lcd_display_string("Main Menu", 1)
    mylcd.lcd_display_string("Select Program", 2)
    pz.stop()
    #print("in main loop")
    if DEVELOPER == 1: #check for developer switch activation and if positive kill program
        mylcd.lcd_display_string("Killing         ", 1)
        mylcd.lcd_display_string("Program         ", 2)
        time.sleep(5)
        MAINRUN = 0
    elif pad.get_button(15) == 1: #when square pressed
        fineremotecontrol()
    elif pad.get_button(13) == 1: #when circle pressed
        courseremotecontrol()
    else:
        time.sleep(0.1)
    time.sleep(0.1)

mylcd.lcd_display_string("Program         ", 1)
mylcd.lcd_display_string("Dead            ", 2)

    
