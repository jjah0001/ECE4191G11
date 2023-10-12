from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    path_planner_node = Node(
        package = "robot_controller",
        executable = "path_planner_node"
    )

    telecommunication_node = Node(
        package = "robot_controller",
        executable = "telecommunication_node"
    )

    ld.add_action(path_planner_node)
    ld.add_action(telecommunication_node)

    return ld

