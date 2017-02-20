import pygame
import time
import smbus
import os
import hcsr04
import piconzero as pz
from gpiozero import Button
import I2C_LCD_driver

#____________________________________________________________________________________
#pygame setup


pygame.joystick.init()
screen = pygame.display.set_mode((100,100))
#pygame.display.set_caption("Hello World")
pad = pygame.joystick.Joystick(0)

#____________________________________________________________________________________
#hardware setup

pz.init() #initiate hardware
mylcd = I2C_LCD_driver.lcd() #assign LCD to variable for ease of use


pz.setInputConfig(0,0) #right IR sensor is input 0 and digital
pz.setInputConfig(1,0) #left IR sensor is input 1 and digital
pz.setInputConfig(2,0) #right line sensor is input 2 and digital
pz.setInputConfig(3,0) #left line is input 3 and digital

DEVELOPER = Button(22) #assign developer switch to variable
DEVELOPER = 0
RIGHTIR = pz.readInput(0) #assign right IR to a variable
LEFTIR = pz.readInput(1) #assign left IR to a variable
RIGHTLINE = pz.readInput(2) #assign right line sensor to a variable
LEFTLINE = pz.readInput(3) #assign left line sensor to a variable

hcsr04.init() #initiate hardware
RANGE = hcsr04.getDistance() #assign HC-SR04 range to variable


#initiate pad
pad.init()

#swap these if it turns the wrong way
LEFTMOTOR = 0
RIGHTMOTOR = 1

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
#___________________________


while True:
    pygame.event.pump()
    print(DUP)
    print(DDOWN)
    print(CIRCLE)
    time.sleep(1)
