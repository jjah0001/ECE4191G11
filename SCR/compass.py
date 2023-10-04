from mag3110 import Compass
import time

compass = Compass()
compass.calibrate()
compass.loadCalibration()

while True:
    print(compass.getBearing())
    time.sleep(0.1)
