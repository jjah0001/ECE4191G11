#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.get_logger().info("Turtle controller has been initialised")
        # In this controller, we run the publisher in the subscriber callback
        # So it publishes 1 msg everytime it reads 1 msg
        self.pose_sub = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10)
        self.cmd_vel_pub = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        self.prev_x = 0


    def pose_callback(self, pose: Pose):
        cmd = Twist()
        if pose.x > 9.0 or pose.x <2.0 or pose.y >9.0 or pose.y < 2.0:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0

        self.cmd_vel_pub.publish(cmd)

        if pose.x >5.5 and self.prev_x <= 5.5:
            self.prev_x = pose.x
            self.call_set_pen_service(255, 0, 0, 3, 0)
            self.get_logger().info("Set colour to red")
        elif pose.x <= 5.5 and self.prev_x > 5.5:
            self.prev_x = pose.x
            self.call_set_pen_service(0, 255, 0, 3, 0)
            self.get_logger().info("Set colour to green")


    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, "/turtle1/set_pen")
                                    # service type, service name
        # wait for service to start, before calling
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for service...")

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen)) # adding callback when service replies
    
    def callback_set_pen(self, future):
        try:
            response = future.result()  # This is the result or the service, in this case there is no response.
            # Previously add_two_ints would be able to use response.sum to get sum
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))



def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
