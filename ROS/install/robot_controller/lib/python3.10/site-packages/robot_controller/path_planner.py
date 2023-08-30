#!/usr/bin/env python3
import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Distances
import RPi.GPIO as GPIO   

class PathPlanner(Node):
    def __init__(self):
        super().__init__("path_planner_node") # name of the node in ros2
        self.get_logger().info("Path Planner Node initialised")
        GPIO.cleanup()

        self.manual_waypoint_subscriber = self.create_subscription(Waypoint, "manual_waypoint", self.manual_waypoint_callback, 10)

        # self.waypoint_timer = self.create_timer(0.1, self.publish_desired_waypoint) 
        self.waypoint_publisher = self.create_publisher(Waypoint, "desired_waypoint", 10) # msg type, topic_name to publish to, buffer size

        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10) 
        # msg type, topic_name to subscribe to, callback func, buffer size

        self.ultrasonic_subscriber = self.create_subscription(Distances, "ultrasonic_distances", self.ultrasonic_callback, 10)

        self.robot_pose = [0, 0, 0]

    def manual_waypoint_callback(self, msg:Waypoint):
        if abs(self.robot_pose[0] - msg.x) > 0.05 or abs(self.robot_pose[1] - msg.y) > 0.05:
            self.publish_desired_waypoint(msg.x, msg.y)

    def publish_desired_waypoint(self, x, y):
        msg = Waypoint()
        msg.x = float(x)
        msg.y = float(y)
        self.waypoint_publisher.publish(msg)

    def pose_callback(self, msg:Pose):
        # self.get_logger().info("Recieved robot pose: [" + str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta) + "]" )
        self.robot_pose = [msg.x, msg.y, msg.theta]
    
    def ultrasonic_callback(self, msg:Distances):
        self.get_logger().info("Recieved ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        

def main(args=None):
    try:
        rclpy.init(args=args)

        path_planner_node = PathPlanner()
        rclpy.spin(path_planner_node)

    except KeyboardInterrupt:
        path_planner_node.get_logger().info("drive node shutdown")
    rclpy.shutdown()

if __name__ == "__main__": # If you want to run node from terminal directly
    main()
