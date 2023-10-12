import RPi.GPIO as GPIO
import time

class LED:
    def __init__(self):
        self.led_pin = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin,GPIO.OUT)
        self.current_mode = 0

    def turn_on(self):
        self.current_mode = 1
        GPIO.output(self.led_pin,GPIO.HIGH)

    def turn_off(self):
        self.current_mode = 0
        GPIO.output(self.led_pin,GPIO.LOW)
    
    def flash(self):
        if self.current_mode:
            GPIO.output(self.led_pin,GPIO.LOW)
            self.current_mode = 0
        else:
            GPIO.output(self.led_pin,GPIO.HIGH)
            self.current_mode = 1


led = LED()

while True:
    led.flash()
    time.sleep(0.5)