import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import time
import matplotlib.pyplot as plt

import sys
sys.path.insert(1, '/home/rpi-team11/ECE4191G11/ROS_Pi/src/robot_controller/robot_controller')

from robot_interfaces.msg import EncoderInfo
from robot_interfaces.msg import Flag
from pid_controller import Controller

class Encoder(Node):
    def __init__(self):
        super().__init__("encoder_node")
        # encoder state and counts
        self.left_count = 0
        self.right_count = 0
        self.left_state = [0, 0]
        self.right_state = [0, 0]

        # GPIO set up
        GPIO.setmode(GPIO.BCM)
        self.left_wheel_ena = 5
        self.left_wheel_enb = 6
        GPIO.setup(self.left_wheel_ena, GPIO.IN)
        GPIO.setup(self.left_wheel_enb, GPIO.IN)


        self.right_wheel_ena = 16
        self.right_wheel_enb = 26
        GPIO.setup(self.right_wheel_ena, GPIO.IN)
        GPIO.setup(self.right_wheel_enb, GPIO.IN)

        ############################################## INITIALISATION: PID Controller #########################
        self.pid = Controller(init_speed=60)

        #PID control vars
        self.target_speed_arr = []
        self.target_cps = 0
        self.left_speed_arr = []
        self.right_speed_arr = []
        self.pid_enabled = False
        self.reset_time = True

        self.encoder_publisher = self.create_publisher(EncoderInfo, "encoder_info", 10)

        callback_group_pid = MutuallyExclusiveCallbackGroup()
        self.pid_subscriber = self.create_subscription(Flag, "pid_flag", self.pid_callback, 10, callback_group=callback_group_pid)

        callback_group_main = MutuallyExclusiveCallbackGroup()
        self.init_timer = self.create_timer(1, self.update_encoder_loop, callback_group=callback_group_main)

    def pid_callback(self, msg:Flag):
        self.pid_enabled = msg.flag
        self.reset_time = True
        self.pid.reset_error()
        self.get_logger().info(f"pid enabled: {self.pid_enabled}")


    def update_encoder_loop(self):
        self.init_timer.cancel()
        """
        Method that indefinately updates encoder counts
        """
        # pid vars
        self.reset_time = True
        set_speed = True
        self.pid.reset_error()

        while True:

            ## Encode state loop
            state_changed = False
            # check encoder
            lp1 = GPIO.input(self.left_wheel_ena)
            lp2 = GPIO.input(self.left_wheel_enb)

            if self.left_state[0] != lp1 or self.left_state[1] != lp2:
                self.left_count += 1
                self.left_state = [lp1, lp2]
                state_changed = True

            rp1 = GPIO.input(self.right_wheel_ena)
            rp2 = GPIO.input(self.right_wheel_enb)

            if self.right_state[0] != rp1 or self.right_state[1] != rp2:
                self.right_count += 1
                self.right_state = [rp1, rp2]
                state_changed = True
            
            if self.left_count %1000 ==0 and self.left_count > 100:
                print(self.left_count, self.right_count)
            
            #self.get_logger().info(f"left count: {self.left_count}, right count: {self.right_count}")
            
            if state_changed:
                msg = EncoderInfo()
                msg.left_count = int(self.left_count)
                msg.right_count = int(self.right_count)
                self.encoder_publisher.publish(msg)
            
            if self.pid_enabled:
                # PID speed control
                if self.reset_time:
                    start_time = time.perf_counter()
                    self.reset_time = False
                    prev_left_count = self.left_count 
                    prev_right_count = self.right_count
                    
                elapsed_time = time.perf_counter() - start_time 
                
                if elapsed_time >= 0.1:
                    left_vel = (self.left_count - prev_left_count)/elapsed_time #vel in cps, counts per sec
                    right_vel = (self.right_count - prev_right_count)/elapsed_time
                    self.left_speed_arr.append(left_vel)
                    self.right_speed_arr.append(right_vel)

                    if set_speed:
                        set_speed = self.set_target_speed(left_vel, right_vel)
                    else:
                        self.pid_control(left_vel, right_vel)
                    self.reset_time = True
    
    def set_target_speed(self, left_vel, right_vel):
        """
        Method to set the PID target speed to current average speed
        """
        avg_vel = (left_vel + right_vel)/2

        if len(self.target_speed_arr) < 3:
            self.target_speed_arr.append(avg_vel)
        else:
            self.target_speed_arr.pop(0)
            self.target_speed_arr.append(avg_vel)
        
        if avg_vel > 1000 and all([abs(x - self.target_speed_arr[0]) <100 for x in self.target_speed_arr] ):
            self.target_cps = sum(self.target_speed_arr)/len(self.target_speed_arr)
            self.get_logger().info(f"target cps: {self.target_cps}")
            return False

        return True
    
    def pid_control(self, left_vel, right_vel):
        """
        Method for calculating error and applying PID control to reach target speed
        """
        try:
            error_left = 100 * (self.target_cps- left_vel)/self.target_cps
        except ZeroDivisionError:
            error_left = 0
        try:
            error_right = 100 * (self.target_cps - right_vel)/self.target_cps
        except ZeroDivisionError:
            error_right = 0

        if abs(error_left) >= 1 and abs(error_left) < 50:
            self.pid.correct_speed("left", error_left)

        if abs(error_right) >= 1 and abs(error_right) < 50:
            self.pid.correct_speed("right", error_right)

    def save_speed_graphs(self):
        """
        Method to save the speed logs as a graph
        """
        plt.figure()
        plt.plot(self.left_speed_arr)
        plt.legend(["left"])
        plt.savefig('left_encoder.png')
        plt.close()
        plt.figure()
        plt.plot(self.right_speed_arr)
        plt.legend(["right"])
        plt.savefig("right_encoder.png")
        plt.close()

    def reset_encoder_counts(self):
        """
        Method to reset encoder counts
        """
        self.left_count = 0
        self.right_count = 0

def main(args=None):
    try:
        rclpy.init(args=args)
        encoder_node = Encoder()

        executor = MultiThreadedExecutor()
        executor.add_node(encoder_node)
        executor.spin()

    except KeyboardInterrupt:
        encoder_node.get_logger().info("encoder node shutdown")
    rclpy.shutdown()


if __name__ == "__main__":
    main()