from motor import Motor
import time
from led import LED


motor = Motor()
led = LED()

motor.drive_forwards(2)
motor.stop()
led.turn_on()
time.sleep(3)
led.turn_off()
motor.drive_forwards(5)
motor.stop()