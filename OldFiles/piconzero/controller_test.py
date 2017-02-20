import pygame
import piconzero as pz
import time
from pygame.locals import *

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((20,20))
#pygame.display.set_caption("Hello World")
joystick_count = pygame.joystick.get_count()
print(joystick_count)


joystick = pygame.joystick.Joystick(0)
joystick.init()
print(joystick.get_name())
print(joystick.get_id())

joystick.init()
print(joystick.get_init())
print(joystick.get_numbuttons())
print(joystick.get_numaxes())
print(joystick.get_numballs())
print(joystick.get_numhats())

while True:
    move = joystick.get_axis(0)
    print(move)
    time.sleep(0.5)
