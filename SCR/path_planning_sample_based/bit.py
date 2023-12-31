import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial.transform import Rotation as Rot

import plotting, utils
from map import Map
from path_smoothing import smooth_path, straighten_path

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


class Tree:
    def __init__(self, x_start, x_goal):
        self.x_start = x_start
        self.goal = x_goal

        self.r = 8.0
        self.V = set()
        self.E = set()
        self.QE = set()
        self.QV = set()

        self.V_old = set()


class BITStar:
    def __init__(self, x_start, x_goal, eta, iter_max, Map, show_animation = False):
        self.x_start = Node(x_start[0], x_start[1])
        self.x_goal = Node(x_goal[0], x_goal[1])
        self.eta = eta
        self.iter_max = iter_max

        self.env = Map
        self.show_animation = show_animation
        self.plotting = plotting.Plotting(x_start, x_goal, Map)
        self.fig, self.ax = plt.subplots()
        self.utils = utils.Utils(Map)

        

        self.delta = self.utils.delta
        self.x_range = Map.x_range
        self.y_range = self.env.y_range

        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

        self.Tree = Tree(self.x_start, self.x_goal)
        self.X_sample = set()
        self.g_T = dict()

    def init(self):
        self.Tree.V.add(self.x_start)
        self.X_sample.add(self.x_goal)

        self.g_T[self.x_start] = 0.0
        self.g_T[self.x_goal] = np.inf

        cMin, theta = self.calc_dist_and_angle(self.x_start, self.x_goal)
        C = self.RotationToWorldFrame(self.x_start, self.x_goal, cMin)
        xCenter = np.array([[(self.x_start.x + self.x_goal.x) / 2.0],
                            [(self.x_start.y + self.x_goal.y) / 2.0], [0.0]])

        return theta, cMin, xCenter, C

    def add_obs_cirlce(self, x, y, r):
        self.obs_circle.append([x, y, r])
        self.env.obs_circle.append([x, y, r])
        self.utils.obs_circle.append([x, y, r])
        self.utils.env.obs_circle.append([x, y, r])

    def add_obs_rectangle(self, x, y, w, h):
        self.obs_rectangle.append([x, y, w, h])
        self.env.rectangle.append([x, y, w, h])
        self.utils.rectangle.append([x, y, w, h])
        self.utils.env.rectangle.append([x, y, w, h])
    

    def planning(self):
        theta, cMin, xCenter, C = self.init()
        optimisation_count = 0
        for k in range(self.iter_max):
            # print(k)
            if not self.Tree.QE and not self.Tree.QV:
                if k == 0:
                    m = 1300
                else:
                    m = 250
                
                if self.x_goal.parent is not None:
                    path_x, path_y = self.ExtractPath()
                    if self.show_animation:
                        plt.plot(path_x, path_y, linewidth=2, color='r')
                        plt.pause(0.01)


                if optimisation_count > 3:
                    break
                optimisation_count +=1

                self.Prune(self.g_T[self.x_goal])
                self.X_sample.update(self.Sample(m, self.g_T[self.x_goal], cMin, xCenter, C))
                self.Tree.V_old = {v for v in self.Tree.V}
                self.Tree.QV = {v for v in self.Tree.V}
                # self.Tree.r = self.radius(len(self.Tree.V) + len(self.X_sample))


            while self.BestVertexQueueValue() <= self.BestEdgeQueueValue():
                self.ExpandVertex(self.BestInVertexQueue())

            vm, xm = self.BestInEdgeQueue()
            self.Tree.QE.remove((vm, xm))

            if self.g_T[vm] + self.calc_dist(vm, xm) + self.h_estimated(xm) < self.g_T[self.x_goal]:
                actual_cost = self.cost(vm, xm)
                if self.g_estimated(vm) + actual_cost + self.h_estimated(xm) < self.g_T[self.x_goal]:
                    if self.g_T[vm] + actual_cost < self.g_T[xm]:
                        if xm in self.Tree.V:
                            # remove edges
                            edge_delete = set()
                            for v, x in self.Tree.E:
                                if x == xm:
                                    edge_delete.add((v, x))

                            for edge in edge_delete:
                                self.Tree.E.remove(edge)
                        else:
                            self.X_sample.remove(xm)
                            self.Tree.V.add(xm)
                            self.Tree.QV.add(xm)

                        self.g_T[xm] = self.g_T[vm] + actual_cost
                        self.Tree.E.add((vm, xm))
                        xm.parent = vm

                        set_delete = set()
                        for v, x in self.Tree.QE:
                            if x == xm and self.g_T[v] + self.calc_dist(v, xm) >= self.g_T[xm]:
                                set_delete.add((v, x))

                        for edge in set_delete:
                            self.Tree.QE.remove(edge)
            else:
                self.Tree.QE = set()
                self.Tree.QV = set()

            if self.show_animation and k % 5 == 0:
                self.animation(xCenter, self.g_T[self.x_goal], cMin, theta)

        path_x, path_y = self.ExtractPath()
        if self.show_animation:
            plt.plot(path_x, path_y, linewidth=2, color='r')
            plt.pause(0.01)
            plt.show()
        
        if len(path_x) == 1:
            return None

        path = []
        tot_dist = 0
        for i in range(len(path_x)-1, -1, -1):
            path.append([path_x[i], path_y[i]])
            
            if i >= 1:
                tot_dist+= np.sqrt((path_x[i]-path_x[i-1])**2 + (path_y[i]-path_y[i-1])**2 )
        print(tot_dist)
        
        return path
        
    def ExtractPath(self):
        node = self.x_goal
        path_x, path_y = [node.x], [node.y]

        while node.parent:
            node = node.parent
            path_x.append(node.x)
            path_y.append(node.y)

        return path_x, path_y

    def Prune(self, cBest):
        self.X_sample = {x for x in self.X_sample if self.f_estimated(x) < cBest}
        self.Tree.V = {v for v in self.Tree.V if self.f_estimated(v) <= cBest}
        self.Tree.E = {(v, w) for v, w in self.Tree.E
                       if self.f_estimated(v) <= cBest and self.f_estimated(w) <= cBest}
        self.X_sample.update({v for v in self.Tree.V if self.g_T[v] == np.inf})
        self.Tree.V = {v for v in self.Tree.V if self.g_T[v] < np.inf}

    def cost(self, start, end):
        if self.utils.is_collision(start, end):
            return np.inf

        return self.calc_dist(start, end)

    def f_estimated(self, node):
        return self.g_estimated(node) + self.h_estimated(node)

    def g_estimated(self, node):
        return self.calc_dist(self.x_start, node)

    def h_estimated(self, node):
        return self.calc_dist(node, self.x_goal)

    def Sample(self, m, cMax, cMin, xCenter, C):
        if cMax < np.inf:
            return self.SampleEllipsoid(m, cMax, cMin, xCenter, C)
        else:
            return self.SampleFreeSpace(m)

    def SampleEllipsoid(self, m, cMax, cMin, xCenter, C):
        print("sampling")
        r = [cMax / 2.0,
             math.sqrt(cMax ** 2 - cMin ** 2) / 2.0,
             math.sqrt(cMax ** 2 - cMin ** 2) / 2.0]
        L = np.diag(r)

        ind = 0
        delta = self.delta
        Sample = set()

        while ind < m:
            xBall = self.SampleUnitNBall()
            x_rand = np.dot(np.dot(C, L), xBall) + xCenter
            node = Node(x_rand[(0, 0)], x_rand[(1, 0)])
            in_obs = self.utils.is_inside_obs(node)
            in_x_range = self.x_range[0] + delta <= node.x <= self.x_range[1] - delta
            in_y_range = self.y_range[0] + delta <= node.y <= self.y_range[1] - delta

            if not in_obs and in_x_range and in_y_range:
                Sample.add(node)
                ind += 1

        return Sample

    def SampleFreeSpace(self, m):
        delta = self.utils.delta
        Sample = set()

        ind = 0
        while ind < m:
            node = Node(random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                        random.uniform(self.y_range[0] + delta, self.y_range[1] - delta))
            if self.utils.is_inside_obs(node):
                continue
            else:
                Sample.add(node)
                ind += 1

        return Sample

    def radius(self, q):
        cBest = self.g_T[self.x_goal]
        lambda_X = len([1 for v in self.Tree.V if self.f_estimated(v) <= cBest])
        radius = 2 * self.eta * (1.5 * lambda_X / math.pi * math.log(q) / q) ** 0.5

        return radius

    def ExpandVertex(self, v):
        self.Tree.QV.remove(v)
        X_near = {x for x in self.X_sample if self.calc_dist(x, v) <= self.Tree.r}

        for x in X_near:
            if self.g_estimated(v) + self.calc_dist(v, x) + self.h_estimated(x) < self.g_T[self.x_goal]:
                self.g_T[x] = np.inf
                self.Tree.QE.add((v, x))

        if v not in self.Tree.V_old:
            V_near = {w for w in self.Tree.V if self.calc_dist(w, v) <= self.Tree.r}

            for w in V_near:
                if (v, w) not in self.Tree.E and \
                        self.g_estimated(v) + self.calc_dist(v, w) + self.h_estimated(w) < self.g_T[self.x_goal] and \
                        self.g_T[v] + self.calc_dist(v, w) < self.g_T[w]:
                    self.Tree.QE.add((v, w))
                    if w not in self.g_T:
                        self.g_T[w] = np.inf

    def BestVertexQueueValue(self):
        if not self.Tree.QV:
            return np.inf

        return min(self.g_T[v] + self.h_estimated(v) for v in self.Tree.QV)

    def BestEdgeQueueValue(self):
        if not self.Tree.QE:
            return np.inf

        return min(self.g_T[v] + self.calc_dist(v, x) + self.h_estimated(x)
                   for v, x in self.Tree.QE)

    def BestInVertexQueue(self):
        if not self.Tree.QV:
            print("QV is Empty!")
            return None

        v_value = {v: self.g_T[v] + self.h_estimated(v) for v in self.Tree.QV}

        return min(v_value, key=v_value.get)

    def BestInEdgeQueue(self):
        if not self.Tree.QE:
            print("QE is Empty!")
            return None

        e_value = {(v, x): self.g_T[v] + self.calc_dist(v, x) + self.h_estimated(x)
                   for v, x in self.Tree.QE}

        return min(e_value, key=e_value.get)

    @staticmethod
    def SampleUnitNBall():
        while True:
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
            if x ** 2 + y ** 2 < 1:
                return np.array([[x], [y], [0.0]])

    @staticmethod
    def RotationToWorldFrame(x_start, x_goal, L):
        a1 = np.array([[(x_goal.x - x_start.x) / L],
                       [(x_goal.y - x_start.y) / L], [0.0]])
        e1 = np.array([[1.0], [0.0], [0.0]])
        M = a1 @ e1.T
        U, _, V_T = np.linalg.svd(M, True, True)
        C = U @ np.diag([1.0, 1.0, np.linalg.det(U) * np.linalg.det(V_T.T)]) @ V_T

        return C

    @staticmethod
    def calc_dist(start, end):
        return math.hypot(start.x - end.x, start.y - end.y)

    @staticmethod
    def calc_dist_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)

    def animation(self, xCenter, cMax, cMin, theta):
        plt.cla()
        self.plot_grid("Batch Informed Trees (BIT*)")

        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

        for v in self.X_sample:
            plt.plot(v.x, v.y, marker='.', color='lightgrey', markersize='2')

        if cMax < np.inf:
            self.draw_ellipse(xCenter, cMax, cMin, theta)

        for v, w in self.Tree.E:
            plt.plot([v.x, w.x], [v.y, w.y], '-g')

        plt.pause(0.001)

    def plot_grid(self, name):
        for (ox, oy, w, h) in self.obs_boundary:
            self.ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, w, h) in self.obs_rectangle:
            self.ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        for (ox, oy, r) in self.obs_circle:
            self.ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        plt.plot(self.x_start.x, self.x_start.y, "bs", linewidth=3)
        plt.plot(self.x_goal.x, self.x_goal.y, "rs", linewidth=3)

        plt.title(name)
        plt.axis("equal")

    @staticmethod
    def draw_ellipse(x_center, c_best, dist, theta):
        a = math.sqrt(c_best ** 2 - dist ** 2) / 2.0
        b = c_best / 2.0
        angle = math.pi / 2.0 - theta
        cx = x_center[0]
        cy = x_center[1]
        t = np.arange(0, 2 * math.pi + 0.1, 0.2)
        x = [a * math.cos(it) for it in t]
        y = [b * math.sin(it) for it in t]
        rot = Rot.from_euler('z', -angle).as_matrix()[0:2, 0:2]
        fx = rot @ np.array([x, y])
        px = np.array(fx[0, :] + cx).flatten()
        py = np.array(fx[1, :] + cy).flatten()
        plt.plot(cx, cy, marker='.', color='darkorange')
        plt.plot(px, py, linestyle='--', color='darkorange', linewidth=2)
    

    def add_obs_from_ultrasonic(self, dist1, dist2):
        robot_pose = [300, 300,45]
        proj_x, proj_y = self.project_coords(0, robot_pose, dist1)

        if self.no_overlaps([proj_x, proj_y, 150], self.env.obs_circle, 100):
            self.env.add_obs_cirlce(proj_x, proj_y, 150)

        proj_x, proj_y = self.project_coords(1, robot_pose, dist2)
        if self.no_overlaps([proj_x, proj_y, 150], self.env.obs_circle, 100):
            self.env.add_obs_cirlce(proj_x, proj_y, 150)


    def project_coords(self, sensor, pose, dist):
        if sensor == 0:
            sensor_x = 65
            sensor_y = 140
            sensor_angle = np.arctan(sensor_x/sensor_y)*180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] + sensor_angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)
        elif sensor == 1:
            sensor_x = 65
            sensor_y = 140
            sensor_angle = np.arctan(sensor_x/sensor_y) *180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] - sensor_angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)

        proj_x = x + dist*np.cos(pose[2]*np.pi/180)
        proj_y = y + dist*np.sin(pose[2]*np.pi/180)
        return proj_x, proj_y
    
    def no_overlaps(self, circle1, circle_list, dist_threshold=100):
        center_x1, center_y1, radius1 = circle1
        print(center_x1, center_y1)
        # check if outside of the walls/ is the wall
        if center_x1 <= 50 or center_x1 >= 1050 or  center_y1 <= 50 or center_y1 >= 1050:
            return False

        
        for circle2 in circle_list:
            center_x2, center_y2, radius2 = circle2
            center_x2, center_y2, radius2 = center_x2*10, center_y2*10, radius2*10 # convert to mm
            
            # Calculate the distance between the centers of the two circles
            distance = math.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)
            
            # Check if the circles overlap significantly
            if distance < dist_threshold:
                return False
        
        # No significant overlap found
        return True

def main():
    x_start = (30, 30)  # Starting node
    x_goal = (100.0, 100.0)  # Goal node
    eta = 2  # useless param it seems
    iter_max = 500

    env = Map()
    bit = BITStar(x_start, x_goal, eta, iter_max, env, show_animation=True)
    bit.add_obs_from_ultrasonic(100, 100)
    bit.add_obs_from_ultrasonic(800 , 800)

    path = bit.planning()

    bit.plot_grid("grid")
    print("Path waypoints:")
    print(path, len(path))

    path_2 = straighten_path(path, env, n_iterations=100)
    print("straightened Path waypoints:")
    print(path_2, len(path_2))


    x_coords = [x[0] for x in path]
    y_coords = [x[1] for x in path]
    plt.plot(x_coords, y_coords)

    x_coords = [x[0] for x in path_2]
    y_coords = [x[1] for x in path_2]
    plt.plot(x_coords, y_coords)
    plt.show()

if __name__ == "__main__":
    main()