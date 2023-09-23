from mag3110 import MAG3110
import time

mag3110 = MAG3110()

while True:
	mag3110.datarate_config()
	mag3110.mode_config()
	heading = mag3110.get_heading()
	print(heading)
	time.sleep(0.1)
