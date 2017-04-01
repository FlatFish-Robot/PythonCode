#code for flatfish Mark 6
import piconzero as pz
import time
from gpiozero import Button
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

button = Button(22)

#end of hardware setup
#______________________________________________________________________________


#____________________________________________________________________________________
#functions for individual tasks


def remotecontrol(): #works perfect
    pz.stop()
    mylcd.lcd_display_string("Remote Control  ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    speed = 100
    turnspeed=100
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
                        turnspeed = min(100, turnspeed+10)
                        mylcd.lcd_display_string("Speed = %d  " % speed, 1)
                        mylcd.lcd_display_string("Press E to End  ", 2)
                if event.code == "KEY_COMMA" or event.code == "KEY_<":
                    if event.state == 1 or event.state == 2:
                        speed = max (0, speed-10)
                        turnspeed = max (0, turnspeed-10)
                        mylcd.lcd_display_string("Speed = %d  " % speed, 1)
                        mylcd.lcd_display_string("Press E to End  ", 2)
                if event.code == "KEY_Q":
                    if event.state == 1 or event.state == 2:
                        speed = 75
                        turnspeed = 100
                        mylcd.lcd_display_string("Fast Maze       ", 1)
                        mylcd.lcd_display_string("Press E to End  ", 2)
                if event.code == "KEY_W":
                    if event.state == 1 or event.state == 2:
                        speed = 60
                        turnspeed = 80
                        mylcd.lcd_display_string("slow Maze       ", 1)
                        mylcd.lcd_display_string("Press E to End  ", 2)
                if event.code == "KEY_SPACE":
                    if event.state == 1 or event.state == 2:
                        pz.stop()
                if event.code == "KEY_E":
                    if event.state == 1 or event.state == 2:
                        pz.stop()
                        GO = 0
    

def linefollower(): #works perfectly on a new set of batteries
    mylcd.lcd_display_string("Line Follower   ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    PREP = 1
    GO = 1
    LFSPEED = 75 #only changes cornering speed
    pz.stop()
    
    while PREP == 1: #setup ready for line following
        for event in get_key():
            mylcd.lcd_display_string("Press G to GO   ", 1)
            mylcd.lcd_display_string("Press E to End  ", 2)
            if event.code == "KEY_G":
                PREP = 0
            elif event.code == "KEY_E":
                GO = 0
                PREP = 0
                
    while GO == 1: #new simple quit - works perfectly
        if button.is_pressed:
            pz.stop()
            GO = 0
                                  
        else:
            mylcd.lcd_display_string("GO!!!!!!!!!!!   ", 1)
            mylcd.lcd_display_string("Switch = stop   ", 2)
            LEFTLINE = pz.readInput(2) #assign right line sensor to a variable
            RIGHTLINE = pz.readInput(3) #assign left line sensor to a variable   
            if RIGHTLINE == 1:
                pz.spinRight(LFSPEED)
                #time.sleep(0.5)
            elif LEFTLINE == 1:
                pz.spinLeft(LFSPEED)
                #time.sleep(0.5)
            elif LEFTLINE == 0 and RIGHTLINE == 0:
                pz.forward(15)
                #time.sleep(0.5)
            elif LEFTLINE == 1 and RIGHTLINE == 1:
                pz.reverse(15)
                #time.sleep(0.5)
                
def automaze():
    pz.stop()
    mylcd.lcd_display_string("Auto Maze       ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    MSPEED = 20
    MTURN = 90
    GO = 1
    PREP = 1
    while PREP == 1: #get ready to go
        for event in get_key():
            mylcd.lcd_display_string("Press G to GO   ", 1)
            mylcd.lcd_display_string("Press E to End  ", 2)
            if event.code == "KEY_G":
                PREP = 0
            elif event.code == "KEY_E":
                GO = 0
                PREP = 0
                
    while GO == 1: #new simple quit - works perfectly
        if button.is_pressed:
            pz.stop()
            GO = 0

        else:
            RIGHTIR = pz.readInput(0) #assign right IR to a variable
            LEFTIR = pz.readInput(1) #assign left IR to a variable
            RANGE = hcsr04.getDistance() #assign HC-SR04 range to variable
            STEP = 0 # start step count
            mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
            mylcd.lcd_display_string("Step = %d %%" % STEP, 2)
            pz.forward(MSPEED)
            
            #steps to follow to complete the maze
            if RANGE < 25 and STEP == 0: #first right turn
                pz.stop()
                pz.spinRight(MTURN)
                time.sleep(0.5)
                pz.stop()
                pz.forward(MSPEED)
                time.sleep(1)
                STEP = 1
                mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
                mylcd.lcd_display_string("Step = %d %%" % STEP, 2)
            if RANGE < 25 and STEP == 1: #second right turn
                pz.stop()
                pz.spinRight(MTURN)
                time.sleep(0.5)
                pz.stop()
                pz.forward(MSPEED)
                time.sleep(1)
                STEP = 2
                mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
                mylcd.lcd_display_string("Step = %d %%" % STEP, 2)
            if RANGE < 25 and STEP == 2: #third right
                pz.stop()
                pz.spinRight(MTURN)
                time.sleep(0.5)
                pz.stop()
                pz.forward(MSPEED)
                time.sleep(1)
                STEP = 3
                mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
                mylcd.lcd_display_string("Step = %d %%" % STEP, 2)
            if RANGE < 25 and STEP == 2: #first left
                pz.stop()
                pz.spinLeft(MTURN)
                time.sleep(0.5)
                pz.stop()
                pz.forward(MSPEED)
                time.sleep(1)
                STEP = 4
                mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
                mylcd.lcd_display_string("Step = %d %%" % STEP, 2)
            if RANGE < 25 and STEP == 4: #second left
                pz.stop()
                pz.spinLeft(MTURN)
                time.sleep(0.5)
                pz.stop()
                pz.forward(MSPEED)
                time.sleep(1)
                STEP = 5
                mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
                mylcd.lcd_display_string("Step = %d %%" % STEP, 2)
            if RANGE < 25 and STEP == 5: #third left
                pz.stop()
                pz.spinLeft(MTURN)
                time.sleep(0.5)
                pz.stop()
                pz.forward(MSPEED)
                time.sleep(1)
                STEP = 6
                mylcd.lcd_display_string("Range = %d %%" % RANGE, 1)
                mylcd.lcd_display_string("Step = %d %%" % STEP, 2)

            #emergency wall avoidance protocol    
            if LEFTIR == 0:
                pz.spinRight(100)
                time.sleep(0.01)
            elif RIGHTIR == 0:
                pz.spinLeft(100)
                time.sleep(0.01)


def speedrun():
    pz.stop()
    mylcd.lcd_display_string("Speed Run       ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    time.sleep(2)
    speed = 100
    GO = 1
    PREP = 1
    
    while PREP == 1: #get ready to go
        for event in get_key():
            mylcd.lcd_display_string("Press G to GO   ", 1)
            mylcd.lcd_display_string("Press E to End  ", 2)
            if event.code == "KEY_G":
                PREP = 0
            elif event.code == "KEY_E":
                pz.stop
                GO = 0
                PREP = 0
                
    while GO == 1: #new simple quit - works perfectly
        if button.is_pressed:
            pz.stop()
            GO = 0
            
        else:
            RIGHTIR = pz.readInput(0) 
            LEFTIR = pz.readInput(1)            
            if RIGHTIR == 0:
                pz.spinLeft(100)
                mylcd.lcd_display_string("Right IR on     ", 1)
                mylcd.lcd_display_string("Use switch=STOP ", 2)
            elif LEFTIR == 0:
                pz.spinRight(100)
                mylcd.lcd_display_string("left IR on      ", 1)
                mylcd.lcd_display_string("Use switch=STOP ", 2)
            elif RIGHTIR == 1 and LEFTIR == 1:
                pz.forward(100)
                mylcd.lcd_display_string("No IR on     ", 1)
                mylcd.lcd_display_string("Use switch=STOP ", 2)


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
                pz.stop()
                pz.cleanup()
                os.system("sudo shutdown -h now")
            elif event.code == "KEY_ESC":
                mylcd.lcd_display_string("Ending Program  ", 1)
                mylcd.lcd_display_string("                ", 2)
                pz.stop()
                pz.cleanup()
                sys.exit()
            elif event.code == "KEY_1":
                remotecontrol()
            elif event.code == "KEY_2":
                speedrun()
            elif event.code == "KEY_3":
                linefollower()
            elif event.code == "KEY_4":
                automaze()
            

except KeyboardInterrupt:
    print ("")

finally:
    pz.stop()
    pz.cleanup()
    










