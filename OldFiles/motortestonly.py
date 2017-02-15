import time
import piconzero as pz

pz.init()
pz.forward(100)
time.sleep(1)
pz.stop()
