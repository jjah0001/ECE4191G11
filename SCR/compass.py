from mag3110 import MAG3110
import time

mag3110 = MAG3110()

while True:
	mag3110.datarate_config()
	mag3110.mode_config()
	mag = mag3110.read_mag()
	print ("Magnetic field in X-Axis : %d"%(mag['x']))
	print ("Magnetic field in Y-Axis : %d"%(mag['y']))
	print ("Magnetic field in Z-Axis : %d"%(mag['z']))
	print (" ************************************* ")
	time.sleep(0.1)
