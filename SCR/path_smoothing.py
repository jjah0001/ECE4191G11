
import numpy as np
from scipy.interpolate import CubicSpline


def smooth_path(path, map):
    # Grab the path coordinates and the map

    # If the path has less than 3 waypoints, already smoothed
    if len(path < 3):
        return path

    # Epsilon is the level of smoothing we want the path to have
    epsilon = 0.5

    # Calculate the smoothed path
    smoothed_path = rdp(path, 0, len(path) - 1, epsilon)

    waypoints_x = np.array([point[0] for point in smoothed_path])
    waypoints_y = np.array([point[1] for point in smoothed_path])

    # Get the obstacles from the map - Circles in the form of [(x, y), r]

    obstacles = []

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
    number_of_waypoints = 10

    # Convert the obstacle constraints into penalty terms
    def penalty_term(xi, yi):
        penalty = 0
        for center, radius in obstacles:
            distance_to_obstacle = np.sqrt((xi - center[0])**2 + (yi - center[1])**2)
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
