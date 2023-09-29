import RPi.GPIO as GPIO
import time


# clockwise = OPEN, duty = 6.5
# c-clockwise = CLOSE, duty = 7.5

open_duty = 6.2 
close_duty = 7.8
GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)
servo1 = GPIO.PWM(22,50)

servo1.start(0)
print("Waiting for 2 seconds")

servo1.ChangeDutyCycle(0)
time.sleep(2)

print("rotating 180 degs in 10 step")

 
servo1.ChangeDutyCycle(close_duty)
time.sleep(2)

servo1.ChangeDutyCycle(0)

time.sleep(1)

servo1.ChangeDutyCycle(open_duty)
time.sleep(2)

GPIO.cleanup()