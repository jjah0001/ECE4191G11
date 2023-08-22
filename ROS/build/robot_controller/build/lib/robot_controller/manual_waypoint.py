#!/usr/bin/env python3
import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint

class ManualWaypoint(Node):
    def __init__(self):
        super().__init__("manual_waypoint_node") # name of the node in ros2
        self.get_logger().info("Manual Waypoint Node initialised")

        self.waypoint_timer = self.create_timer(0.1, self.publish_manual_waypoint)
        self.waypoint_publisher = self.create_publisher(Waypoint, "manual_waypoint", 10) # msg type, topic_name to publish to, buffer size


    def publish_manual_waypoint(self):
        msg = Waypoint()
        msg.x = float(input("enter the desired x-coordinate  in mm: \n"))
        msg.y = float(input("enter the desired y-coordinate  in mm: \n"))
        self.waypoint_publisher.publish(msg)

def main(args=None):
    try:
        rclpy.init(args=args)

        manual_waypoint_node = ManualWaypoint()
        rclpy.spin(manual_waypoint_node)

    except KeyboardInterrupt:
        manual_waypoint_node.get_logger().info("Manual Waypoint node shutdown")
    rclpy.shutdown()

if __name__ == "__main__": # If you want to run node from terminal directly
    main()