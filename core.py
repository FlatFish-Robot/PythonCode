#core script to run at startup for flatfish robot
from triangula.input import SixAxis, SixAxisResource
import time
import smbus
import os
import hcsr04 as hc
import piconzero as pz
from gpiozero import Button

#__________________________________________________________________
#Intialise the display - from http://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi/

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

#__________________________________________________________________
#initiate piconzero

pz.init() #initiate hardware

pz.setInputConfig(0,0) #developer switch is input 0 and digital
pz.setInputConfig(1,0) #right IR sensor is input 1 and digital
pz.setInputConfig(2,0) #left IR sensor is input 2 and digital
pz.setInputConfig(3,0) #right line sensor is input 3 and digital
pz.setInputConfig(4,0) #left line is input 4 and digital

DEVELOPER = Button(22) #assign developer switch to variable
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

def remotecontrol:
    print ("Remote Control Program Active")
    lcd_string("Remote Control  <",LCD_LINE_1)
    lcd_string("Select Ends     <",LCD_LINE_2)
    RUN = 1
    while RUN == 1:
        x = joystick.axes[0].corrected_value()
        y = joystick.axes[1].corrected_value()
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif 0.1 >= x >= -0.1 and 0.1 >= y >= -0.1: #stop
            x = abs(x)
            y = abs(y)
            r = 0
            l = 0
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)    
        elif 0.1 >= x >= -0.1 and y <= -0.1: #full speed forwards
            x = abs(x)
            y = abs(y)
            r = 100 * y
            l = 100 * y
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)
        elif 0.1 >= x >= -0.1 and y >= 0.1: #full speed backwards
            x = abs(x)
            y = abs(y)
            r = 100 * y
            l = 100 * y
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r) 
        elif x <= -0.1 and 0.1 >= y >= -0.1: #spin right
            x = abs(x)
            y = abs(y)
            r = -100 * x
            l = 100 * x
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)
        elif x >= 0.1 and 0.1 >= y >= -0.1: #spin left
            x = abs(x)
            y = abs(y)
            r = 100 * x
            l = -100 * x
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r) 
        elif -0.9 < x < -0.1 and -0.9 < y < -0.1: #turnR - forwards
            x = abs(x)
            y = abs(y)
            r = 100 * x * (1-y)
            l = 100 * x
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)
        elif 0.9 > x > 0.1 and -0.9 < y < -0.1: #turnL - forwards
            x = abs(x)
            y = abs(y)
            r = 100 * x
            l = 100 * x * (1-y)
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)
        elif 0.9 > x > 0.1 and 0.1 > y > 0.1: #turnL - backwards
            x = abs(x)
            y = abs(y)
            r = -100 * x
            l = -100 * x * (1-y)
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)
        elif x < -0.1 and y > 0.1: #turnR - backwards
            x = abs(x)
            y = abs(y)
            r = -100 * x * (1-y)
            l = -100 * x 
            pz.setMotor(leftmotor,l)
            pz.setMotor(rightmotor,r)
    

def linefollow:
    print ("Line Following Program Active")
    lcd_string("Line Following  <",LCD_LINE_1)
    lcd_string("Select Ends     <",LCD_LINE_2)
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

def automaze:
    print("Automaze Program Active")
    lcd_string("Automaze        <",LCD_LINE_1)
    lcd_string("Select Ends     <",LCD_LINE_2)
    LINE = 0 #set reflectivity - swap with BACKGROUND to invert
    BACKGROUND = 1 #set reflectivity - swap with LINE to invert
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        

def autospeed:
    print("Autospeed Program Active")
    lcd_string("Autospeed       <",LCD_LINE_1)
    lcd_string("Select Ends     <",LCD_LINE_2)
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

def wallstop:
    print("Wall Stop Program Active")
    lcd_string("Wallstop        <",LCD_LINE_1)
    lcd_string("Select Ends     <",LCD_LINE_2)
    RUN = 1
    while RUN == 1:
        if buttons_pressed & 1 << SixAxis.BUTTON_SELECT:
            RUN = 0
        elif RANGE > 10:
            pz.forward(100)
            lcd_string("Range=          <",LCD_LINE_1)
            lcd_string(RANGE."     <",LCD_LINE_2)
        elif 5 < RANGE =< 10:
            pz.forward(40)
            lcd_string("Range=          <",LCD_LINE_1)
            lcd_string(RANGE."     <",LCD_LINE_2)
        elif 2 < RANGE =< 5:
            pz.forward(20)
            lcd_string("Range=          <",LCD_LINE_1)
            lcd_string(RANGE."     <",LCD_LINE_2)
        elif 1 <= RANGE =< 2:
            pz.forward(10)
            lcd_string("Range=          <",LCD_LINE_1)
            lcd_string(RANGE."     <",LCD_LINE_2)
        elif RANGE < 1:
            pz.stop(0)
            lcd_string("Range=          <",LCD_LINE_1)
            lcd_string(RANGE."     <",LCD_LINE_2)
            time.sleep(2)
            lcd_string("Wallstop Ended  <",LCD_LINE_1)
            lcd_string("Select For Menu <",LCD_LINE_2)
            time.sleep(10)


#__________________________________________________________________
#Main program
MAINRUN = 1

#LCD prompt
COUNTDOWN = 9
while COUNTDOWN > 0:
    DISPLAYCOUNTDOWN = "Connect PS3 - " . COUNTDOWN . "<"
    lcd_string("Starting Up     <",LCD_LINE_1)
    lcd_string(DISPLAYCOUNTDOWN ,LCD_LINE_2)
    time.sleep(1)
    COUNTDOWN = COUNTDOWN - 1

# Get a joystick
with SixAxisResource() as joystick:
    
    #Main loop - using this for the menu system
    while MAINRUN == 1:
        lcd_string("Main Menu       <",LCD_LINE_1)
        lcd_string("Select Program  <",LCD_LINE_2)

        buttons_pressed = joystick.get_and_clear_button_press_history()

        pz.stop()

        if DEVELOPER == 1: #check for developer switch activation and if positive kill program
            lcd_string("Killing Program <",LCD_LINE_1)
            lcd_string("                <",LCD_LINE_2)
            time.sleep(5)
            MAINRUN = 0
        elif buttons_pressed & 1 << SixAxis.BUTTON_START: #shutdown the pi if start is pressed
            lcd_string("Shutting Down   <",LCD_LINE_1)
            lcd_string("Confirm?        <",LCD_LINE_2)
            time.sleep(2)
            if buttons_pressed & 1 << SixAxis.BUTTON_START:
                pz.cleanup()
                os.system("shutdown now -h")
            else:
                lcd_string("Shut Down       <",LCD_LINE_1)
                lcd_string("Cancelled       <",LCD_LINE_2)
                time.sleep(2)
                lcd_string("Main Menu       <",LCD_LINE_1)
                lcd_string("Select Program  <",LCD_LINE_2)
        elif buttons_pressed & 1 << SixAxis.BUTTON_SQUARE:
            lcd_string("Starting.....   <",LCD_LINE_1)
            lcd_string("Remote Control  <",LCD_LINE_2)
            time.sleep(2)            
            remotecontrol()
        elif buttons_pressed & 1 << SixAxis.BUTTON_CIRCLE:
            print ("Square Pressed")
        elif buttons_pressed & 1 << SixAxis.BUTTON_TRIANGE:
            print ("Square Pressed")
        elif buttons_pressed & 1 << SixAxis.BUTTON_CROSS:
            print ("Square Pressed")

lcd_string("Program Dead    <",LCD_LINE_1)
lcd_string("                <",LCD_LINE_2)
time.sleep(2)
pz.cleanup()

