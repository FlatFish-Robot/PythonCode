import pygame, sys
from time import sleep

# setup the pygame window
pygame.init()
window = pygame.display.set_mode((200, 200), 0, 32)

# how many joysticks connected to computer?
joystick_count = pygame.joystick.get_count()
print "There is " + str(joystick_count) + " joystick/s"

if joystick_count == 0:
    # if no joysticks, quit program safely
    print ("Error, I did not find any joysticks")
    pygame.quit()
    sys.exit()
else:
    # initialise joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

axes = joystick.get_numaxes()
buttons = joystick.get_numbuttons()
hats = joystick.get_numhats()

print "There is " + str(axes) + " axes"
print "There is " + str(buttons) + " button/s"
print "There is " + str(hats) + " hat/s"


while True:
    for event in pygame.event.get():
      # loop through events, if window shut down, quit program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    print joystick.get_axis(0)
