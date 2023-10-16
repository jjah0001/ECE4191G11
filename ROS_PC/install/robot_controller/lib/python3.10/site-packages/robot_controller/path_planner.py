#!/usr/bin/env python3
import sys
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/sample_planners')
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/grid_planners')
sys.path.insert(1, '/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller')

import rclpy
from rclpy.node import Node      
import time
from copy import deepcopy
from robot_interfaces.msg import DesState
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Obstacles
from robot_interfaces.msg import QRData
from robot_interfaces.msg import JSONData
from robot_interfaces.msg import Flag


from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# bit* imports
from bit import BITStar
from map_bit import Map
from path_straightener import straighten_path

# A* imports
from a_star import AStar
from env import Env
from path_smoothing import smooth_path, path_intersects
import plotting
import matplotlib.pyplot as plt

#pygame vis
import pygame
from graphics import Graphics


import json

class PathPlanner(Node):
    def __init__(self):
        super().__init__("path_planner_node") # name of the node in ros2
        self.get_logger().info("Path Planner Node initialised")


        callback_group_main = MutuallyExclusiveCallbackGroup()
        self.manual_waypoint_subscriber = self.create_subscription(DesState, "manual_waypoint", self.manual_waypoint_callback, 10, callback_group= callback_group_main)
        
        self.des_state_publisher = self.create_publisher(DesState, "des_state", 10) # msg type, topic_name to publish to, buffer size

        callback_group_pose = MutuallyExclusiveCallbackGroup()
        self.pose_subscriber = self.create_subscription(Pose, "estimated_pose", self.pose_callback, 10, callback_group= callback_group_pose) 
        # msg type, topic_name to subscribe to, callback func, buffer size

        """
        callback_group_ultrasonic = MutuallyExclusiveCallbackGroup()
        self.ultrasonic_subscriber = self.create_subscription(Distances, "ultrasonic_distances", self.ultrasonic_callback, 10, callback_group=callback_group_ultrasonic)
        """

        '''
        Telecommunication Section
        '''
        callback_group_comms = MutuallyExclusiveCallbackGroup()
        # Use this to initialise the node and then run the receive_messages function to listen in on the server?
        self.comms_subscriber = self.create_subscription(JSONData, "json_data", self.receive_telecommunication_callback, 10, callback_group=callback_group_comms)

        callback_group_obs = MutuallyExclusiveCallbackGroup()
        self.obs_subscriber = self.create_subscription(Obstacles, "obs_detected", self.obs_detected_callback, 10, callback_group=callback_group_obs)
        self.qr_subscriber = self.create_subscription(QRData, "qr_data", self.qr_callback, 10, callback_group=callback_group_obs)
        self.return_subscriber = self.create_subscription(QRData, "return_state", self.return_callback, 10, callback_group=callback_group_obs)

        self.home = [250, 250]
        self.robot_pose = [self.home[0], self.home[1], 90]
        self.goal_list = [[190, 1000], [600, 1000], [1010, 1000]]
        self.goal = [self.home[0], self.home[1]] # temporary goal
        

        self.mode = "A*"
        self.plotting = False
    
        if self.mode == "A*":
            map_size = [1200, 1200]
            self.scaling = 4
            self.map = Env(self.scaling)
            self.map.set_arena_size(map_size[0]//self.scaling, map_size[1]//self.scaling)
            # testing
            # self.map.add_square_obs(300, 600, 150)

        elif self.mode == "BIT*":
            self.map = Map()
            # testing
            # self.map.add_obs_cirlce(300, 600, 150)
        
        self.path_updated = False
        self.path = []


        self.init_timer = self.create_timer(1, self.main_loop, callback_group=callback_group_main)
        # self.move_to_waypoint()

        self.gfx = Graphics()
        callback_group_vis = MutuallyExclusiveCallbackGroup()
        self.init_vis_timer= self.create_timer(0.2, self.main_vis_loop, callback_group=callback_group_vis)

        # possible_states = ["wait_qr", "to_goal", "deliver", "to_home", "localise"]
        self.state = "to_goal"
        self.prev_state = "wait_qr"
        self.qr_data = -2


        ### PARTNER ROBOT VARS
        self.partner_pose = [1000, 300, 90]
        self.add_obs(1000, 300, 150+150)

    def main_loop(self):
        self.init_timer.cancel()
        while True:
            if self.state == "wait_qr":
                if self.qr_data == -2:
                    self.get_logger().info(f"Published command to start qr scanning")
                    self.publish_des_state(state = 0, x=-1.0, y=-1.0, theta=-1.0)
                    self.qr_data = -1
                elif self.qr_data >= 0:
                    self.get_logger().info(f"Got goal from QR Code: {self.qr_data}")
                    self.goal = self.goal_list[self.qr_data-1]
                    self.qr_data = -2
                    self.prev_state = self.state
                    self.state = "to_goal"
                    

            elif self.state == "to_goal":
                self.qr_data = 1
                self.goal = self.goal_list[self.qr_data-1]

                self.get_logger().info(f"Moving to goal at [{self.goal[0]}, {self.goal[1]}]")
                self.move_to_waypoint(self.goal)
                self.prev_state = self.state
                self.state = "deliver"
            
            elif self.state == "deliver":
                if self.prev_state != "deliver":
                    self.get_logger().info("Dropping off parcel")
                    self.publish_des_state(state = 2, x=-1.0, y=-1.0, theta=-1.0)
                    self.prev_state = self.state

            
            elif self.state == "to_home":
                self.get_logger().info(f"Moving to home at [{self.home[0]}, {self.home[1]}]")
                self.move_to_waypoint(self.home)
                self.prev_state = self.state
                self.state = "localise"
            
            elif self.state == "localise":
                if self.prev_state != "localise":
                    self.get_logger().info(f"Localising sequence")
                    self.publish_des_state(state = 3, x=-1.0, y=-1.0, theta=-1.0)
                    self.prev_state = self.state

    def qr_callback(self, msg:QRData):
        self.qr_data = msg.data
    
    def return_callback(self, msg:QRData):
        if msg.data == 2:
            self.prev_state = self.state
            self.state = "to_home"
        if msg.data == 3:
            self.prev_state = self.state
            self.state = "wait_qr"

    def move_to_waypoint(self, waypoint):
        self.get_logger().info("Move started")
        goal_seq = [waypoint]
        start_point = True
        while len(goal_seq) > 0:
            if start_point:
                time.sleep(0.1)
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
        waypoint_theta = self.path[0][2]

        self.publish_des_state(int(1), float(waypoint_x), float(waypoint_y), float(waypoint_theta))
        self.get_logger().info("Published waypoint to move to: (" + str(waypoint_x) + ", " + str(waypoint_y) +")")

    def manual_waypoint_callback(self, msg:DesState):
        if abs(self.robot_pose[0] - msg.x) > 0.05 or abs(self.robot_pose[1] - msg.y) > 0.05:
            self.publish_des_state(1, msg.x, msg.y)

    def publish_des_state(self, state, x, y, theta):
        msg = DesState()
        msg.state = int(state)
        msg.x = float(x)
        msg.y = float(y)
        msg.theta = float(theta)
        self.des_state_publisher.publish(msg)

    def pose_callback(self, msg:Pose):
        # self.get_logger().info("Recieved robot pose: [" + str(msg.x) + ", " + str(msg.y)+ ", " + str(msg.theta) + "]" )
        self.robot_pose = [msg.x, msg.y, msg.theta]
    
    """
    def ultrasonic_callback(self, msg:Distances):
        # self.get_logger().info("Recieved ultrasonic distances: ( Sensor 1: " + str(msg.sensor1) + ", Sensor 2: " + str(msg.sensor2) + ")")
        obs_added = self.add_obs_from_ultrasonic(msg.sensor1, msg.sensor2)
        self.path_updated = obs_added
    """

    def receive_telecommunication_callback(self, msg:JSONData):
        # JSONData is just a string
        JSON_object = json.loads(msg.json_data)

        self.partner_pose = JSON_object["pose"]
        self.map.clear_obs()
        self.add_obs(self.partner_pose[0], self.partner_pose[1], 150+150)
        current_path = deepcopy(self.path)
        current_path.insert(0, [self.robot_pose[0], self.robot_pose[1], self.robot_pose[2]])

        if path_intersects(current_path, self.map.obs_list_segments):
            self.get_logger().info("Path obstructed, stopping robot, replanning...")
            self.publish_des_state(state = -1, x=-1.0, y=-1.0, theta=-1.0)
            time.sleep(0.1)
            self.path_updated = True
        else:
            self.get_logger().info("no intersections")

        # Use these variables however you wish --------------------


    def obs_detected_callback(self, msg:Obstacles):
        if msg.flag:
            if msg.obs1_r > 0:
                self.add_obs(msg.obs1_x, msg.obs1_y, msg.obs1_r)
            if msg.obs2_r > 0:
                self.add_obs(msg.obs2_x, msg.obs2_y, msg.obs2_r)
            if msg.obs3_r > 0:
                self.add_obs(msg.obs3_x, msg.obs3_y, msg.obs3_r)
            self.path_updated = msg.flag

    def recalculate_path(self, goal):
        start_time = time.time()
        if self.mode == "A*":
            path = None

            x_start = (self.robot_pose[0]//self.scaling , self.robot_pose[1]//self.scaling)  # Starting node
            x_goal = (goal[0]//self.scaling, goal[1]//self.scaling)  # Goal node

            # self.get_logger().info(str(x_start[0]) + ", " + str(x_start[1]))
            # self.get_logger().info(str(x_goal[0]) + ", " + str(x_goal[1]))

            while path is None:
                try:
                    astar = AStar(x_start, x_goal, "euclidean", self.map)
                    path, visited = astar.searching()    
                except KeyError:

                    seg_str = ""
                    for s in self.map.obs_list_segments:
                        seg_str += f"[[{s[0][0]},{s[0][1]}], [{s[1][0]},{s[1][1]}]]"
                    self.get_logger().info(seg_str) 

                    self.get_logger().info("could not find path, trying again after 3s")
                    time.sleep(3)
                    return self.recalculate_path(goal)

                if path is not None:

                    if self.plotting:
                        plot = plotting.Plotting(x_start, x_goal, self.map)
                        plot.plot_grid("map")
                        x_coords = [x[0] for x in path]
                        y_coords = [x[1] for x in path]
                        plt.plot(x_coords, y_coords)
                        plt.show()

                    path = [[x[0]*self.scaling, x[1]*self.scaling] for x in path]
                    path = smooth_path(path, self.map.obs_list_segments, n_iterations = 50)
                    self.get_logger().info("new path planned")                    

                else:
                    self.get_logger().info("could not find path")
                    # shrink obs and retry


            # path = [[self.robot_pose[0], self.robot_pose[1]], [100,100], [200,200], [300,300], [self.goal_a[0], self.goal_a[1]]]
            self.get_logger().info(f"Time taken: {time.time()-start_time}")
        
        elif self.mode == "BIT*":
            x_start = (self.robot_pose[0]/10, self.robot_pose[1]/10)  # Starting node
            x_goal = (goal[0]/10, goal[1]/10)  # Goal node
            eta = 2  # useless param it seems
            iter_max = 500

            # self.get_logger().info(f"{x_start[0]}, {x_start[1]}")
            # self.get_logger().info(f"{x_goal[0]}, {x_goal[1]}")
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

                else:
                    self.get_logger().info("could not find path")
                    iter_max = int(iter_max*1.5)
            self.get_logger().info(f"Time taken: {time.time()-start_time}")

        for i in range(len(path)):
            path[i].append(-1)
        
        if self.state == "to_goal":
            path[-1][2] = 90
        elif self.state == "to_home":
            path[-1][2] = 270

        path_str = ""
        for p in path:
            path_str += "[" + str(p[0]) + ", " + str(p[1])+ "," + str(p[2]) + "] "
        self.get_logger().info(path_str) 

        return path

    def add_obs(self, center_x, center_y, r_or_l):

        if self.mode == "A*":
            x = max(center_x//self.scaling, 1)
            y = max(center_y//self.scaling, 1)
            w = max(r_or_l//self.scaling, 1)

            self.map.add_square_obs(x, y, w)

        elif self.mode == "BIT*":
            
            # self.map.add_obs_circle(center_x, center_y, r_or_l)
            self.map.add_obs_circle(center_x, center_y, r_or_l)



    def main_vis_loop(self):
        # self.get_logger().info("updating vis")
        pygame.event.get()
        self.gfx.draw_map()
        if self.mode == "BIT*":
            self.gfx.draw_obs(self.map.obs_circle)
        else:
            # self.gfx.draw_obs(self.map.obs_list_gfx)
            pass
        self.gfx.draw_robot(self.robot_pose)
        self.gfx.draw_partner_robot(self.partner_pose)
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
