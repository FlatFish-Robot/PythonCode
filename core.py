#core script to run at startup for flatfish robot
from triangula.input import SixAxis, SixAxisResource
import time
import smbus
import os
import hcsr04
import piconzero

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
#Functions for individual programs

#__________________________________________________________________
#Sub routines as functions for individual programs

def remotecontrol:
    print ("Remote Control Program Active")

def linefollow:
    print ("Line Following Program Active")

def automaze:
    print("Automaze Program Active")

def autospeed:
    print("Autospeed Program Active")

def wallstop:
    print("Wall Stop Program Active")

#__________________________________________________________________
#Main program


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
    while 1:
        lcd_string("Main Menu       <",LCD_LINE_1)
        lcd_string("Select Program  <",LCD_LINE_2)
        buttons_pressed = joystick.get_and_clear_button_press_history()
        x = joystick.axes[0].corrected_value()
        y = joystick.axes[1].corrected_value()
        if buttons_pressed & 1 << SixAxis.BUTTON_START:
            lcd_string("Shutting Down   <",LCD_LINE_1)
            lcd_string("                <",LCD_LINE_2)
            time.sleep(5)
            os.system("shutdown now -h")
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

