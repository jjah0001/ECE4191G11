from motor import Motor
import time
from led import LED


motor = Motor()

motor.rotate("CW")
time.sleep(10)
motor.stop()