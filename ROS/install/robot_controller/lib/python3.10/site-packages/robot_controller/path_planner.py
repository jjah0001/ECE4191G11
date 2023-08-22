#!/usr/bin/env python3
import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Distances

class PathPlanner(Node):
    def __init__(self):
        super().__init__("path_planner_node") # name of the node in ros2
        self.get_logger().info("Path Planner Node initialised")

        self.waypoint_timer = self.create_timer(0.1, self.publish_desired_waypoint)
        self.waypoint_publisher = self.create_publisher(Waypoint, "desired_waypoint", 10) # msg type, topic_name to publish to, buffer size

        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10) 
        # msg type, topic_name to subscribe to, callback func, buffer size

        self.ultrasonic_subscriber = self.create_subscription(Distances, "ultrasonic_distances", self.ultrasonic_callback, 10)

        self.robot_pose = [0, 0, 0]

    def publish_desired_waypoint(self):
        msg = Waypoint()
        msg.x = float(input("enter the desired x-coordinate  in mm: \n"))
        msg.y = float(input("enter the desired y-coordinate  in mm: \n"))
        self.waypoint_publisher.publish(msg)

    def pose_callback(self, msg:Pose):
        self.get_logger().info("Recieved robot pose: [" + str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta) + "]" )

    
    def ultrasonic_callback(self, msg:Distances):
        self.get_logger().info("Recieved ultrasonic distances: ( " + str(msg.sensor1) + ", " + str(msg.sensor2)+ ", " + str(msg.sensor3) + ")")


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
