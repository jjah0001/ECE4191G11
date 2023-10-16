import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

import sys
sys.path.insert(1, '/home/rpi-team11/ECE4191G11/ROS_Pi/src/robot_controller/robot_controller')

from pid_controller import Controller

class Encoder:
    def __init__(self):
        # encoder state and counts
        self.left_count = 0
        self.right_count = 0
        self.left_state = [0, 0]
        self.right_state = [0, 0]

        # GPIO set up
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.left_wheel_ena = 5
        self.left_wheel_enb = 6
        GPIO.setup(self.left_wheel_ena, GPIO.IN)
        GPIO.setup(self.left_wheel_enb, GPIO.IN)


        self.right_wheel_ena = 16
        self.right_wheel_enb = 26
        GPIO.setup(self.right_wheel_ena, GPIO.IN)
        GPIO.setup(self.right_wheel_enb, GPIO.IN)


    def update_encoder_loop(self, left_count, right_count):
        """
        Method that indefinately updates encoder counts
        """

        while True:

            ## Encode state loop
            # check encoder
            lp1 = GPIO.input(self.left_wheel_ena)
            lp2 = GPIO.input(self.left_wheel_enb)

            if self.left_state[0] != lp1 or self.left_state[1] != lp2:
                left_count.value += 1
                self.left_state = [lp1, lp2]

            rp1 = GPIO.input(self.right_wheel_ena)
            rp2 = GPIO.input(self.right_wheel_enb)

            if self.right_state[0] != rp1 or self.right_state[1] != rp2:
                right_count.value += 1
                self.right_state = [rp1, rp2]
            
            #self.get_logger().info(f"left count: {left_count}, right count: {right_count}")

    def reset_encoder_counts(self):
        """
        Method to reset encoder counts
        """
        self.left_count = 0
        self.right_count = 0
