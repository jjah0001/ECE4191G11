from mag3110 import Compass
import time

compass = Compass()
while True:
    compass.rawMagnetometer()