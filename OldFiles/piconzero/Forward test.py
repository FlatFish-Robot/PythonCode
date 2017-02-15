import piconzero as pz
import time

pz.init()
pz.forward(50)
time.sleep(1)
pz.reverse(50)
time.sleep(1)
pz.spinRight(100)
time.sleep(1)
pz.spinLeft(100)
time.sleep(1)
pz.stop()
