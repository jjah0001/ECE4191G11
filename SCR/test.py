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

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    


while(1):

    x=input()
    
    if x=='r':
        print("run")
        logging.info('Run')
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         logging.info('Forward')
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         logging.info('Backwards')
         x='z'


    elif x=='s':
        print("stop")
        logging.info('Stop')
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'
        logging.info('Forward')

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'
        logging.info('Backward')

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(20)
        x='z'
        logging.info('Low')

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(60)
        x='z'
        logging.info('Medium')

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(100)
        x='z'
        logging.info('High')
     
    
    elif x=='e':
        GPIO.cleanup()
        logging.error('Code terminated')
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")