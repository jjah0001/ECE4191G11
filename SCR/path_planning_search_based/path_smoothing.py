import math

# Calculate the perpendicular distance from a point to a line segment
def point_to_line_distance(point, start, end):
    line_length = math.dist(start, end)
    if line_length == 0:
        return math.dist(point, start)
    
    t = ((point[0] - start[0]) * (end[0] - start[0]) + (point[1] - start[1]) * (end[1] - start[1])) / (line_length ** 2)
    t = max(0, min(1, t))
    
    projection = (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
    return math.dist(point, projection)

# Recursive Douglas-Peucker simplification
def douglas_peucker_simplify(path, epsilon):
    dmax = 0
    index = 0
    
    for i in range(1, len(path) - 1):
        d = point_to_line_distance(path[i], path[0], path[-1])
        if d > dmax:
            index = i
            dmax = d
    
    if dmax > epsilon:
        recursive_result1 = douglas_peucker_simplify(path[:index + 1], epsilon)
        recursive_result2 = douglas_peucker_simplify(path[index:], epsilon)
        simplified_path = recursive_result1[:-1] + recursive_result2
    else:
        simplified_path = [path[0], path[-1]]
    
    return simplified_path


def smooth_path(path):
    
    if len(path) <= 2:
        return path # path already smoothed

    smoothed_path = path
    # current_dir = [path[1][0] - path[0][0], path[1][1] - path[0][1]]
    # smoothed_path = [path[0]]
    # for i in range(2, len(path)):
    #     if [path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]] != current_dir:
    #         smoothed_path.append(path[i-1])
    #         current_dir = [path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]]
    # smoothed_path.append(path[-1])


    smoothed_path = douglas_peucker_simplify(smoothed_path, epsilon=1)

    return smoothed_path
