import pygame

class Graphics:
    def __init__(self):
        pygame.init()
        self.robot_img_path = "/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/robot_img.png"
        self.partner_robot_img_path = "/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/partner_robot_img.png"
        self.map_img_path = "/home/lingc/ECE4191G11/ROS_PC/src/robot_controller/robot_controller/map_img.png"
        self.scale = 0.5
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.lred = (255, 51, 51)
        self.yel = (255, 255, 0)

        self.robot = pygame.image.load(self.robot_img_path)
        self.partner_robot = pygame.image.load(self.partner_robot_img_path)
        self.map_img = pygame.image.load(self.map_img_path)

        self.height, self.width = (int(1200*self.scale), int(1200*self.scale))

        pygame.display.set_caption("visualisation")
        self.map = pygame.display.set_mode((self.width, self.height))

    
    def draw_robot(self, pose):
        rotated = pygame.transform.rotozoom(self.robot, pose[2]-90, self.scale)
        rect = rotated.get_rect(center = self.to_pygame_coord((int(pose[0]*self.scale), int(pose[1]*self.scale))))
        self.map.blit(rotated, rect)

    def draw_partner_robot(self, pose):
        rotated = pygame.transform.rotozoom(self.partner_robot, pose[2]-90, self.scale)
        rect = rotated.get_rect(center = self.to_pygame_coord((int(pose[0]*self.scale), int(pose[1]*self.scale))))
        self.map.blit(rotated, rect)

    def draw_map(self):
        rotated = pygame.transform.rotozoom(self.map_img, 0, self.scale)
        rect = rotated.get_rect(center = (int(600*self.scale), int(600*self.scale)))
        self.map.blit(rotated, rect)

    def draw_obs(self, obs_list):
        for obs in obs_list:
            pygame.draw.circle(self.map,self.black, self.to_pygame_coord((int(obs[0]*10*self.scale),int(obs[1]*10*self.scale))),int((obs[2]-15)*10*self.scale))
    
    def draw_square_obs(self, obs_list):
        for obs in obs_list:
            top_left_x, top_left_y = self.to_pygame_coord(  [(obs[0]-obs[2])*10 *self.scale, (obs[1] + obs[2])*10 *self.scale] )
            width = obs[2]*2*10*self.scale
            height = obs[2]*2*10*self.scale
            pygame.draw.rect(self.map, self.lred, [top_left_x, top_left_y, width, height], 0)

    def draw_path(self, pose, path):
        if path is None or len(path) == 0:
            return
        path = [self.to_pygame_coord((p[0]*self.scale, p[1]*self.scale)) for p in path]
        path.insert(0,self.to_pygame_coord((pose[0]*self.scale,pose[1]*self.scale)))
        pygame.draw.lines(self.map, self.green, False, path, 4)

    def draw_goals(self):
        pygame.draw.line(self.map, self.blue, self.to_pygame_coord([15*self.scale, 1200*self.scale]), self.to_pygame_coord([285*self.scale, 1200*self.scale]), 8)
        pygame.draw.line(self.map, self.blue, self.to_pygame_coord([(1200-15)*self.scale, 1200*self.scale]), self.to_pygame_coord([(1200-285)*self.scale, 1200*self.scale]), 8)
        pygame.draw.line(self.map, self.blue, self.to_pygame_coord([465*self.scale, 1200*self.scale]), self.to_pygame_coord([(465+270)*self.scale, 1200*self.scale]), 8)
    def to_pygame_coord(self, coords):
        return (coords[0], self.height-coords[1])
    
    def draw_partner_path(self, partner_pose, partner_goal):
        if partner_goal is not None:
            path = [self.to_pygame_coord((partner_goal[0]*self.scale,partner_goal[1]*self.scale))]
            path.insert(0,self.to_pygame_coord((partner_pose[0]*self.scale,partner_pose[1]*self.scale)))
            pygame.draw.lines(self.map, self.red, False, path, 4)