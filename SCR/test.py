import RPi.GPIO as GPIO          
from time import sleep
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Define the format for the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler
file_handler = logging.FileHandler('../log/test_code.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

#    Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logging.info('Setup ready')

in1 = 23
in2 = 24
en = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1=GPIO.PWM(en,1000)



in3 = 8
in4 = 7
en2 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2,1000)
p2.start(0)


print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    


def set_speed(motor, direction = "forward", speed = 0):
    """
    Set speed and direction for selected motor

    :param motor:  Either 0 or 1 to select motor
    :param direction: "forward" or "reverse"
    :param speed: 0-100%
    
    """

    if speed < 0 or speed > 100:
        raise Exception("Invalid speed")

    if motor == 0:
        p1.start(0)
        if direction == "forward":
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        elif direction == "reverse":
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
        else:
            raise Exception("Invalid direction")
        p1.ChangeDutyCycle(speed)
    elif motor == 1:
        p2.start(0)
        if direction == "forward":
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
        elif direction == "reverse":
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
        else:
            raise Exception("Invalid direction")
        p2.ChangeDutyCycle(speed)
    else:
        raise Exception("Invalid motor selected")
        
def stop_motor(motor):
    if motor == 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        p1.stop()
    elif motor == 1:
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        p2.stop()
    else:
        raise Exception("Invalid motor selected")


while(1):

    x=input()
    
    if x=='r':
        set_speed(0, "forward", 50)
        set_speed(1, "forward", 50)
    if x == "s":
        stop_motor(0)
        stop_motor(1)
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
