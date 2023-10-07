 
import RPi.GPIO as GPIO  
import time 

def angle_to_pwm(angle):
    return (angle/18) +2
GPIO.setmode(GPIO.BCM)  
GPIO.setup(22,GPIO.OUT)  
pwm=GPIO.PWM(22,50)  
pwm.start(0)  


pwm.ChangeDutyCycle(angle_to_pwm(0))  
time.sleep(2)
pwm.ChangeDutyCycle(angle_to_pwm(140))  
time.sleep(2)



pwm.stop()  
GPIO.cleanup()  

