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

def remotecontrolcomplex():
    print ("Remote Control Program Active")
    mylcd.lcd_display_string("Remote Control C", 1)
    mylcd.lcd_display_string("Select Ends", 2)
    time.sleep(2)
    RUN = 1
    while RUN == 1:
        x = joystick.axes[0].corrected_value()
        y = joystick.axes[1].corrected_value()
        r = 0
        l = 0
        #mylcd.lcd_display_string("X: %d " % r, 1)
        #mylcd.lcd_display_string("Y: %d " % l, 2)
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif 0.1 >= x >= -0.1 and 0.1 >= y >= -0.1: #stop
            x = abs(x)
            y = abs(y)
            r = 0
            l = 0
            pz.setMotor(0,l)
            pz.setMotor(1,r)    
        elif 0.1 >= x >= -0.1 and y <= -0.1: #full speed forwards
            x = abs(x)
            y = abs(y)
            r = int(100 * y)
            l = int(100 * y)
            pz.setMotor(0,l)
            pz.setMotor(1,r)
        elif 0.1 >= x >= -0.1 and y >= 0.1: #full speed backwards
            x = abs(x)
            y = abs(y)
            r = int(100 * y)
            l = int(100 * y)
            pz.setMotor(0,l)
            pz.setMotor(1,r) 
        elif x <= -0.1 and 0.1 >= y >= -0.1: #spin right
            x = abs(x)
            y = abs(y)
            r = int(-100 * x)
            l = int(100 * x)
            pz.setMotor(0,l)
            pz.setMotor(1,r)
        elif x >= 0.1 and 0.1 >= y >= -0.1: #spin left
            x = abs(x)
            y = abs(y)
            r = int(100 * x)
            l = int(-100 * x)
            pz.setMotor(0,l)
            pz.setMotor(1,r) 
        elif -0.9 < x < -0.1 and -0.9 < y < -0.1: #turnR - forwards
            x = abs(x)
            y = abs(y)
            r = int(100 * x * (1-y))
            l = int(100 * x)
            pz.setMotor(0,l)
            pz.setMotor(1,r)
        elif 0.9 > x > 0.1 and -0.9 < y < -0.1: #turnL - forwards
            x = abs(x)
            y = abs(y)
            r = int(100 * x)
            l = int(100 * x * (1-y))
            pz.setMotor(0,l)
            pz.setMotor(1,r)
        elif 0.9 > x > 0.1 and 0.1 > y > 0.1: #turnL - backwards
            x = abs(x)
            y = abs(y)
            r = int(-100 * x)
            l = int(-100 * x * (1-y))
            pz.setMotor(0,l)
            pz.setMotor(1,r)
        elif x < -0.1 and y > 0.1: #turnR - backwards
            x = abs(x)
            y = abs(y)
            r = int(-100 * x * (1-y))
            l = int(-100 * x )
            pz.setMotor(0,l)
            pz.setMotor(1,r)

def remotecontrolbasic():
    print ("Remote Control Program Active")
    mylcd.lcd_display_string("Remote Control B", 1)
    mylcd.lcd_display_string("Select Ends", 2)
    time.sleep(2)
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif buttons_pressed & 1 << SixAxis.BUTTON_D_UP:
            pz.forward(100)
        elif buttons_pressed & 1 << SixAxis.BUTTON_D_DOWN:
            pz.reverse(100)
        elif buttons_pressed & 1 << SixAxis.BUTTON_D_RIGHT:
            pz.spinRight(100)
        elif buttons_pressed & 1 << SixAxis.BUTTON_D_LEFT:
            pz.spinLeft(100)
            
            
    

def linefollow():
    print ("Line Following Program Active")
    mylcd.lcd_display_string("Line Follow", 1)
    mylcd.lcd_display_string("Select Ends", 2)
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif RIGHTLINE == BACKGROUND and LEFTLINE == BACKGROUND:
            pz.forward(100)
        elif RIGHTLINE == LINE and LEFTLINE == BACKGROUND:
            pz.spinRight(40)
        elif RIGHTLINE == BACKGROUND and LEFTLINE == LINE:
            pz.spinLeft(40)
        elif RIGHTLINE == LINE and LEFTLINE == LINE:
            pz.reverse(70)

