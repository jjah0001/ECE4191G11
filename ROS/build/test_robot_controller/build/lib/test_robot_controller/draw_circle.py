#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # need to import all the msg types you use, new <depend> tag needs to be added for new package

class DrawCircleNode(Node):
    def __init__(self):
        super().__init__("draw_circle") # name of the node in ros2
        self.get_logger().info("Draw circle node has started")
        self.timer = self.create_timer(0.5, self.send_velocity_command)
        self.my_cmd_vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10) # msg type, topic_name to publish to, buffer size


    def send_velocity_command(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.my_cmd_vel_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args) # initialise ros2 communications
    node = DrawCircleNode()


    rclpy.spin(node) # making a node spin, means keeping the node alive until killed, enables all callbacks
    rclpy.shutdown() # shutdown ros2 communications, close the node

if __name__ == "__main__": # If you want to run node from terminal directly
    main()

"""
Note to self, when creating a new node:
- make sure file is executable
- make sure all packages are listed in package.xml
- add node to setup.py
- run colcon build --symlink-install , in ros2_ws
- source ~/.bashrc
"""