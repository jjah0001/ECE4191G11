import math
# from rclpy.node import Node
import time
# from robot_interfaces.msg import Waypoint
import numpy as np
import matplotlib.pyplot as plt

class Map:
    def __init__(self, length, width, cell_size=1):
        '''

        :param length: x coordinate
        :param width: y coordinate
        :param cell_size: size of coordinate squares
        '''
        self.width = width
        self.length = length
        self.cell_size = cell_size
        self.grid_width = int(width / cell_size)
        self.grid_length = int(length / cell_size)
        self.grid = [[0.5 for _ in range(self.grid_length)] for _ in range(self.grid_width)]

    def add_obstacle(self, x, y):
        grid_x = int(x / self.cell_size)
        grid_y = int(y / self.cell_size)
        if 0 <= grid_x < self.grid_length and 0 <= grid_y < self.grid_width:
            self.grid[grid_y][grid_x] = 0.0

    def get_value(self, x, y):
        grid_x = int(x / self.cell_size)
        grid_y = int(y / self.cell_size)
        if 0 <= grid_x < self.grid_length and 0 <= grid_y < self.grid_width:
            return self.grid[grid_y][grid_x]
        else:
            return None

    def visualise_map(self):
        map_data = np.array(self.grid)
        plt.imshow(map_data, origin='lower', cmap='gray', extent=(0, self.length, 0, self.width))
        plt.xlabel('X (mm)')
        plt.ylabel('Y (mm)')
        plt.colorbar(label='Occupancy Probability')
        plt.title('Map')
        plt.show()

# Main
if __name__ == "__main__":
    # Creates a grid of 1200mm x 1200mm with cell size of 10mm
    # Grid will comprise of 120 x 120 coordinates
    map_node = Map(length=1200, width=1200, cell_size=10)
    map_node.add_obstacle(600, 600)
    map_node.visualise_map()