def automaze():
    print("Automaze Program Active")
    mylcd.lcd_display_string("Automaze", 1)
    mylcd.lcd_display_string("Select Ends", 2)
    LINE = 0 #set reflectivity - swap with BACKGROUND to invert
    BACKGROUND = 1 #set reflectivity - swap with LINE to invert
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        

def autospeed():
    print("Autospeed Program Active")
    mylcd.lcd_display_string("Autospeed", 1)
    mylcd.lcd_display_string("Select Ends", 2)
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif RIGHTIR == 0 and LEFTIR == 0:
            pz.forward(100)
        elif RIGHTIR == 1 and LEFTIR == 0:
            pz.reverse(40)
            time.sleep(1)
            pz.spinLeft(40)
            time.sleep(0.3)
        elif RIGHTIR == 0 and LEFTIR == 1:
            pz.reverse(40)
            time.sleep(1)
            pz.spinRight(40)
            time.sleep(0.3)

def wallstop():
    print("Wall Stop Program Active")
    mylcd.lcd_display_string("Wall Stop", 1)
    mylcd.lcd_display_string("Select Ends", 2)
    
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif RANGE > 10:
            pz.forward(100)
            mylcd.lcd_display_string("Range= %d %%" % RANGE, 2)
        elif 5 < RANGE <= 10:
            pz.forward(40)
            mylcd.lcd_display_string("Range= %d %%" % RANGE, 2)
        elif 2 < RANGE <= 5:
            pz.forward(20)
            mylcd.lcd_display_string("Range= %d %%" % RANGE, 2)
        elif 1 <= RANGE <= 2:
            pz.forward(10)
            mylcd.lcd_display_string("Range= %d %%" % RANGE, 2)
        elif RANGE < 1:
            pz.stop(0)
            mylcd.lcd_display_string("Range= %d %%" % RANGE, 2)
            time.sleep(2)
            mylcd.lcd_display_string("Ended", 1)
            mylcd.lcd_display_string("Press Select", 2)
            time.sleep(10)


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
        mylcd.lcd_display_string("Main Menu", 1)
        mylcd.lcd_display_string("Select Program", 2)

        buttons_pressed = joystick.get_and_clear_button_press_history()

        pz.stop()

        if DEVELOPER == 1: #check for developer switch activation and if positive kill program
            mylcd.lcd_display_string("Killing", 1)
            mylcd.lcd_display_string("Program", 2)
            time.sleep(5)
            MAINRUN = 0
        #_______________________________________________________________________________________________________________



        elif buttons_pressed & 1 << SixAxis.BUTTON_START: #shutdown the pi if start is pressed
            mylcd.lcd_display_string("Shut Down", 1)
            mylcd.lcd_display_string("Confirm?", 2)
            time.sleep(2)
            if buttons_pressed & 1 << SixAxis.BUTTON_START:
                pz.cleanup()
                os.system("shutdown now -h")
            else:
                mylcd.lcd_display_string("Shut Down", 1)
                mylcd.lcd_display_string("Cancelled", 2)
                time.sleep(2)
        #_________________________________________________________________________________________________________________

        
        elif buttons_pressed & 1 << SixAxis.BUTTON_SQUARE:
            #mylcd.lcd_display_string("Starting", 1)
            #mylcd.lcd_display_string("Remote Control B", 2)
            #time.sleep(2)            
            #remotecontrolbasic()
            print ("Remote Control Program Active")
            mylcd.lcd_display_string("Remote Control B", 1)
            mylcd.lcd_display_string("Select Ends   ", 2)
            time.sleep(2)
            RUN = 1
            while RUN == 1:
                print("In Loop")
                if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
                    RUN = 0
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_UP:
                    pz.forward(100)
                    print("Forwards")
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_DOWN:
                    pz.reverse(100)
                    print("Reverse")
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_RIGHT:
                    pz.spinRight(100)
                    print("Right")
                elif buttons_pressed & 1 << SixAxis.BUTTON_D_LEFT:
                    pz.spinLeft(100)
                    print("Left")
                else:
                    RUN = 1
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

