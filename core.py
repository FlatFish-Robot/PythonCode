#code for flatfish Mark 6
import piconzero as pz
import time
import sys
from inputs import get_key
import os
import hcsr04
import I2C_LCD_driver
#I2C LCD driver from http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/



#____________________________________________________________________________________
#hardware setup

mylcd = I2C_LCD_driver.lcd() #assign LCD to variable for ease of use

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

#end of hardware setup
#______________________________________________________________________________


#____________________________________________________________________________________
#functions for individual tasks


def remotecontrol():
    mylcd.lcd_display_string("Remote Control  ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    speed = 100
    mylcd.lcd_display_string("Speed = %d    " % speed , 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    GO = 1
    BURST = 0.2
    while GO == 1:
            for event in get_key():
                if event.code == "KEY_UP":
                        if event.state == 1:
                            pz.forward(speed)
                            time.sleep(BURST)
                            pz.stop()
                        elif event.state == 2:
                            pz.forward(speed)
                        elif event.state == 0:
                            pz.stop()
                if event.code == "KEY_DOWN":
                        if event.state == 1:
                            pz.reverse(speed)
                            time.sleep(BURST)
                            pz.stop()
                        elif event.state == 2:
                            pz.reverse(speed)
                        elif event.state == 0:
                            pz.stop()
                if event.code == "KEY_RIGHT":
                        if event.state == 1:
                            pz.spinRight(speed)
                            time.sleep(BURST)
                            pz.stop()
                        elif event.state == 2:
                            pz.spinRight(speed)
                        elif event.state == 0:
                            pz.stop()
                if event.code == "KEY_LEFT":
                        if event.state == 1:
                            pz.spinLeft(speed)
                            time.sleep(BURST)
                            pz.stop()
                        elif event.state == 2:
                            pz.spinLeft(speed)
                        elif event.state == 0:
                            pz.stop()
                if event.code == "KEY_DOT" or event.code == "KEY_>":
                    if event.state == 1 or event.state == 2:
                        speed = min(100, speed+10)
                        mylcd.lcd_display_string("Speed = %d  " % speed, 1)
                        mylcd.lcd_display_string("Press E to End  ", 2)
                if event.code == "KEY_COMMA" or event.code == "KEY_<":
                    if event.state == 1 or event.state == 2:
                        speed = max (0, speed-10)
                        mylcd.lcd_display_string("Speed = %d  " % speed, 1)
                        mylcd.lcd_display_string("Press E to End  ", 2)
                if event.code == "KEY_SPACE":
                    if event.state == 1 or event.state == 2:
                        pz.stop()
                if event.code == "KEY_E":
                    if event.state == 1 or event.state == 2:
                        GO == 0

def linefollower():
    mylcd.lcd_display_string("Line Follower   ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    speed = 100

def automaze():
    mylcd.lcd_display_string("Auto Maze       ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    speed = 100

def speedrun():
    mylcd.lcd_display_string("Auto Maze       ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    speed = 100
    GO = True
    while True:
        mylcd.lcd_display_string("Press G to GO   ", 1)
        mylcd.lcd_display_string("Press E to End  ", 2)
        if event.code == "KEY_G":
            break
        elif event.code == "KEY_E":
            pz.stop
            GO = False
            break
    while GO == True:
        mylcd.lcd_display_string("GO!!!!!!!!!!!   ", 1)
        mylcd.lcd_display_string("Press S to STOP ", 2)
        pz.forward(100)
        if RIGHTIR == 1:
            pz.spinleft(100)
            time.sleep(0.8)
            pz.forward(100)
        elif LEFTIR == 1:
            pz.spinright(100)
            time.sleep(0.8)
            pz.forward(100)
        elif event.code == "KEY_S":
            pz.stop
            while True:
                mylcd.lcd_display_string("Press G to GO   ", 1)
                mylcd.lcd_display_string("Press S to STOP ", 2)
                if event.code == "KEY_G":
                    break
                elif event.code == "KEY_S":
                   pz.stop
                   GO = False
                   break
        elif event.code == "KEY_E":
            pz.stop
            break

#end functions
#_____________________________________________________________________________

#____________________________________________________________________________________
#Main Loop

mylcd.lcd_display_string("Select Option   ", 1)
mylcd.lcd_display_string("S to Shutdown   ", 2)
MAINLOOP = 1

try:
    while True:
        for event in get_key():
            mylcd.lcd_display_string("Select Option   ", 1)
            mylcd.lcd_display_string("S to Shutdown   ", 2)
            if event.code == "KEY_S":
                mylcd.lcd_display_string("Shutting Down   ", 1)
                mylcd.lcd_display_string("                ", 2)
                os.system("shutdown now -h")
            elif event.code == "KEY_1":
                remotecontrol()
            elif event.code == "KEY_2":
                speedrun()
            

except KeyboardInterrupt:
    print ("")

finally:
    pz.stop()
    pz.cleanup()
    










