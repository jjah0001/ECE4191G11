#!/usr/bin/env python3
import sys
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/sample_planners/')
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/grid_planners/')

import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Distances


from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# from bit import BITStar
# from map import Map
from Astar import Astar
from env import Env





class PathPlanner(Node):
    def __init__(self):
        super().__init__("path_planner_node") # name of the node in ros2
        self.get_logger().info("Path Planner Node initialised")


        callback_group_main = MutuallyExclusiveCallbackGroup()
        self.manual_waypoint_subscriber = self.create_subscription(Waypoint, "manual_waypoint", self.manual_waypoint_callback, 10, callback_group= callback_group_main)
        
        
        self.waypoint_publisher = self.create_publisher(Waypoint, "desired_waypoint", 10) # msg type, topic_name to publish to, buffer size

        callback_group_pose = MutuallyExclusiveCallbackGroup()
        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10, callback_group= callback_group_pose) 
        # msg type, topic_name to subscribe to, callback func, buffer size

        callback_group_ultrasonic = MutuallyExclusiveCallbackGroup()
        self.ultrasonic_subscriber = self.create_subscription(Distances, "ultrasonic_distances", self.ultrasonic_callback, 10, callback_group=callback_group_ultrasonic)

        self.robot_pose = [50, 50, 0]
        self.goal_a = [1000, 1000]

        self.map = Env()
        self.map.set_arena_size(1200, 1200)
        self.map.add_square_obs(400, 400, 100)

        self.path_updated = False
        self.path = []


        self.init_timer = self.create_timer(1, self.move_to_waypoint, callback_group=callback_group_main)
        # self.move_to_waypoint()


    def move_to_waypoint(self):
        self.get_logger().info("Move started")
        self.init_timer.cancel()
        self.path = self.recalculate_path()
        
        while len(self.path) > 0: 
            waypoint_x = self.path[0][0]
            waypoint_y = self.path[0][1]
            # self.get_logger().info("Current waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
            # self.get_logger().info("Current robot pose: (" + str(self.robot_pose[0]) + ", " + str(self.robot_pose[1]) +")")
            # tell the robot to move to some waypoint
            
            reached_waypoint = abs(self.robot_pose[0] - waypoint_x) < 5 and abs(self.robot_pose[1] - waypoint_x) < 5

            if reached_waypoint:
                self.get_logger().info("Reached waypoint: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
                self.path.pop(0)

                if len(self.path) > 0:
                    waypoint_x = self.path[0][0]
                    waypoint_y = self.path[0][1]
                    msg = Waypoint()
                    msg.x = float(waypoint_x)
                    msg.y = float(waypoint_y)
                    self.publish_desired_waypoint(msg.x, msg.y)
                    self.get_logger().info("Published waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
                else:
                    break

            if self.path_updated:
                self.path = self.recalculate_path()
        

    def manual_waypoint_callback(self, msg:Waypoint):
        if abs(self.robot_pose[0] - msg.x) > 0.05 or abs(self.robot_pose[1] - msg.y) > 0.05:
            self.publish_desired_waypoint(msg.x, msg.y)

    def publish_desired_waypoint(self, x, y):
        msg = Waypoint()
        msg.x = float(x)
        msg.y = float(y)
        self.waypoint_publisher.publish(msg)

    def pose_callback(self, msg:Pose):
        # self.get_logger().info("Recieved robot pose: [" + str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta) + "]" )
        self.robot_pose = [msg.x, msg.y, msg.theta]
    
    def ultrasonic_callback(self, msg:Distances):
        self.get_logger().info("Recieved ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        
        # if obs detected
            # calculate obs coord
            
            # add obs to map
            
            # self.map.add_square_obs(x, y, w)
            # # recalc path
            # self.path_updated = True
        pass
        
    def recalculate_path(self):
        path = None

        x_start = (self.robot_pose[0], self.robot_pose[1])  # Starting node
        x_goal = (self.goal_a[0], self.goal_a[1])  # Goal node

        self.get_logger().info(str(x_start[0]) + ", " + str(x_start[1]))
        self.get_logger().info(str(x_goal[0]) + ", " + str(x_goal[1]))

        while path is None:
            astar = AStar(x_start, x_goal, "euclidean", self.map)
            path, visited = astar.searching()
            if path is not None:
                path = [[x[0]*10, x[1]*10] for x in path]
                self.get_logger().info("new path planned")
                
        # path = [[self.robot_pose[0], self.robot_pose[1]], [100,100], [200,200], [300,300], [self.goal_a[0], self.goal_a[1]]]
        return path
    
def main(args=None):
    try:
        rclpy.init(args=args)

        path_planner_node = PathPlanner()

        executor = MultiThreadedExecutor()
        executor.add_node(path_planner_node)
        executor.spin()

    except KeyboardInterrupt:
        path_planner_node.get_logger().info("path planner node shutdown")
    rclpy.shutdown()

if __name__ == "__main__": # If you want to run node from terminal directly
    main()
