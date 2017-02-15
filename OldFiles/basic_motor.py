import pygame
import time
import piconzero as pz

#all the setup
pz.init()
pygame.joystick.init()
screen = pygame.display.set_mode((100,100))
#pygame.display.set_caption("Hello World")
pad = pygame.joystick.Joystick(0)

#initiate pad
pad.init()


#swap these if it turns the wrong way
leftmotor = 0
rightmotor = 1

while True:
    pygame.event.pump()
    x = pad.get_axis(0) 
    y = pad.get_axis(1)
    if 0.1 >= x >= -0.1 and 0.1 >= y >= -0.1: #stop
        x = abs(x)
        y = abs(y)
        r = 0
        l = 0
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "stop"
    elif 0.1 >= x >= -0.1 and y <= -0.9: #full speed forwards
        x = abs(x)
        y = abs(y)
        r = 100 * x
        l = 100 * x
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "full speed"
    elif 0.1 >= x >= -0.1 and y >= 0.9: #full speed backwards
        x = abs(x)
        y = abs(y)
        r = 100 * x
        l = 100 * x
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "full reverse"
    elif -0.9 < x < -0.1 and -0.9 < y < -0.1: #turnR - forwards
        x = abs(x)
        y = abs(y)
        r = 100 * x * (1-y)
        l = 100 * x
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "R forwards"
    elif 0.9 > x > 0.1 and -0.9 < y < -0.1: #turnL - forwards
        x = abs(x)
        y = abs(y)
        r = 100 * x
        l = 100 * x * (1-y)
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "L forwards"
    elif 0.9 > x > 0.1 and 0.1 > y > 0.1: #turnL - backwards
        x = abs(x)
        y = abs(y)
        r = -100 * x
        l = -100 * x * (1-y)
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "L backwards"
    elif x < -0.1 and y > 0.1: #turnR - backwards
        x = abs(x)
        y = abs(y)
        r = -100 * x * (1-y)
        l = -100 * x 
        pz.setMotor(leftmotor,l)
        pz.setMotor(rightmotor,r)
        print "R Backwards"
    time.sleep(2)
    
