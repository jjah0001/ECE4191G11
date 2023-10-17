import RPi.GPIO as GPIO  
import time 

class Servo:
    def __init__(self):
        self.servo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  
        GPIO.setup(self.servo_pin,GPIO.OUT)  
        self.pwm=GPIO.PWM(self.servo_pin,50)
        self.pwm.start(0)

    def angle_to_pwm(self, angle):
        return (angle/18) +2


    def operate_door(self):

        self.pwm.ChangeDutyCycle(self.angle_to_pwm(0))  
        time.sleep(3)
        self.pwm.ChangeDutyCycle(self.angle_to_pwm(145))
        time.sleep(0.1)


