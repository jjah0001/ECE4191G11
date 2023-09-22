#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

import RPi.GPIO as GPIO          
import time
import matplotlib.pyplot as plt
from robot_interfaces.msg import Pose
from robot_interfaces.msg import DesState
from robot_interfaces.msg import Obstacles
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
        self.target_speed_arr = []
        self.target_cps = 0
        self.left_speed_arr = []
        self.right_speed_arr = []

        # motor variables
        self.WHEEL_CIRCUMFERENCE = 55*np.pi
        self.WHEEL_BASELINE = 183
        self.COUNTS_PER_REV = 3592

        ############################################## INITIALISATION: ULTRASONIC #########################
        self.ultrasonics = Ultrasonic(mode="BIT*", obs_shape="circle", obs_radius=170)      
        self.obs_detected = False  

        ############################################ INITIALISATION: CAMERA #########################
        self.camera = Camera()

        ############################################ INITIALISATION: VARIABLES #######################


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
        # Using ros2 callback groups to perform multithreading
        
        callback_group_encoder = MutuallyExclusiveCallbackGroup()
        # The encoder callback group:
        #   - contains loop for updating encoder, (code should be kept as small as possible to ensure encoder accuracy)
        self.encoder_init_timer = self.create_timer(1, self.main_loop, callback_group=callback_group_encoder)


        callback_group_main = ReentrantCallbackGroup()
        # The drive callback group:
        #   - activates whenever a desired waypoint is recieved turns the motors on until waypiont is reached
        #   - command can be overwritten by new desired waypoint. (new path, obs detected etc)
        #   - should contain PID for motor speed and position, (because we know when robot is driving/when idle)
        self.state_subscriber = self.create_subscription(DesState, "des_state", self.main_callback, 10, callback_group= callback_group_main)

        callback_group_pose = MutuallyExclusiveCallbackGroup()
        # Callback group for constantly publishing robot pose.
        #  (can be optimised to only publish pose when path changed, or waypoint reached)

        # self.pose_timer = self.create_timer(0.05, self.publish_estimated_pose, callback_group=callback_group_pose)
        self.pose_publisher = self.create_publisher(Pose, "estimated_pose", 10) # msg type, topic_name to publish to, buffer size


        callback_group_detect = MutuallyExclusiveCallbackGroup()
        # Callback group for detecting obstacles
        # can possibly be merged with pose publisher if we no longer publish pose frequently
        self.detect_timer = self.create_timer(0.2, self.detect_obstacles, callback_group=callback_group_detect)
        self.detect_timer.cancel()

        # Other publishers
        self.obs_publisher = self.create_publisher(Obstacles, "obs_detected", 10)
        self.qr_publisher = self.create_publisher(QRData, "qr_data", 10)

        self.get_logger().info('Robot node initialised')


    ## Publishing methods:
    def publish_estimated_pose(self):
        """
        publishes current pose to the topic: "estimated pose"
        """    
        msg = Pose()
        msg.x = float(self.pose[0])
        msg.y = float(self.pose[1])
        msg.theta = float(self.pose[2])
        # self.get_logger().info("Publishing estimated pose: (" + str(msg.x) + ", " + str(msg.y) + ", " + str(msg.theta) + ")")
        self.pose_publisher.publish(msg)
    
    def publish_qr(self, qr_data):
        """
        publishes detected qr code to topic: "qr_data"
        """
        qr_msg = QRData()
        qr_msg.data = qr_data
        self.qr_publisher.publish(qr_msg)

    def publish_obs(self, obs):
        """
        publishes the detected obstacles from the 3 ultrasonic sensors to: "obs_detected"        
        """
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

    ## Threading Callbacks:
    def init_encoders(self):
        """
        Intialised by the ros timer, this function intialises the multithreaded infinite update encoder loop
        """
        self.encoder_init_timer.cancel()
        self.motors.encoders.update_encoder_loop()
    
    def detect_obstacles(self):
        """
        Method that gets the distances from ultrasonic sensors, then checks whether an obs is detected
        """
        dist1, dist2, dist3 = self.ultrasonics.get_distances()

        # self.get_logger().info("Publishing ultrasonic distances: ( Sensor 1: " + str(dist1) + ", Sensor 2: " + str(dist2) + ", Sensor 3: " + str(dist3) + ")")

        obs, obs_flag = self.ultrasonics.add_obs_from_ultrasonic(dist1, dist2, dist3)

        if obs_flag:
            self.obs_detected = True
            self.get_logger().info("Obstacle detected")
            self.publish_obs(obs)


    def main_callback(self, msg:DesState):
        """
        Main callback that controls robot action based on recieved state
        
        """
        if msg.state == 0:  # If the desired state is: reading qr code
            self.detect_timer.cancel()
            goal = self.read_qr()
            self.publish_qr(goal)

        elif msg.state == 1: # If the desired state is: moving to a waypoint
            self.motors.stop()
            self.target_waypoint[0] = msg.x
            self.target_waypoint[1] = msg.y
            
            self.get_logger().info("Recieved command to move to coordinates: (" + str(msg.x) + ", " + str(msg.y) + ")")

            try:
                if abs(self.pose[0] - msg.x) > 0.05 or abs(self.pose[1] - msg.y) > 0.05:
                    self.detect_timer.reset()
                    time.sleep(0.1)
                    self.obs_detected = False
                    self.drive_to_waypoint(waypoint = [msg.x, msg.y])

                    # assume that we reach the coorect coord after movement??? remove this if robot becomes more accurate
                    self.pose[0] = msg.x
                    self.pose[1] = msg.y
                    self.publish_estimated_pose()

                    self.detect_timer.cancel()
                    self.get_logger().info("Final Robot pose (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )
                    self.get_logger().info("Encoder counts: [" + str(self.motors.encoders.left_count) + ", " + str(self.motors.encoders.right_count) + "]" )
                else:
                    self.get_logger().info("Robot not moved (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )
            except:
                self.detect_timer.cancel()
                self.get_logger().info("obstacle detected or target waypoint changed")
                self.publish_estimated_pose()
                return


    ## Auxiliary Methods
    def read_qr(self): 
        """
        Method to continuously read from camera until qr code if scanned
        """
        return self.camera.read_qr()
            

    def drive_distance(self, distance):
        """
        Drives a distance specified in milimetres 
        
        """

        current_target_waypoint = [0, 0]
        current_target_waypoint[0], current_target_waypoint[1] = self.target_waypoint

        # 170mm per revolution, per 3600 count
        DISTANCE_PER_COUNT = self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV
        original_pose = [0, 0, 0]
        original_pose[0], original_pose[1], original_pose[2] = self.pose #have to do it this way to hard copy arr

        total_count = 0
        count_required = (distance/self.WHEEL_CIRCUMFERENCE)*self.COUNTS_PER_REV

        # self.get_logger().info("To travel the specified distance, encoder needs to count " + str(count_required) + " times.")

        # pid vars
        reset_time = True
        set_speed = True
        self.target_speed_arr = []
        self.target_cps = 0
        self.motors.encoders.reset_error()
        self.motors.encoders.reset_encoder_counts()

        # move loop
        self.motors.drive_forwards()
        while total_count < count_required:
            # Check if target waypoint changed
            if self.obs_detected or self.target_waypoint[0] != current_target_waypoint[0] or self.target_waypoint[1] != current_target_waypoint[1]:
                self.motors.stop()
                raise Exception("target waypoint changed")

            # calculate pose
            left_count = self.motors.encoders.left_count
            right_count = self.motors.encoders.right_count
            total_count = (left_count + right_count)//2
            self.pose[0] = original_pose[0] + DISTANCE_PER_COUNT * np.cos(self.pose[2] * (np.pi/180)) * total_count
            self.pose[1] = original_pose[1] + DISTANCE_PER_COUNT * np.sin(self.pose[2] * (np.pi/180)) * total_count
            
            # PID speed control
            if reset_time:
                start_time = time.perf_counter()
                reset_time = False
                prev_left_count = self.motors.encoders.left_count
                prev_right_count = self.motors.encoders.right_count
                   
            elapsed_time = time.perf_counter() - start_time 
            
            if elapsed_time >= 0.1:
                left_vel = (self.motors.encoders.left_count - prev_left_count)/elapsed_time #vel in cps, counts per sec
                right_vel = (self.motors.encoders.right_count - prev_right_count)/elapsed_time
                self.left_speed_arr.append(left_vel)
                self.right_speed_arr.append(right_vel)

                if set_speed:
                    set_speed = self.set_target_speed(left_vel, right_vel)
                else:
                    self.pid_control(left_vel, right_vel)
                reset_time = True

        distance_travelled = total_count*(self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)
        self.motors.stop()
        # self.get_logger().info("Robot wheel has rotated " + str(deg) + " degrees and travelled a distance of " + str(distance_travelled) + " mm.")

    def rotate_angle(self, angle):
        """
        rotates a specified angle in degrees
        
        """

        current_target_waypoint = [0, 0]
        current_target_waypoint[0], current_target_waypoint[1] = self.target_waypoint


        MM_PER_DEG = self.WHEEL_BASELINE*np.pi / 360
        ANGLE_PER_COUNT = (self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)/MM_PER_DEG

        original_pose = [0, 0, 0]
        original_pose[0], original_pose[1], original_pose[2] = self.pose #have to do it this way to hard copy arr

        total_count = 0
        count_required = ((abs(angle) * MM_PER_DEG)/self.WHEEL_CIRCUMFERENCE) * self.COUNTS_PER_REV

        # self.get_logger().info("To rotate the specified angle, encoder needs to count " + str(count_required) + " times.")


        # pid vars
        reset_time = True
        set_speed = True
        self.target_speed_arr = []
        self.target_cps = 0
        self.motors.encoders.reset_error()
        self.motors.encoders.reset_encoder_counts()

        # moving loop
        if angle > 0:
            self.motors.rotate("CCW")
        elif angle < 0:
            self.motors.rotate("CW")

        while total_count < count_required:        
            # Check if waypoint has changed
            if self.obs_detected or self.target_waypoint[0] != current_target_waypoint[0] or self.target_waypoint[1] != current_target_waypoint[1]:
                self.motors.stop()
                raise Exception("target waypoint changed")
            
            # calculate pose
            left_count = self.motors.encoders.left_count
            right_count = self.motors.encoders.right_count
            total_count = (left_count + right_count)//2
            self.pose[2] = original_pose[2] + ANGLE_PER_COUNT* np.sign(angle) * total_count
            
            # PID speed control
            if reset_time:
                start_time = time.perf_counter()
                reset_time = False
                prev_left_count = self.motors.encoders.left_count
                prev_right_count = self.motors.encoders.right_count
                   
            elapsed_time = time.perf_counter() - start_time 
            
            if elapsed_time >= 0.1:
                left_vel = (self.motors.encoders.left_count - prev_left_count)/elapsed_time #vel in cps, counts per sec
                right_vel = (self.motors.encoders.right_count - prev_right_count)/elapsed_time
                self.left_speed_arr.append(left_vel)
                self.right_speed_arr.append(right_vel)

                if set_speed:
                    set_speed = self.set_target_speed(left_vel, right_vel)
                else:
                    self.pid_control(left_vel, right_vel)
                reset_time = True

        deg_rotated = total_count*ANGLE_PER_COUNT
        self.motors.stop()
        # self.get_logger().info("Robot has rotated an angle of " + str(deg_rotated) + " degs.")

    def drive_to_waypoint(self, waypoint):
        """
        drives towards a specified waypoint given in world coordinate frame.
        """

        # 0 deg pose = pointing in the positive x-direction. pose angle increases when going counter clockwise.
        # 90 deg pose = pointing in the positive y-direction
        # Bottom left of arena = (0,0), moving up towards bin = +y, moving left along loading zone = +x
        angle_to_rotate = self.motors.calculate_rotation(waypoint)
        distance_to_travel = self.motors.calculate_distance(waypoint)
        
        try:
            if abs(distance_to_travel) > 0.05:
                if abs(angle_to_rotate) > 0.05:
                    # code to rotate
                    self.get_logger().info("Recieved command to rotate by " + str(angle_to_rotate) + " degrees")
                    self.rotate_angle(angle_to_rotate)
                
                time.sleep(1.5)
                # code to drive
                self.get_logger().info("Recieved command to drive forward by " + str(distance_to_travel) + " mm")
                self.drive_distance(distance_to_travel)
        except:
            raise Exception("target waypoint changed")

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
            self.motors.encoders.correct_speed("left", error_left)

        if abs(error_right) >= 1 and abs(error_right) < 50:
            self.motors.encoders.correct_speed("right", error_right)

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

    def clear_gpio(self): 
        """
        Method to clear the GPIO pin assignments
        """
        GPIO.cleanup()




def main(args=None):
    try:
        rclpy.init(args=args)
        robot_node = Robot()

        executor = MultiThreadedExecutor()
        executor.add_node(robot_node)
        executor.spin()

    except KeyboardInterrupt:
        robot_node.save_speed_graphs()
        robot_node.clear_gpio()
        robot_node.cap.release()
        robot_node.get_logger().info("drive node shutdown")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
