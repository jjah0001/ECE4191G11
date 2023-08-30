#!/usr/bin/env python3
import sys
sys.path.insert(1, '/home/rpi-team11/ECE4191G11/ROS/src/robot_controller/robot_controller/path_planning_files/')
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS/src/robot_controller/robot_controller/path_planning_files/')

import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Distances
from .map import Map
from bit import BITStar
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor




class PathPlanner(Node):
    def __init__(self):
        super().__init__("path_planner_node") # name of the node in ros2
        self.get_logger().info("Path Planner Node initialised")


        callback_group_manual = MutuallyExclusiveCallbackGroup()
        self.manual_waypoint_subscriber = self.create_subscription(Waypoint, "manual_waypoint", self.manual_waypoint_callback, 10, callback_group= callback_group_manual)
        
        self.waypoint_publisher = self.create_publisher(Waypoint, "desired_waypoint", 10) # msg type, topic_name to publish to, buffer size

        callback_group_pose = MutuallyExclusiveCallbackGroup()
        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10, callback_group= callback_group_pose) 
        # msg type, topic_name to subscribe to, callback func, buffer size

        callback_group_ultrasonic = MutuallyExclusiveCallbackGroup()
        self.ultrasonic_subscriber = self.create_subscription(Distances, "ultrasonic_distances", self.ultrasonic_callback, 10, callback=callback_group_ultrasonic)

        self.robot_pose = [50, 50, 0]
        self.goal_a = [500, 500]

        self.map = Map()
        # self.map.add_obs_cirlce(250, 250, 100)
        self.path_updated = False
        self.path = []


        self.move_to_waypoint()


    def move_to_waypoint(self):
        self.get_logger().info("Move started")
        # self.path = self.recalculate_path()
        
        # while len(self.path) > 0:
        #     waypoint_x = self.path[0][0]
        #     waypoint_y = self.path[0][1]
        #     self.get_logger().info("Current waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
        #     self.get_logger().info("Current robot pose: (" + str(self.robot_pose[0]) + ", " + str(self.robot_pose[1]) +")")
        #     # tell the robot to move to some waypoint
            
        #     reached_waypoint = abs(self.robot_pose[0] - waypoint_x) < 5 and abs(self.robot_pose[1] - waypoint_x) < 5

        #     if reached_waypoint:
        #         self.get_logger().info("Reached waypoint: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
        #         self.path.pop(0)

        #         if len(self.path) > 0:
        #             waypoint_x = self.path[0][0]
        #             waypoint_y = self.path[0][1]
        #             msg = Waypoint()
        #             msg.x = float(waypoint_x)
        #             msg.y = float(waypoint_y)
        #             # self.publish_desired_waypoint(msg.x, msg.y)
        #             self.get_logger().info("Published waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
        #         else:
        #             break

        #     if self.path_updated:
        #         self.path = self.recalculate_path()
        

    def manual_waypoint_callback(self, msg:Waypoint):
        if abs(self.robot_pose[0] - msg.x) > 0.05 or abs(self.robot_pose[1] - msg.y) > 0.05:
            self.publish_desired_waypoint(msg.x, msg.y)

    def publish_desired_waypoint(self, x, y):
        msg = Waypoint()
        msg.x = float(x)
        msg.y = float(y)
        self.waypoint_publisher.publish(msg)

    def pose_callback(self, msg:Pose):
        self.get_logger().info("Recieved robot pose: [" + str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta) + "]" )
        self.robot_pose = [msg.x, msg.y, msg.theta]
    
    def ultrasonic_callback(self, msg:Distances):
        self.get_logger().info("Recieved ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        
        # if obs detected
            # calculate obs coord
            
            # add obs to map
            
            # self.map.add_obs_cirlce(x, y, r)
            # # recalc path
            # self.path_updated = True
    
    def recalculate_path(self):
        x_start = (self.robot_pose[0]/10, self.robot_pose[1]/10)  # Starting node
        x_goal = (self.goal_a[0]/10, self.goal_a[1]/10)  # Goal node
        eta = 2  # useless param it seems
        iter_max = 500

        self.get_logger().info(str(x_start[0]) + ", " + str(x_start[1]))
        self.get_logger().info(str(x_goal[0]) + ", " + str(x_goal[1]))

        bit = BITStar(x_start, x_goal, eta, iter_max, self.map)
        path = bit.planning(show_animation=False)
        path = [[x[0]*10, x[1]*10] for x in path]
        if path is not None:
            self.get_logger().info("new path planned")
        else:
            self.get_logger().info("could not find path")
        return path

def main(args=None):
    try:
        rclpy.init(args=args)

        path_planner_node = PathPlanner()

        executor = MultiThreadedExecutor()
        executor.add_node(path_planner_node)
        executor.spin()

    except KeyboardInterrupt:
        path_planner_node.get_logger().info("drive node shutdown")
    rclpy.shutdown()

if __name__ == "__main__": # If you want to run node from terminal directly
    main()
