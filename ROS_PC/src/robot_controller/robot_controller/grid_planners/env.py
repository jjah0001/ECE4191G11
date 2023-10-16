class Env:
    def __init__(self, scaling):
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = set()
        self.obs_list_gfx = []
        self.obs_list_segments = []
        self.scaling = scaling
        self.clear_obs()

    def set_arena_size(self, width, height):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = width//self.scaling
        y = height//self.scaling

        

        # for i in range(x):
        #     self.obs.add((i, -1))
        # for i in range(x):
        #     self.obs.add((i, y - 1))

        # for i in range(y):
        #     self.obs.add((-1, i))
        # for i in range(y):
        #     self.obs.add((x - 1, i))

        wall_padding = 150//self.scaling

        # bottom wall
        for i in range(x):
            self.obs.add((i, wall_padding))

        # top wall
        for i in range(x):
            self.obs.add((i, y - 1-wall_padding))

        # left wall
        for i in range(y):
            self.obs.add((wall_padding, i))

        # right wall
        for i in range(y):
            self.obs.add((x - 1 -wall_padding, i))


    def add_square_obs(self, center_x, center_y, half_length):

        self.obs_list_gfx.append([center_x*self.scaling//10, center_y*self.scaling//10, half_length*self.scaling//10])

        side_length = half_length*2


        bottom_left_x = int((center_x - side_length//2))
        bottom_left_y = int((center_y - side_length//2))

         # bottom wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + i, bottom_left_y))
        self.obs_list_segments.append([[bottom_left_x*self.scaling, bottom_left_y*self.scaling], [(bottom_left_x+ side_length)*self.scaling, bottom_left_y*self.scaling]])

        # top wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + i, bottom_left_y + side_length))
        self.obs_list_segments.append([[bottom_left_x*self.scaling, (bottom_left_y+side_length)*self.scaling], [(bottom_left_x+ side_length)*self.scaling, (bottom_left_y+side_length)*self.scaling]])

        # left wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x, bottom_left_y + i))
        self.obs_list_segments.append([[bottom_left_x*self.scaling, bottom_left_y*self.scaling], [bottom_left_x*self.scaling, (bottom_left_y+side_length)*self.scaling]])

        # right wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + side_length, bottom_left_y + i))
        self.obs_list_segments.append([[(bottom_left_x+side_length)*self.scaling, bottom_left_y*self.scaling], [(bottom_left_x+ side_length)*self.scaling, (bottom_left_y+side_length)*self.scaling]])
        
    def clear_obs(self):
        self.obs = set()
        self.obs_list_gfx = []
        self.obs_list_segments = []


        self.set_arena_size(1200, 1200)

        bottom_left_x = 800//self.scaling
        bottom_left_y = 0

        side_length = 400//self.scaling

         # bottom wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + i, bottom_left_y))
        self.obs_list_segments.append([[bottom_left_x*self.scaling, bottom_left_y*self.scaling], [(bottom_left_x+ side_length)*self.scaling, bottom_left_y*self.scaling]])

        # top wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + i, bottom_left_y + side_length))
        self.obs_list_segments.append([[bottom_left_x*self.scaling, (bottom_left_y+side_length)*self.scaling], [(bottom_left_x+ side_length)*self.scaling, (bottom_left_y+side_length)*self.scaling]])

        # left wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x, bottom_left_y + i))
        self.obs_list_segments.append([[bottom_left_x*self.scaling, bottom_left_y*self.scaling], [bottom_left_x*self.scaling, (bottom_left_y+side_length)*self.scaling]])

        # right wall
        for i in range(int(side_length)):
            self.obs.add((bottom_left_x + side_length, bottom_left_y + i))
        self.obs_list_segments.append([[(bottom_left_x+side_length)*self.scaling, bottom_left_y*self.scaling], [(bottom_left_x+ side_length)*self.scaling, (bottom_left_y+side_length)*self.scaling]])
        