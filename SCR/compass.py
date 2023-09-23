from mag3110 import Compass
import time

compass = Compass()
compass.loadCalibration()

while True:
    print(compass.rawMagnetometer())
