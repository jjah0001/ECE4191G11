class Env:
    def __init__(self):
        self.x_range = (0, 120)
        self.y_range = (0, 120)
        self.obs_boundary = [
            [0, 0, 1, 120],
            [0, 120, 120, 1],
            [1, 0, 120, 1],
            [120, 1, 1, 120]
        ]
        self.obs_circle = [

        ]

        self.obs_rectangle = []
    