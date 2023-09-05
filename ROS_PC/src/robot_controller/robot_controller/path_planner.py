#!/usr/bin/env python3
import sys
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/sample_planners')
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/grid_planners')
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller')

import rclpy
from rclpy.node import Node      
import time
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Distances
from robot_interfaces.msg import Obstacles
import numpy as np


from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# bit* imports
from bit import BITStar
from map_bit import Map
from path_straightener import straighten_path

# A* imports
from a_star import AStar
from env import Env
from path_smoothing import smooth_path
import plotting
import matplotlib.pyplot as plt

#pygame vis
import pygame
from graphics import Graphics



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

        """
        callback_group_ultrasonic = MutuallyExclusiveCallbackGroup()
        self.ultrasonic_subscriber = self.create_subscription(Distances, "ultrasonic_distances", self.ultrasonic_callback, 10, callback_group=callback_group_ultrasonic)
        """

        callback_group_obs = MutuallyExclusiveCallbackGroup()
        self.obs_subscriber = self.create_subscription(Obstacles, "obs_detected", self.obs_detected_callback, 10, callback_group=callback_group_obs)

        self.robot_pose = [300, 200, 90]
        self.goal_1 = [900, 800]
        self.goal_2 = [300, 800]
        
        self.mode = "BIT*"
        self.plotting = False
    
        if self.mode == "A*":
            map_size = [1200, 1200]
            self.scaling = 5
            self.map = Env()
            self.map.set_arena_size(map_size[0]//self.scaling, map_size[1]//self.scaling)
            # testing
            # self.add_obs_from_ultrasonic(150, 200)

        elif self.mode == "BIT*":
            self.map = Map()
            # testing
            # self.add_obs_from_ultrasonic(150, 200)
        
        self.obs_shape = "circle"
        self.obs_radius = 165
        self.path_updated = False
        self.path = []


        self.init_timer = self.create_timer(1, self.move_to_waypoint, callback_group=callback_group_main)
        # self.move_to_waypoint()

        self.gfx = Graphics()
        callback_group_vis = MutuallyExclusiveCallbackGroup()
        self.init_vis_timer= self.create_timer(0.2, self.main_vis_loop, callback_group=callback_group_vis)



    def move_to_waypoint(self):
        self.get_logger().info("Move started")
        self.init_timer.cancel()
        goal_seq = [self.goal_1, self.goal_2]
        start_point = True
        while len(goal_seq) > 0:
            if start_point:
                time.sleep(3)
            else:
                time.sleep(10)
            start_point = False

            current_goal = goal_seq.pop(0)
            self.path = self.recalculate_path(current_goal)
            self.path.pop(0)
            self.publish_next_waypoint()
            
            while len(self.path) > 0: 
                waypoint_x = self.path[0][0]
                waypoint_y = self.path[0][1]
                # self.get_logger().info("Current waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
                # self.get_logger().info("Current robot pose: (" + str(self.robot_pose[0]) + ", " + str(self.robot_pose[1]) +")")
                # tell the robot to move to some waypoint
                
                reached_waypoint = abs(self.robot_pose[0] - waypoint_x) < 5 and abs(self.robot_pose[1] - waypoint_y) < 5

                # self.get_logger().info(str(reached_waypoint))

                if reached_waypoint:
                    self.get_logger().info("Reached waypoint: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")
                    self.path.pop(0)

                    if len(self.path) > 0:
                        self.publish_next_waypoint()
                    else:
                        break

                if self.path_updated:
                    self.get_logger().info("path updating...")
                    while self.path_updated:
                        self.path_updated = False
                        self.path = self.recalculate_path(current_goal)
                    self.path.pop(0)
                    self.publish_next_waypoint()
        
    def publish_next_waypoint(self):
        waypoint_x = self.path[0][0]
        waypoint_y = self.path[0][1]
        msg = Waypoint()
        msg.x = float(waypoint_x)
        msg.y = float(waypoint_y)
        self.publish_desired_waypoint(msg.x, msg.y)
        self.get_logger().info("Published waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")

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
    
    """
    def ultrasonic_callback(self, msg:Distances):
        # self.get_logger().info("Recieved ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        obs_added = self.add_obs_from_ultrasonic(msg.sensor1, msg.sensor2)
        self.path_updated = obs_added
    """

    def obs_detected_callback(self, msg:Obstacles):
        if msg.flag:
            if msg.obs1_r > 0:
                self.add_obs(msg.obs1_x, msg.obs1_y, msg.obs1_r)
            if msg.obs2_r > 0:
                self.add_obs(msg.obs2_x, msg.obs2_y, msg.obs2_r)
            self.path_updated = msg.flag

    def recalculate_path(self, goal):

        if self.mode == "A*":
            path = None

            x_start = (self.robot_pose[0]//self.scaling , self.robot_pose[1]//self.scaling)  # Starting node
            x_goal = (goal[0]//self.scaling, goal[1]//self.scaling)  # Goal node

            # self.get_logger().info(str(x_start[0]) + ", " + str(x_start[1]))
            # self.get_logger().info(str(x_goal[0]) + ", " + str(x_goal[1]))

            while path is None:
                astar = AStar(x_start, x_goal, "euclidean", self.map)
                path, visited = astar.searching()    
                path = smooth_path(path)
                
                if path is not None:

                    if self.plotting:
                        plot = plotting.Plotting(x_start, x_goal, self.map)
                        plot.plot_grid("map")
                        x_coords = [x[0] for x in path]
                        y_coords = [x[1] for x in path]
                        plt.plot(x_coords, y_coords)
                        plt.show()

                    path = [[x[0]*self.scaling, x[1]*self.scaling] for x in path]
                    self.get_logger().info("new path planned")
                    for p in path:
                        self.get_logger().info("[" + str(p[0]) + " " + str(p[1])+ "]")

                    

                else:
                    self.get_logger().info("could not find path")
                    # shrink obs and retry

            # path = [[self.robot_pose[0], self.robot_pose[1]], [100,100], [200,200], [300,300], [self.goal_a[0], self.goal_a[1]]]
            return path
        
        elif self.mode == "BIT*":
            x_start = (self.robot_pose[0]/10, self.robot_pose[1]/10)  # Starting node
            x_goal = (goal[0]/10, goal[1]/10)  # Goal node
            eta = 2  # useless param it seems
            iter_max = 500

            self.get_logger().info(f"{x_start[0]}, {x_start[1]}")
            self.get_logger().info(f"{x_goal[0]}, {x_goal[1]}")
            path = None
            while path is None:

                bit = BITStar(x_start, x_goal, eta, iter_max, self.map, show_animation=False, plotting=self.plotting)
                path = bit.planning()
                path = straighten_path(path, self.map, n_iterations=100)

                if path is not None:
                    if self.plotting:
                        bit.plot_grid("map")
                        x_coords = [x[0] for x in path]
                        y_coords = [x[1] for x in path]
                        plt.plot(x_coords, y_coords)
                        plt.show()

                    path = [[x[0]*10, x[1]*10] for x in path]
                    self.get_logger().info("new path planned")
                    for p in path:
                        self.get_logger().info("[" + str(p[0]) + " " + str(p[1])+ "]")

                else:
                    self.get_logger().info("could not find path")
                    iter_max = int(iter_max*1.5)

            return path

    def add_obs(self, center_x, center_y, r_or_l):

        if self.mode == "A*":
            x = max(center_x//self.scaling, 1)
            y = max(center_y//self.scaling, 1)
            w = max(r_or_l//self.scaling, 1)
            self.map.add_square_obs(x, y, w)
        elif self.mode == "BIT*":
            
            self.map.add_obs_cirlce(center_x, center_y, r_or_l)
    

    
    def main_vis_loop(self):
        # self.get_logger().info("updating vis")
        pygame.event.get()
        self.gfx.draw_map()
        self.gfx.draw_robot(self.robot_pose)
        self.gfx.draw_obs(self.map.obs_circle)
        self.gfx.draw_path(self.robot_pose, self.path)
        pygame.display.update()
    
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
