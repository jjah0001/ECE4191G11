class Map:
    def __init__(self):
        self.x_range = (0, 120-15)
        self.y_range = (0, 120-15)
        self.obs_boundary = [
            [0, 0, 15, 120],
            [0, 120, 120, -15],
            [0, 0, 120, 15],
            [120, 0, -15, 120],
        ]
        self.obs_circle = []
        self.obs_rectangle = []
    
    def add_obs_circle(self, x, y, r):
        self.obs_circle.append([x/10, y/10, r/10])


    def add_obs_rectangle(self, center_x, center_y, half_length):

        bottom_left_x = int((center_x - half_length))
        bottom_left_y = int((center_y - half_length))
        

        self.obs_rectangle.append([bottom_left_x/10, bottom_left_y/10, half_length*2/10, half_length*2/10])

    