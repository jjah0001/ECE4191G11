import RPi.GPIO as GPIO
import time

class Switch:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.left_switch = 10
        self.right_switch = 9
        GPIO.setup(self.left_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def read(self):
        # high = not clicked, low = clicked

        left_state = GPIO.input(self.left_switch)
        right_state = GPIO.input(self.right_switch)
        if (not left_state) and (not right_state):
            return True
        else:
            return False