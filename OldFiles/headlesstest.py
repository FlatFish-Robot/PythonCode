#headless from pygame site
"""How to use pygame with no windowing system, like on headless servers.
 
Thumbnail generation with scaling is an example of what you can do with pygame.
NOTE: the pygame scale function uses mmx if available, and can be run 
  in multiple threads.
 
"""
useage = """-scale inputimage outputimage new_width new_height
eg.  -scale in.png out.png 50 50
 
"""
 
import os, sys
 
# set SDL to use the dummy NULL video driver, 
#   so it doesn't need a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"
 
 
import pygame.transform
 
 
if 1:
    #some platforms might need to init the display for some parts of pygame.
    import pygame.display
    pygame.display.init()
    screen = pygame.display.set_mode((1,1))
 
 
 
def scaleit(fin, fout, w, h):
    i = pygame.image.load(fin)
 
    if hasattr(pygame.transform, "smoothscale"):
        scaled_image = pygame.transform.smoothscale(i, (w,h))
    else:
        scaled_image = pygame.transform.scale(i, (w,h))
    pygame.image.save(scaled_image, fout)
if __name__ == "__main__":
    if "-scale" in sys.argv:
        fin, fout, w, h = sys.argv[2:]
        w, h = map(int, [w,h])
        scaleit(fin, fout, w,h)
    else:
        print useage


import pygame
import time


pygame.joystick.init()
#screen = pygame.display.set_mode((100,100))
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
