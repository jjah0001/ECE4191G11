#!/usr/bin/env python3
import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import Pose

class PathPlanner(Node):
    def __init__(self):
        super().__init__("path_planner_node") # name of the node in ros2
        self.get_logger().info("Path Planner Node initialised")

        self.waypoint_timer = self.create_timer(0.01, self.publish_desired_waypoint)
        self.waypoint_publisher = self.create_publisher(Waypoint, "desired_waypoint", 10) # msg type, topic_name to publish to, buffer size

        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10) 
        # msg type, topic_name to subscribe to, callback func, buffer size


    def publish_desired_waypoint(self):
        msg = Waypoint()
        msg.x = 123.123
        msg.y = 456.456
        self.waypoint_publisher.publish(msg)

    def pose_callback(self, msg:Pose):
        self.get_logger().info(str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta))


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
