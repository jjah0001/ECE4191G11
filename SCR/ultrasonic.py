import RPi.GPIO as GPIO          
from time import sleep
import logging
import time

class Ultrasonic():
    def __init__(self):

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
        logging.info("Ultrasonic would return distance")
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
        logging.info("time between emission and detection: " + TimeElapsed)
        distance = (TimeElapsed * 34300) / 2
        logging.info("distance recorded: " + TimeElapsed)
    
        return distance
    
    def test_continuous_reading(self):
        logging.info("Ultrasonic would return distance continuously")
        try:
            while True:
                dist = self.get_distance()
                logging.info("Measured Distance =" + str(dist) +" cm")
                time.sleep(0.1)
            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            logging.warning("Measurement stopped by User")
            GPIO.cleanup()