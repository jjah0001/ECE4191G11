import mag3110
import time

compass = mag3110.compass()
while True:
    print(compass.rawMagnetometer())
    time.sleep(0.1)