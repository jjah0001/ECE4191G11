#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# creating our node class inheriting rclpy Node class
class MyNode(Node): 

    def __init__(self):
        super().__init__("first_node") # name of the node in ros2
        #self.get_logger().info("Hello from ROS2!")
        self.counter = 0
        self.create_timer(1.0, self.timer_callback)


    def timer_callback(self):
        self.get_logger().info("Hello " + str(self.counter))
        self.counter += 1

def main(args=None):
    rclpy.init(args=args) # initialise ros2 communications
    node = MyNode()



    rclpy.spin(node) # making a node spin, means keeping the node alive until killed, enables all callbacks
    rclpy.shutdown() # shutdown ros2 communications, close the node


if __name__ == "__main__": # if you want to run on terminal directly
    main()