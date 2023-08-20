'''
This code is mainly to test the motors and the ultrasonic and it would not be used for the actual run.
'''

from drive import Drive
import time
import RPi.GPIO as GPIO          
from ultrasonic import Ultrasonic

import logging

# Logging:
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

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

left_wheel_ena = 5
left_wheel_enb = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_wheel_ena, GPIO.IN)
GPIO.setup(left_wheel_enb, GPIO.IN)

def drive(speed, distance):
    controller = Drive()
    controller.drive_forwards(speed)

    # 170mm per revolution, per 3600 count
    WHEEL_CIRCUMFERENCE = 169
    COUNTS_PER_REV = 3600
    total_count = 0
    deg = 0
    count_required = (distance/WHEEL_CIRCUMFERENCE)*COUNTS_PER_REV
    input_a = 0
    input_b = 0

    logging.info("To travel the specified distance, encoder needs to count " + str(count_required) + " times.")

    while total_count < count_required:
        if GPIO.input(left_wheel_ena) != input_a or GPIO.input(left_wheel_enb) != input_b:
            input_a = GPIO.input(left_wheel_ena)
            input_b = GPIO.input(left_wheel_enb)

            total_count += 1
            deg = total_count/10
            
            distance_travelled = total_count*(WHEEL_CIRCUMFERENCE/COUNTS_PER_REV)
            logging.info("Robot has travelled " + str(deg) + " degrees and a distance of " + str(distance_travelled) + " mm.")
    controller.stop()
    controller.clear_gpio()

ultrasonic_1 = Ultrasonic()

while True:
    logging.info("Distance: " + str(ultrasonic_1.get_distance()))
    time.sleep(0.01)






