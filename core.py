#code for flatfish Mark 6
import piconzero as pz
import time
import sys
import tty
import termios
import os
import hcsr04
import I2C_LCD_driver
#I2C LCD driver from http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

#======================================================================
# Reading single character by forcing stdin to raw mode

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================


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
    mylcd.lcd_display_string("Speed = %d    ", 1)
    mylcd.lcd_display_string("Press E to End  ", 2)
    while True:
        keyp = readkey()
        if ord(keyp) == 16:
            pz.forward(speed)
            keyp = readkey()
        if ord(keyp) == 17:
            pz.reverse(speed)
            keyp = readkey()
        if ord(keyp) == 18:
            pz.spinRight(speed)
            keyp = readkey()
        if ord(keyp) == 19:
            keyp = readkey()
            pz.spinLeft(speed)
        if keyp == '.' or keyp == '>':
            keyp = readkey()
            speed = min(100, speed+10)
            mylcd.lcd_display_string("Speed = %d  " % speed, 1)
            mylcd.lcd_display_string("Press E to End  ", 2)
        if keyp == ',' or keyp == '<':
            keyp = readkey()
            speed = max (0, speed-10)
            mylcd.lcd_display_string("Speed = %d  " % speed, 1)
            mylcd.lcd_display_string("Press E to End  ", 2)
        if keyp == ' ':
            keyp = readkey()
            pz.stop()
        if keyp == 'e':
            keyp = readkey()
            break
        time.sleep(0.02)

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
        keyp = readkey()
        mylcd.lcd_display_string("Press G to GO   ", 1)
        mylcd.lcd_display_string("Press E to End  ", 2)
        if keyp == 'g':
            break
        elif keyp == 'e':
            pz.stop
            GO = False
            break
    while GO == True:
        keyp = readkey()
        mylcd.lcd_display_string("GO!!!!!!!!!!!   ", 1)
        mylcd.lcd_display_string("Press S to STOP ", 2)
        if RIGHTIR == 1:
            pz.spinleft(100)
            time.sleep(0.5)
        elif LEFTIR == 1:
            pz.spinright(100)
            time.sleep(0.5)
        elif keyp == 's':
            pz.stop
            while True:
                keyp = readkey()
                mylcd.lcd_display_string("Press G to GO   ", 1)
                mylcd.lcd_display_string("Press S to STOP ", 2)
                if keyp == 'g':
                    break
                elif keyp == 'e':
                   pz.stop
                   break
        elif keyp == 'e':
            pz.stop
            break

#end functions
#_____________________________________________________________________________

#____________________________________________________________________________________
#Main Loop

mylcd.lcd_display_string("Select Option   ", 1)
mylcd.lcd_display_string("S to Shutdown   ", 2)

try:
    while True:
        keyp = readkey()
        mylcd.lcd_display_string("Select Option   ", 1)
        mylcd.lcd_display_string("S to Shutdown   ", 2)
        if keyp == 's':
            mylcd.lcd_display_string("Shutting Down   ", 1)
            mylcd.lcd_display_string("                ", 2)
            os.system("shutdown now -h")
        elif keyp == '1':
            remotecontrol()
            

except KeyboardInterrupt:
    print ("")

finally:
    pz.stop()
    pz.cleanup()
    










