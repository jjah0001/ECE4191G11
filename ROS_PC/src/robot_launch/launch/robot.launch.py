from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    path_planner_node = Node(
        package = "robot_controller",
        executable = "path_planner_node"
    )

    server_node = Node(
        package = "robot_controller",
        executable = "server_node"
    )

    ld.add_action(path_planner_node)
    ld.add_action(server_node)

    return ld

