from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    """
    ultrasonic_node = Node(
        package = "robot_controller",
        executable = "ultrasonic_node"
    )
    ld.add_action(ultrasonic_node)
    """

    driver_node = Node(
        package = "robot_controller",
        executable = "drive_node"
    )

    encoder_node = Node(
        package = "robot_controller",
        executable = "encoder_node"
    )

    ld.add_action(driver_node)
    
    ld.add_action(encoder_node)

    return ld

