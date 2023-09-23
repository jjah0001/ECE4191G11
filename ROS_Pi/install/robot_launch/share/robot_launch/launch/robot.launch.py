from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    robot_node = Node(
        package = "robot_controller",
        executable = "robot_node"
    )

    ld.add_action(robot_node)
    

    return ld

