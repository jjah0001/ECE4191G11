class Map:
    def __init__(self):
        self.x_range = (0, 120)
        self.y_range = (0, 120)
        self.obs_boundary = [
            [0, 0, 0, 120],
            [0, 120, 120, 0],
            [1, 0, 120, 0],
            [120, 0, 0, 120]
        ]
        self.obs_circle = []
        self.obs_rectangle = []
    
    def add_obs_cirlce(self, x, y, r):
        self.obs_circle.append([x/10, y/10, r/10])


    def add_obs_rectangle(self, x, y, w, h):
        self.obs_rectangle.append([x/10, y/10, w/10, h/10])

    