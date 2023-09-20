#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

import RPi.GPIO as GPIO          
import time
from robot_interfaces.msg import Pose
from robot_interfaces.msg import DesState
from robot_interfaces.msg import EncoderInfo
from robot_interfaces.msg import Obstacles
from robot_interfaces.msg import Distances
from robot_interfaces.msg import QRData
import numpy as np
import sys
sys.path.insert(1, '/home/rpi-team11/ECE4191G11/ROS_Pi/src/robot_controller/robot_controller')


from camera import Camera
from ultrasonic import Ultrasonic
from motor import Motor

class Robot(Node):
    def __init__(self):
        super().__init__("robot_node")

        ############################################## INITIALISATION: MOTORS #########################
        self.motors = Motor()

        ############################################## INITIALISATION: ULTRASONIC #########################
        self.ultrasonics = Ultrasonic(mode="BIT*", obs_shape="circle", obs_radius=170)        

        ############################################ INITIALISATION: CAMERA #########################
        self.camera = Camera()

        ############################################ INITIALISATION: VARIABLES #######################


        # motor variables
        self.WHEEL_CIRCUMFERENCE = 55*np.pi
        self.WHEEL_BASELINE = 183
        self.COUNTS_PER_REV = 3592


        # path planning variables
        self.target_waypoint = [0, 0]
        self.pose = [300, 200, 90]
        self.prev_waypoint = [self.pose[0], self.pose[1]]



        ########## PARAMS INFO
        # 0 deg pose = pointing in the positive x-direction. pose angle increases when going counter clockwise.
        # 90 deg pose = pointing in the positive y-direction
        # Bottom left of arena = (0,0), moving up towards bin = +y, moving left along loading zone = +x
        # x and y will be in units of mm

        # motor 0 = right motor, motor 1 = left motor


        ############################################ INITIALISATION: CALLBACKS #######################

        callback_group_encoder = MutuallyExclusiveCallbackGroup()
        callback_group_pose = MutuallyExclusiveCallbackGroup()
        callback_group_drive = ReentrantCallbackGroup()

        self.pose_timer = self.create_timer(0.05, self.publish_estimated_pose, callback_group=callback_group_pose)
        self.pose_publisher = self.create_publisher(Pose, "estimated_pose", 10) # msg type, topic_name to publish to, buffer size

        
        self.des_state_subscriber = self.create_subscription(DesState, "des_state", self.des_state_callback, 10, callback_group= callback_group_drive)
        self.encoder_subscriber = self.create_subscription(EncoderInfo, "encoder_info", self.encoder_callback, 10, callback_group=callback_group_encoder)

        callback_group_detect = MutuallyExclusiveCallbackGroup()
        self.detect_timer = self.create_timer(0.2, self.detect_obstacles, callback_group=callback_group_detect)
        self.detect_timer.cancel()
        # self.measure_publisher = self.create_publisher(Distances, "ultrasonic_distances", 10) # msg type, topic_name to publish to, buffer size

        self.obs_publisher = self.create_publisher(Obstacles, "obs_detected", 10)

        self.qr_publisher = self.create_publisher(QRData, "qr_data", 10)

        self.get_logger().info('Robot node initialised')

    def publish_estimated_pose(self):
        
        msg = Pose()
        msg.x = float(self.pose[0])
        msg.y = float(self.pose[1])
        msg.theta = float(self.pose[2])
        # self.get_logger().info("Publishing estimated pose: (" + str(msg.x) + ", " + str(msg.y) + ", " + str(msg.theta) + ")")
        self.pose_publisher.publish(msg)

    def des_state_callback(self, msg:DesState):
        if msg.state == 0:
            goal = self.read_qr()
            qr_msg = QRData()
            qr_msg.data = goal
            self.qr_publisher.publish(qr_msg)

        elif msg.state == 1:
            self.stop()
            self.target_waypoint[0] = msg.x
            self.target_waypoint[1] = msg.y
            
            self.get_logger().info("Recieved command to move to coordinates: (" + str(msg.x) + ", " + str(msg.y) + ")")

            try:
                if abs(self.pose[0] - msg.x) > 0.05 or abs(self.pose[1] - msg.y) > 0.05:
                    self.detect_timer.reset()
                    time.sleep(0.1)
                    self.obs_detected = False
                    self.motors.drive_to_waypoint(waypoint = [msg.x, msg.y])

                    # assume that we reach the coorect coord after movement??? remove this if robot becomes more accurate
                    self.pose[0] = msg.x
                    self.pose[1] = msg.y

                    self.detect_timer.cancel()
                    self.get_logger().info("Final Robot pose (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )
                    self.get_logger().info("Encoder counts: [" + str(self.left_encoder_count) + ", " + str(self.right_encoder_count) + "]" )
                else:
                    self.get_logger().info("Robot not moved (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )
            except:
                self.detect_timer.cancel()
                return

    def read_qr(self):
        self.detect_timer.cancel()
        return self.camera.read_qr()

    def detect_obstacles(self):
        dist1, dist2, dist3 = self.ultrasonics.get_distances()

        # self.get_logger().info("Publishing ultrasonic distances: ( Sensor 1: " + str(dist1) + ", Sensor 2: " + str(dist2) + ", Sensor 3: " + str(dist3) + ")")

        obs, obs_flag = self.ultrasonics.add_obs_from_ultrasonic(dist1, dist2, dist3)

        if obs_flag:
            self.get_logger().info("Obstacle detected")
            obstacles = Obstacles()
            obstacles.flag = True
            
            if len(obs[0]) > 0:
                obstacles.obs1_x = float(obs[0][0])
                obstacles.obs1_y = float(obs[0][1])
                obstacles.obs1_r = float(obs[0][2])
            else:
                obstacles.obs1_x = -1.0
                obstacles.obs1_y = -1.0
                obstacles.obs1_r = -1.0

            if len(obs[1]) > 0:
                obstacles.obs2_x = float(obs[1][0])
                obstacles.obs2_y = float(obs[1][1])
                obstacles.obs2_r = float(obs[1][2])
            else:
                obstacles.obs2_x = -1.0
                obstacles.obs2_y = -1.0
                obstacles.obs2_r = -1.0
            
            if len(obs[2]) > 0:
                obstacles.obs3_x = float(obs[2][0])
                obstacles.obs3_y = float(obs[2][1])
                obstacles.obs3_r = float(obs[2][2])
            else:
                obstacles.obs3_x = -1.0
                obstacles.obs3_y = -1.0
                obstacles.obs3_r = -1.0

            self.obs_publisher.publish(obstacles)


    def encoder_callback(self, msg:EncoderInfo):
        self.left_encoder_count = msg.left_count
        self.right_encoder_count = msg.right_count
        # self.get_logger().info("COUNT: (" + str(msg.left_count) + ", " + str(msg.right_count) + ")")


    def clear_gpio(self): 
        GPIO.cleanup()



def main(args=None):
    try:
        rclpy.init(args=args)
        robot_node = Robot()

        executor = MultiThreadedExecutor()
        executor.add_node(robot_node)
        executor.spin()

    except KeyboardInterrupt:
        robot_node.clear_gpio()
        robot_node.get_logger().info("drive node shutdown")
        robot_node.cap.release()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
