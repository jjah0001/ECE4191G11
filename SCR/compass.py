import mag3110
import time

compass = mag3110.compass()
while True:
    x,y,z, temp = compass.rawMagnetometer()
    print(compass.getBearing())
    time.sleep(0.1)