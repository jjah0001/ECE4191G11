import math
# from rclpy.node import Node
import time
# from robot_interfaces.msg import Waypoint
import numpy as np
import matplotlib.pyplot as plt

# Coordinates from [0 - 1199][0 - 1199]
class Map:
    def __init__(self, length, width, cell_size=10, robot_initial_position=(150, 150)):
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
        self.grid = [[1 for _ in range(self.grid_length)] for _ in range(self.grid_width)]
        self.previous_robot_position = robot_initial_position
        self.update_robot_position(robot_initial_position[0], robot_initial_position[1])
        self.set_walls()

    def update_robot_position(self, x, y, radius=100):
        radius_in_cells = int(radius / self.cell_size)

        if self.previous_robot_position:
            prev_grid_x, prev_grid_y = self.get_grid_coordinates(self.previous_robot_position[0], self.previous_robot_position[1])
            for dx in range(-radius_in_cells, radius_in_cells + 1):
                for dy in range(-radius_in_cells, radius_in_cells + 1):
                    new_grid_x = prev_grid_x + dx
                    new_grid_y = prev_grid_y + dy
                    if 0 <= new_grid_x < self.grid_length and 0 <= new_grid_y < self.grid_width:
                        self.grid[new_grid_y][new_grid_x] = 1.0

        grid_x, grid_y = self.get_grid_coordinates(x, y)
        self.grid[grid_y][grid_x] = 0.5
        self.previous_robot_position = (x, y)

        for dx in range(-radius_in_cells, radius_in_cells + 1):
            for dy in range(-radius_in_cells, radius_in_cells + 1):
                new_grid_x = grid_x + dx
                new_grid_y = grid_y + dy
                if 0 <= new_grid_x < self.grid_length and 0 <= new_grid_y < self.grid_width:
                    self.grid[new_grid_y][new_grid_x] = 0.5

    def get_grid_coordinates(self, x, y):
        grid_x = int(x / self.cell_size)
        grid_y = int(y / self.cell_size)
        return grid_x, grid_y

    def set_walls(self):
        for x in range(self.grid_length):
            self.grid[0][x] = 0.0
            self.grid[self.grid_length - 1][x] = 0.0

        for y in range(self.grid_width):
            self.grid[y][0] = 0.0
            self.grid[y][self.grid_width - 1] = 0.0

    def add_obstacle(self, x, y, radius):
        '''
        Adds an obstacle to the map with a specified radius
        Not sure if we want this to be a square obstacle or a circle
        '''
        grid_x, grid_y = self.get_grid_coordinates(x, y)
        radius_in_cells = int(radius / self.cell_size)

        # Square implementation
        # for dx in range(-radius_in_cells, radius_in_cells + 1):
        #     for dy in range(-radius_in_cells, radius_in_cells + 1):
        #         new_grid_x = grid_x + dx
        #         new_grid_y = grid_y + dy
        #         if 0 <= new_grid_x < self.grid_length and 0 <= new_grid_y < self.grid_width:
        #             self.grid[new_grid_y][new_grid_x] = 0.0

        # Circle implementation involves more processing
        for dx in range(-radius_in_cells, radius_in_cells + 1):
            for dy in range(-radius_in_cells, radius_in_cells + 1):
                new_grid_x = grid_x + dx
                new_grid_y = grid_y + dy
                if 0 <= new_grid_x < self.grid_length and 0 <= new_grid_y < self.grid_width:
                    cell_center_x = (new_grid_x + 0.5) * self.cell_size
                    cell_center_y = (new_grid_y + 0.5) * self.cell_size
                    if (cell_center_x - x)**2 + (cell_center_y - y)**2 <= radius**2:
                        self.grid[new_grid_y][new_grid_x] = 0.0


    def get_value(self, x, y):
        grid_x, grid_y = self.get_grid_coordinates(x, y)
        if 0 <= grid_x < self.grid_length and 0 <= grid_y < self.grid_width:
            return self.grid[grid_y][grid_x]
        else:
            return None

    def visualise_map(self):
        map_data = np.array(self.grid)
        plt.clf()
        plt.imshow(map_data, origin='lower', cmap='gray', extent=(0, self.length, 0, self.width))
        plt.xlabel('X (mm)')
        plt.ylabel('Y (mm)')
        plt.colorbar(label='Occupancy Probability')
        plt.title('Map')
        plt.pause(0.01)
        plt.draw()

# Main
if __name__ == "__main__":
    # Creates a grid of 1200mm x 1200mm with cell size of 10mm
    # Grid will comprise of 120 x 120 coordinates
    map_node = Map(length=1200, width=1200, cell_size=10, robot_initial_position=(150, 150))
    map_node.add_obstacle(400, 600, 40)

    try:
        while True:
            new_robot_position_x = float(input("Enter new robot x position: "))
            new_robot_position_y = float(input("Enter new robot y position: "))
            check_if_new_obstacle = (input("Do you want to add another obstacle? [Y/N] "))
            if (check_if_new_obstacle == "Y"):
                new_obstacle_position_x = float(input("Enter new obstacle x position: "))
                new_obstacle_position_y = float(input("Enter new obstacle y position: "))
                new_obstacle_radius = float(input("Enter obstacle radius: "))
                map_node.add_obstacle(new_obstacle_position_x, new_obstacle_position_y, new_obstacle_radius)

            map_node.update_robot_position(new_robot_position_x, new_robot_position_y)
            map_node.visualise_map()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Map visualisation ended.")




