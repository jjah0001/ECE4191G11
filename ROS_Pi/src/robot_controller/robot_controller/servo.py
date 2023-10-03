import RPi.GPIO as GPIO  
import time 

class Servo:
    def __init__(self):
        # set up GPIO
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(22,GPIO.OUT)  
        self.pwm=GPIO.PWM(22,50)  
        self.pwm.stop()  


    def angle_to_pwm(self, angle):
        return (angle/18) +2


    def operate_door(self):
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(self.angle_to_pwm(0))  
        time.sleep(5)
        self.pwm.ChangeDutyCycle(self.angle_to_pwm(140))
        self.pwm.stop()

