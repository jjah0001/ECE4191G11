import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
left_switch = 10
right_switch = 9
GPIO.setup(left_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if not GPIO.input(left_switch):
        print("left low")
    if not GPIO.input(right_switch):
        print("right low")
    time.sleep(0.01)