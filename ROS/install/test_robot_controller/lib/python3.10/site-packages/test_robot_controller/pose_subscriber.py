#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriberNode(Node):
    def __init__(self):
        super().__init__("pose_subscriber") # name of the node in ros2
        self.my_pose_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10) 
        # msg type, topic_name to subscribe to, callback func, buffer size


    def pose_callback(self, msg:Pose):
        self.get_logger().info(str(msg.x) + ", " + str(msg.y))


def main(args=None):
    rclpy.init(args=args) # initialise ros2 communications
    node = PoseSubscriberNode()


    rclpy.spin(node) # making a node spin, means keeping the node alive until killed, enables all callbacks
    rclpy.shutdown() # shutdown ros2 communications, close the node

if __name__ == "__main__": # If you want to run node from terminal directly
    main()
