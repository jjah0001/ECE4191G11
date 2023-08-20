import RPi.GPIO as GPIO          
from time import sleep
import logging
import time

class Ultrasonic():
    def __init__(self):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # Define the format for the log messages
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create a file handler
        self.file_handler = logging.FileHandler('../log/ultrasonic_test.log')
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.formatter)

        #    Add the handlers to the logger
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(console_handler)

        logging.info('Ultrasonic class initiallised')

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #set GPIO Pins
        self.GPIO_TRIGGER = 27
        self.GPIO_ECHO = 17
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)


    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    
    def test_continuous_reading(self):
        try:
            while True:
                dist = self.get_distance()
                logging.info("Measured Distance =" + str(dist) +" cm")
                time.sleep(0.1)
            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            logging.error("Measurement stopped by User")
            GPIO.cleanup()