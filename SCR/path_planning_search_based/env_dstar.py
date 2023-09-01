class Env:
    def __init__(self):
        self.x_range = 1200
        self.y_range = 1200
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = set()

    def set_arena_size(self, width, height):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = width
        y = height

        for i in range(x):
            self.obs.add((i, 0))
        for i in range(x):
            self.obs.add((i, y - 1))

        for i in range(y):
            self.obs.add((0, i))
        for i in range(y):
            self.obs.add((x - 1, i))


    def add_square_obs(self, center_x, center_y, side_length):
        bottom_left_x = int((center_x - side_length//2))
        bottom_left_y = int((center_y - side_length//2))

        for i in range(int(side_length)):
            self.obs.add((bottom_left_x, bottom_left_y +i))
            self.obs.add((bottom_left_x + side_length, bottom_left_y +i))

        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + i, bottom_left_y))
            self.obs.add((bottom_left_x + i, bottom_left_y +side_length))
                
