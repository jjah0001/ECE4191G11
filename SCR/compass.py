from mag3110 import MAG3110
import time
import i2c

mag = MAG3110(i2c.I2C0)
while True:
    if (mag.is_data_ready()):
        values = mag.get_values()
        print("mag: ", values)
        time.sleep(0.1)
