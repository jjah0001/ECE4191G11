import RPi.GPIO as GPIO          
from time import sleep
import logging
import time

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

    def _set_speed(self, motor, direction, speed):
        """
        Set speed and direction for selected motor

        :param motor:  Either 0 or 1 to select motor
        :param direction: "forward" or "reverse"
        :param speed: 0-100%
        
        """

        if speed < 0 or speed > 100:
            raise Exception("Invalid speed")

        if motor == 0:
            if direction == "forward":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(speed)
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif direction == "reverse":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(speed)
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
            else:
                raise Exception("Invalid direction")
            
        elif motor == 1:
            if direction == "forward":
                self.p2.start(0)
                self.p2.ChangeDutyCycle(speed)
                GPIO.output(self.in3,GPIO.HIGH)
                GPIO.output(self.in4,GPIO.LOW)
            elif direction == "reverse":
                self.p2.start(0)
                self.p2.ChangeDutyCycle(speed)
                GPIO.output(self.in3,GPIO.LOW)
                GPIO.output(self.in4,GPIO.HIGH)
            else:
                raise Exception("Invalid direction")
            
        else:
            raise Exception("Invalid motor selected")
        
    def _stop_motor(self, motor):
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
    
    def rotate(self, direction, speed):
        """
        Rotate at a specified speed in either direction
        :param direction: "CW" or "CCW"
        :param speed: 0-100%
        """
        if speed < 0 or speed > 100:
            raise Exception("Invalid speed")
        
        if direction == "CW":
            self._set_speed(0, "forward", speed)
            self._set_speed(1, "reverse", speed)
        elif direction == "CCW":
            self._set_speed(0, "reverse", speed)
            self._set_speed(1, "forward", speed)
        else:
            raise Exception("Invalid direction")
        
    def drive_forwards(self, speed, duration=None):
        """
        Drive forwards at a specified speed. If duration is given, stops after a certain time
        
        """
        if speed < 0 or speed > 100:
            raise Exception("Invalid speed")
        
        self._set_speed(0, "forward", speed)
        self._set_speed(1, "forward", speed)

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float)
                time.sleep(duration)
                self._stop_motor(0)
                self._stop_motor(1)
            else:
                raise Exception("Invalid duration")
        
    def drive_backwards(self, speed, duration=None):
        if speed < 0 or speed > 100:
            raise Exception("Invalid speed")
        
        self._set_speed(0, "reverse", speed)
        self._set_speed(1, "reverse", speed)

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float)
                time.sleep(duration)
                self._stop_motor(0)
                self._stop_motor(1)
            else:
                raise Exception("Invalid duration")
    
    def drive_distance(self, distance):
        """
        Calibrate this to find the correct time + speed % = what distance

        distance = vel * time, calibrate what speed % = what velocity?        
        
        """

        pass
