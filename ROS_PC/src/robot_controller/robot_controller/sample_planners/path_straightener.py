
import numpy as np
from scipy.interpolate import CubicSpline
import random
import math

def smooth_path(path, map):
    # Grab the path coordinates and the map

    # If the path has less than 3 waypoints, already smoothed
    if len(path) < 3:
        return path

    # Epsilon is the level of smoothing we want the path to have
    epsilon = 0.5

    # Calculate the smoothed path
    smoothed_path = rdp(path, 0, len(path) - 1, epsilon)

    waypoints_x = np.array([point[0] for point in smoothed_path])
    waypoints_y = np.array([point[1] for point in smoothed_path])

    # Get the obstacles from the map - Circles in the form of [(x, y), r]

    obstacles = map.obs_circle

    smoothed_path_with_obstacle_avoidance = obstacle_avoidance(waypoints_x, waypoints_y, obstacles)

    # return smoothed path
    return smoothed_path_with_obstacle_avoidance


def perpendicular_distance(p, a, b):
    return abs((b[1] - a[1]) * p[0] - (b[0] - a[0]) * p[1] + b[0] * a[1] - b[1] * a[0]) / ((b[1] - a[1])**2 +
                                                                                           (b[0] - a[0])**2)**0.5


def rdp(points, start_idx, end_idx, epsilon=0.5):
    # If the points are separated by one, return the two points
    if end_idx - start_idx <= 1:
        return [points[start_idx], points[end_idx]]

    max_distance = 0
    farthest_idx = start_idx

    # Iterate through all points between start and end indices
    for i in range(start_idx + 1, end_idx):
        # Calculate the perpendicular distance of points[i] from a line segment (points[start_idx], points[end_idx])
        distance = perpendicular_distance(points[i], points[start_idx], points[end_idx])

        if distance > max_distance:
            max_distance = distance
            farthest_idx = i

    # If the max distance is less than the smoothing parameter, return the start/end idx
    if max_distance < epsilon:
        return [points[start_idx], points[end_idx]]

    # Compute the smoothing for the smaller segments of the path
    left = rdp(points, start_idx, farthest_idx)
    right = rdp(points, farthest_idx, end_idx)

    return left + right[1:]


def obstacle_avoidance(x, y, obstacles):
    # Might want to adjust the number of points needed to be at most ~10
    number_of_waypoints = 20

    # Convert the obstacle constraints into penalty terms
    def penalty_term(xi, yi):
        penalty = 0
        for center_x, center_y, radius in obstacles:
            distance_to_obstacle = np.sqrt((xi - center_x)**2 + (yi - center_y)**2)
            if distance_to_obstacle < radius:
                penalty += (1 - distance_to_obstacle / radius) ** 2
        return penalty

    penalties = np.array([penalty_term(xi, yi) for xi, yi in zip(x, y)])

    # Now perform the cubic spline interpolation with the penalty constraints
    cs_y = CubicSpline(x, y - penalties, bc_type='natural', extrapolate=False, axis=0)

    smoothed_x = np.linspace(x[0], x[-1], number_of_waypoints)  # Adjust the number of points as needed
    smoothed_y = cs_y(smoothed_x)

    waypoints = [(x, y) for x, y in zip(smoothed_x, smoothed_y)]

    return waypoints

# Function to check collision with circle obstacles
def is_collision_free(point1, point2, obstacles):
    for obstacle in obstacles:
        center = (obstacle[0], obstacle[1])
        radius = obstacle[2]-0.2 #removing from radius to get slightly better paths, 
                                 #since our obstacle radius will be over estimated anyway
        
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        
        # Vector between the start point of the line and the center of the circle
        diff_x = point1[0] - center[0]
        diff_y = point1[1] - center[1]
        
        # Calculate coefficients for the quadratic equation
        a = dx**2 + dy**2
        b = 2 * (dx * diff_x + dy * diff_y)
        c = diff_x**2 + diff_y**2 - radius**2
        
        # Calculate the discriminant
        discriminant = b**2 - 4 * a * c
        
        if discriminant >= 0:
            # If the discriminant is non-negative, there is an intersection
            t1 = (-b + math.sqrt(discriminant)) / (2 * a)
            t2 = (-b - math.sqrt(discriminant)) / (2 * a)
            
            # Check if the intersection points are within the line segment
            if 0 <= t1 <= 1 or 0 <= t2 <= 1:
                return False  # Intersection detected
    
    return True  # No intersection


# RRT-based path smoothing
def straighten_path(path, map, n_iterations):

    obstacles = map.obs_circle

    paths = []
    paths_len = []

    for k in range(3):
        smoothed_path = path.copy()
        
        for i in range(n_iterations):

            if len(smoothed_path) <=2: #already smoothened
                break

            idx1 = random.randint(0, len(smoothed_path) - 1)
            idx2 = random.randint(0, len(smoothed_path) - 1)
            
            if idx1 == idx2:
                continue

            point1 = smoothed_path[idx1]
            point2 = smoothed_path[idx2]

            
            if idx1 > idx2:
                idx1, idx2 = idx2, idx1
                point1, point2 = point2, point1
            
            if is_collision_free(point1, point2, obstacles):
                smoothed_path = smoothed_path[:idx1 + 1] + smoothed_path[idx2:]
        paths.append(smoothed_path)
        paths_len.append(len(smoothed_path))
        

    return paths[np.argmin(paths_len)]
