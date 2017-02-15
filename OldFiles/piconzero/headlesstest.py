import pygame
import time


pygame.joystick.init()
screen = pygame.display.set_mode((100,100))
#pygame.display.set_caption("Hello World")
joystick_count = pygame.joystick.get_count()
print joystick_count


pad = pygame.joystick.Joystick(0)
print pad.get_name()
print pad.get_id()

pad.init()
print pad.get_init()
print pad.get_numbuttons()
print pad.get_numaxes()
print pad.get_numballs()
print pad.get_numhats() 

while True:
    pygame.event.pump()
    print "new run"
    print pad.get_axis(0)
    print pad.get_axis(1)
    print "_______"
    print " "
    time.sleep(5)
