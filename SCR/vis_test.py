import pygame
import time
class Robot:
    def __init__(self, pose, width):
        self.mm2p = 1
        
        self.w = width

        self.pose = pose


class Graphics:
    def __init__(self):
        pygame.init()
        self.robot_img_path = "robot_img.png"
        self.map_img_path = "map_img.png"
        self.scale = 0.5
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        self.robot = pygame.image.load(self.robot_img_path)
        self.map_img = pygame.image.load(self.map_img_path)

        self.height, self.width = (int(1200*self.scale), int(1200*self.scale))

        pygame.display.set_caption("visualisation")
        self.map = pygame.display.set_mode((self.width, self.height))

    
    def draw_robot(self, pose):
        rotated = pygame.transform.rotozoom(self.robot, pose[2]-90, self.scale)
        rect = rotated.get_rect(center = (pose[0], pose[1]))
        self.map.blit(rotated, rect)

    def draw_map(self):
        rotated = pygame.transform.rotozoom(self.map_img, 0, self.scale)
        rect = rotated.get_rect(center = (int(600*self.scale), int(600*self.scale)))
        self.map.blit(rotated, rect)

    def draw_obs(self, obs_list):
        for obs in obs_list:
            pygame.draw.circle(self.map,self.black,(int(obs[0]*self.scale),int(obs[1]*self.scale)),int(obs[2]*self.scale)) 

def main_vis_loop():
    gfx = Graphics()

    start = (150, 150, 0)
    robot_baseline = 220

    robot = Robot(start, robot_baseline)
    obs_list = [[600, 600, 100], [1000, 1000, 200]]


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        gfx.draw_map()
        gfx.draw_robot(robot.pose)
        gfx.draw_obs(obs_list)

        robot.pose = [robot.pose[0]+1, robot.pose[1]+1, robot.pose[2]+1]
        pygame.display.update()
        time.sleep(1/60)

if __name__=="__main__":
    main_vis_loop()