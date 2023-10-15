import math
import random
import numpy as np

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


def smooth_path(path, obs_segments, n_iterations):
    
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


    smoothed_path = douglas_peucker_simplify(smoothed_path, epsilon=2)


    paths = []
    paths_len = []

    for k in range(3):
        
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
            
            if not path_intersects([point1, point2], obs_segments):
                smoothed_path = smoothed_path[:idx1 + 1] + smoothed_path[idx2:]
        paths.append(smoothed_path)
        paths_len.append(len(smoothed_path))
        

    return paths[np.argmin(paths_len)]




def onSegment(p, q, r): 
    if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
           (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))): 
        return True
    return False
  
def orientation(p, q, r): 
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Collinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 
      
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  
      
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
    if (val > 0): 
          
        # Clockwise orientation 
        return 1
    elif (val < 0): 
          
        # Counterclockwise orientation 
        return 2
    else: 
          
        # Collinear orientation 
        return 0
  
# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
  
    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1 
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1 
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
  
    # If none of the cases 
    return False

def path_intersects(path, obs_segments):
    if len(path) < 2: 
        return False

    for i in range(len(path)-1):
        p1 = path[i]
        q1 = path[i+1]

        for j in range(len(obs_segments)):
            p2 = obs_segments[j][0]
            q2 = obs_segments[j][1]

            if doIntersect(p1, q1, p2, q2):
                return True
    return False