#!/usr/bin/env python3
import sys

sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller')

import rclpy
from rclpy.node import Node

from rclpy.executors import MultiThreadedExecutor
from robot_interfaces.msg import JSONData

import json
import socket
import threading
from cryptography.fernet import Fernet


class Telecommunication(Node):
    def __init__(self):
        super().__init__("telecommunication_node")  # name of node in ros2
        self.get_logger().info("Telecommunication Node initialised")
        # Client Socket
        # Host Address
        # Port
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_address = '127.0.0.1'  # Replace this with Server IP address
        port = 12345  # Replace with server suitable port
        client_socket.connect((host_address, port))
        self.get_logger().info("CONNECTED TO SERVER")
        # Receive private key
        key = client_socket.recv(1024)
        self.get_logger().info("RECEIVED KEY")
        cipher_suite = Fernet(key)

        self.client_socket = client_socket
        self.cipher_suite = cipher_suite

        # Comms Publisher
        self.comms_publisher = self.create_publisher(JSONData, "json_data", 10)

    def receive_messages(self):
        while rclpy.ok():
            try:
                # Attempt to receive a message from the server (non-blocking)
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    # Decrypt the message
                    decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
                    # JSON_object = json.loads(decrypted_message)

                    # Functions here to check stuff
                    # Send the JSON string to the path planner node
                    self.process_received_message(decrypted_message)

            except Exception as e:
                # Handle exceptions
                self.get_logger().error(f'Error receiving message: {str(e)}')

    def send_message(self, JSON_object):
        # stringify JSON_object
        JSON_object_str = json.dumps(JSON_object)
        encrypted_message = self.cipher_suite.encrypt(JSON_object_str.encode())
        # Send the message to the server to broadcast
        self.client_socket.send(encrypted_message)

    def process_received_message(self, JSON_object):
        # Implement what we want to do with the object
        # Send message to Path Planner Node
        msg = JSON_object  # Should be a string, handle the object in path planner

        self.comms_publisher.publish(msg)


def main(args=None):
    try:
        rclpy.init(args=args)
        telecommunication_node = Telecommunication()

        executor = MultiThreadedExecutor()
        executor.add_node(telecommunication_node)
        executor.spin()
    except KeyboardInterrupt:
        telecommunication_node.get_logger().info("Telecommunications node shutdown")

    telecommunication_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    '''
    JSON_object = {"robot_id": x, "location": x, "status": x, "bin": x, "current_path": x}
    # Robot ID -
    # Location - [x, y]
    # Status - "Loading", "Unloading", "Moving", "Idle"
    # Bin - 1, 2, 3
    # Current Path - [[x, y]...]
    '''
