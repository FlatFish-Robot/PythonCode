#core script to run at startup for flatfish robot
from triangula.input import SixAxis, SixAxisResource
import time
import smbus
import os
import hcsr04
import piconzero as pz
from gpiozero import Button
import I2C_LCD_driver

#__________________________________________________________________
#initiate piconzero and display

pz.init() #initiate hardware
mylcd = I2C_LCD_driver.lcd() #assign LCD to variable for ease of use

pz.setInputConfig(0,0) #developer switch is input 0 and digital
pz.setInputConfig(1,0) #right IR sensor is input 1 and digital
pz.setInputConfig(2,0) #left IR sensor is input 2 and digital
pz.setInputConfig(3,0) #right line sensor is input 3 and digital
pz.setInputConfig(4,0) #left line is input 4 and digital

DEVELOPER = Button(22) #assign developer switch to variable
DEVELOPER = 0
RIGHTIR = pz.readInput(0) #assign right IR to a variable
LEFTIR = pz.readInput(1) #assign left IR to a variable
RIGHTLINE = pz.readInput(2) #assign right line sensor to a variable
LEFTLINE = pz.readInput(3) #assign left line sensor to a variable

hcsr04.init() #initiate hardware
RANGE = hcsr04.getDistance() #assign HC-SR04 range to variable

#__________________________________________________________________
#Functions for individual programs

#__________________________________________________________________
#Sub routines as functions for individual programs




#__________________________________________________________________
#Main program
MAINRUN = 1

#LCD prompt
COUNTDOWN = 9
while COUNTDOWN > 0:
    mylcd.lcd_display_string("Connect", 1)
    mylcd.lcd_display_string("Controller %d %%" % COUNTDOWN, 2)
    time.sleep(1)
    COUNTDOWN = COUNTDOWN - 1

# Get a joystick
with SixAxisResource() as joystick:
    #Main loop - using this for the menu system
    while MAINRUN == 1:
            #mylcd.lcd_display_string("Starting", 1)
            #mylcd.lcd_display_string("Remote Control B", 2)
            #time.sleep(2)            
            #remotecontrolbasic()
            print ("Remote Control Program Active")
            mylcd.lcd_display_string("Remote Control B", 1)
            mylcd.lcd_display_string("Select Ends   ", 2)
            time.sleep(2)
            RUN = 1
            buttons_pressed = joystick.get_and_clear_button_press_history()
            while RUN == 1:
                print("In Loop")
                buttons_pressed = joystick.get_and_clear_button_press_history()
                if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
                    RUN = 0
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_UP:
                    pz.forward(60)
                    print("Forwards")
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_DOWN:
                    pz.reverse(60)
                    print("Reverse")
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_RIGHT:
                    pz.spinRight(60)
                    print("Right")
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_LEFT:
                    pz.spinLeft(60)
                    print("Left")
                else:
                    RUN = 1
                    pz.stop()
                time.sleep(0.01)
        #____________________________________________________________________________________________________________________


        elif buttons_pressed & 1 << SixAxis.BUTTON_CIRCLE:
            print ("Remote control complex")
            mylcd.lcd_display_string("Starting", 1)
            mylcd.lcd_display_string("Remote Control C", 2)
            time.sleep(2)            
            remotecontrolcomplex()
        elif buttons_pressed & 1 << SixAxis.BUTTON_TRIANGLE:
            print ("Square Pressed")
        elif buttons_pressed & 1 << SixAxis.BUTTON_CROSS:
            print ("Square Pressed")

mylcd.lcd_display_string("Ended", 1)
time.sleep(2)
pz.cleanup()

