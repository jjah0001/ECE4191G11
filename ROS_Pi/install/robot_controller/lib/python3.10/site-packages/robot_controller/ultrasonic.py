#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO          
import time
from robot_interfaces.msg import Distances
from robot_interfaces.msg import Obstacles
from robot_interfaces.msg import Pose
import sys
sys.path.insert(1, '/home/rpi-team11/ECE4191G11/ROS_Pi/src/robot_controller/robot_controller')
from map_bit import Map
from env import Env
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
import numpy as np
from rclpy.executors import MultiThreadedExecutor


class Ultrasonic(Node):
    def __init__(self):
        super().__init__("ultrasonic_node") # name of the node in ros2
        
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #set GPIO Pins
        self.GPIO_TRIGGER = 27
        self.GPIO_ECHO = 17
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        self.GPIO_TRIGGER_2 = 2
        self.GPIO_ECHO_2 = 3

        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

        self.robot_pose = [300, 200, 90]

        self.mode = "BIT*"
        self.plotting = False
    
        if self.mode == "A*":
            map_size = [1200, 1200]
            self.scaling = 5
            self.map = Env()
            self.map.set_arena_size(map_size[0]//self.scaling, map_size[1]//self.scaling)

        elif self.mode == "BIT*":
            self.map = Map()

        self.obs_shape = "circle"
        self.obs_radius = 150

        callback_group_pose = MutuallyExclusiveCallbackGroup()
        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10, callback_group= callback_group_pose) 

        time.sleep(1)
        self.detect_timer = self.create_timer(0.2, self.detect_obstacles)
        # self.measure_publisher = self.create_publisher(Distances, "ultrasonic_distances", 10) # msg type, topic_name to publish to, buffer size

        self.obs_publisher = self.create_publisher(Obstacles, "obs_detected", 10)

        self.get_logger().info("Ultrasonic class initiallised")

    def detect_obstacles(self):
        msg = Distances()
        msg.sensor1 = float(self.get_distance(0)*10)
        time.sleep(0.01)
        msg.sensor2 = float(self.get_distance(1)*10)
        time.sleep(0.01)
        msg.sensor3 = float(self.get_distance(2)*10)
        # self.get_logger().info("hi")
        # self.get_logger().info("Publishing ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        # self.measure_publisher.publish(msg)

        obs, obs_flag = self.add_obs_from_ultrasonic(msg.sensor1, msg.sensor2)
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

            self.obs_publisher.publish(obstacles)


    def pose_callback(self, msg:Pose):
        # self.get_logger().info("Recieved robot pose: [" + str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta) + "]" )
        self.robot_pose = [msg.x, msg.y, msg.theta]

    def get_distance(self, sensor):
        if sensor == 0:
            trig = self.GPIO_TRIGGER
            echo = self. GPIO_ECHO
        elif sensor ==1:
            trig = self.GPIO_TRIGGER_2
            echo = self. GPIO_ECHO_2
        elif sensor == 2:
            return 0.0

        # set Trigger to HIGH
        GPIO.output(trig, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trig, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        no_echo = False
        # save StartTime
        start_start_time = StartTime
        while GPIO.input(echo) == 0:
            if time.time() - start_start_time > 0.2: 
                break
            StartTime = time.time()
    
        if not no_echo:
            # save time of arrival
            while GPIO.input(echo) == 1:
                StopTime = time.time()
    
    
        
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            # self.get_logger().info("time between emission and detection: " + str(TimeElapsed))
            distance = (TimeElapsed * 34300) / 2
            # self.get_logger().info("distance recorded: " + str(distance))
            if distance >= 200:
                return -999.0
            return distance
        else:
            return -999.0

    
    def get_average_distance(self, sensor):
        distance_array = []
        for i in range(3):
            dist = self.get_distance(sensor)

            if dist > 0 and dist < 200:
                distance_array.append(dist)
            
            length = len(distance_array)
            if length == 0:
                return 0
            else:
                return sum(distance_array)/length

    
    def add_obs_from_ultrasonic(self, dist1, dist2, dist3=None):
        obs_added = False
        obs = [[],[]]
        if dist1 is not None and dist1 >= 10 and dist1 <= 500:
            proj_x, proj_y = self.project_coords(0, self.robot_pose, dist1)
            if self.no_overlaps([proj_x, proj_y, self.obs_radius], self.map.obs_circle, 100):
                self.get_logger().info("Obs added: (" + str(proj_x) + ", " + str(proj_y) + ")")
                self.add_obs(proj_x, proj_y, self.obs_radius)
                obs_added = True
                obs[0] = [proj_x, proj_y, self.obs_radius]

        if dist2 is not None and dist2 >= 10 and dist2 <= 500:
            proj_x, proj_y = self.project_coords(1, self.robot_pose, dist2)
            if self.no_overlaps([proj_x, proj_y, self.obs_radius], self.map.obs_circle, 100):
                self.get_logger().info("Obs added: (" + str(proj_x) + ", " + str(proj_y) + ")")
                self.add_obs(proj_x, proj_y, self.obs_radius)
                obs_added = True
                obs[1] = [proj_x, proj_y, self.obs_radius]

        return obs, obs_added

    def add_obs(self, center_x, center_y, r_or_l):

        if self.mode == "A*":
            x = max(center_x//self.scaling, 1)
            y = max(center_y//self.scaling, 1)
            w = max(r_or_l//self.scaling, 1)
            self.map.add_square_obs(x, y, w)
        elif self.mode == "BIT*":
            
            self.map.add_obs_cirlce(center_x, center_y, r_or_l)
    
    def project_coords(self, sensor, pose, dist):
        if sensor == 0:
            sensor_x = 65
            sensor_y = 140
            sensor_angle = np.arctan(sensor_x/sensor_y)*180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] + sensor_angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)
        elif sensor == 1:
            sensor_x = 65
            sensor_y = 140
            sensor_angle = np.arctan(sensor_x/sensor_y) *180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] - sensor_angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)


        proj_x = x + dist*np.cos(pose[2]*np.pi/180)
        proj_y = y + dist*np.sin(pose[2]*np.pi/180)
        return proj_x, proj_y
    
    def no_overlaps(self, circle1, circle_list, dist_threshold=100):
        center_x1, center_y1, radius1 = circle1
        
        # check if outside of the walls/ is the wall
        if center_x1 <= 50 or center_x1 >= 1050 or  center_y1 <= 50 or center_y1 >= 1050:
            return False
        
        for circle2 in circle_list:
            center_x2, center_y2, radius2 = circle2
            center_x2, center_y2, radius2 = center_x2*10, center_y2*10, radius2*10 # convert to mm
            
            # Calculate the distance between the centers of the two circles
            distance = np.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)
            
            # Check if the circles overlap significantly
            if distance < dist_threshold:
                return False
        
        # No significant overlap found
        return True


def main(args=None):
    try:
        rclpy.init(args=args)
        ultrasonic_node = Ultrasonic()

        executor = MultiThreadedExecutor()
        executor.add_node(ultrasonic_node)
        executor.spin()

    except KeyboardInterrupt:
        ultrasonic_node.get_logger().info("ultrasonic node shutdown")
    rclpy.shutdown()


if __name__ == "__main__": # If you want to run node from terminal directly
    main()
