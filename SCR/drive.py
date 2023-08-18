import RPi.GPIO as GPIO          
from time import sleep
import logging


class Drive():
    def __init__(self):
        # Logging:
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # Define the format for the log messages
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create a file handler
        self.file_handler = logging.FileHandler('../log/test_code.log')
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)

        # Create a console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        self.console_handler.setFormatter(self.formatter)

        #    Add the handlers to the logger
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

        logging.info('Drive class initialised')

        # Setting up GPIO
        self.in1 = 23
        self.in2 = 24
        self.en = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.en,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.p1=GPIO.PWM(self.en,1000)



        self.in3 = 8
        self.in4 = 7
        self.en2 = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.en2,GPIO.OUT)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        self.p2=GPIO.PWM(self.en2,1000)

    def set_speed(self, motor, direction = "forward", speed = 0):
        """
        Set speed and direction for selected motor

        :param motor:  Either 0 or 1 to select motor
        :param direction: "forward" or "reverse"
        :param speed: 0-100%
        
        """

        if speed < 0 or speed > 100:
            raise Exception("Invalid speed")

        if motor == 0:
            self.p1.start(0)
            if direction == "forward":
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif direction == "reverse":
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
            else:
                raise Exception("Invalid direction")
            self.p1.ChangeDutyCycle(speed)
        elif motor == 1:
            self.p2.start(0)
            if direction == "forward":
                GPIO.output(self.in3,GPIO.HIGH)
                GPIO.output(self.in4,GPIO.LOW)
            elif direction == "reverse":
                GPIO.output(self.in3,GPIO.LOW)
                GPIO.output(self.in4,GPIO.HIGH)
            else:
                raise Exception("Invalid direction")
            self.p2.ChangeDutyCycle(speed)
        else:
            raise Exception("Invalid motor selected")
        
    def stop_motor(self, motor):
        if motor == 0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)
            self.p1.stop()
        elif motor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)
            self.p2.stop()
        else:
            raise Exception("Invalid motor selected")