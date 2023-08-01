#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# creating our node class inheriting rclpy Node class
class MyNode(Node): 

    def __init__(self):
        super().__init__("first_node") # name of the node in ros2
        self.get_logger().info("hello from ROS2")

def main(args=None):
    rclpy.init(args=args) # initialise ros2 communications
    node = MyNode()



    rclpy.spin(node) # making a node spin, means keeping the node alive until killed
    rclpy.shutdown() # shutdown ros2 communications, close the node


if __name__ == "__main__":
    main()