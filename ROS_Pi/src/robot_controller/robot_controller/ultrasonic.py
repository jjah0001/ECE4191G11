import RPi.GPIO as GPIO   
from map_bit import Map
from env import Env
import time
import numpy as np

class Ultrasonic:
    def __init__(self, mode, obs_shape, obs_radius):
        GPIO.setmode(GPIO.BCM)
        self.empty_buffer_count = 0
        #set GPIO Pins
        self.GPIO_TRIGGER = 27
        self.GPIO_ECHO = 17
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        self.GPIO_TRIGGER_2 = 2
        self.GPIO_ECHO_2 = 3

        GPIO.setup(self.GPIO_TRIGGER_2, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_2, GPIO.IN)

        self.GPIO_TRIGGER_3 = 19
        self.GPIO_ECHO_3 = 13

        GPIO.setup(self.GPIO_TRIGGER_3, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_3, GPIO.IN)


        self.mode = mode
        self.obs_shape = obs_shape
        self.obs_radius = obs_radius
        

        if self.mode == "A*":
            map_size = [1200, 1200]
            self.scaling = 5
            self.map = Env()
            self.map.set_arena_size(map_size[0]//self.scaling, map_size[1]//self.scaling)

        elif self.mode == "BIT*":
            self.map = Map()



    def get_distances(self):
        """
        Method to get the distance measurements from all 3 ultrasonic sensors
        """
        print("get_distances")
        sensor1 = float(self.get_distance(0)*10)
        print( "bye")
        time.sleep(0.01)
        sensor2 = float(self.get_distance(1)*10)
        time.sleep(0.01)
        sensor3 = float(self.get_distance(2)*10)

        return sensor1, sensor2, sensor3

    def get_distance(self, sensor):
        """
        Method to get the disance measurement from a specified ultrasonic sensor
        """
        print("hi")
        if sensor == 0:
            trig = self.GPIO_TRIGGER
            echo = self. GPIO_ECHO
        elif sensor ==1:
            trig = self.GPIO_TRIGGER_2
            echo = self. GPIO_ECHO_2
        elif sensor == 2:
            trig = self.GPIO_TRIGGER_3
            echo = self. GPIO_ECHO_3

        # set Trigger to HIGH
        GPIO.output(trig, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trig, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        no_echo = False
        # save StartTime
        start_start_time = StartTime
        while GPIO.input(echo) == 0:
            if time.time() - start_start_time > 0.2: 
                break
            StartTime = time.time()
    
        if not no_echo:
            # save time of arrival
            while GPIO.input(echo) == 1:
                StopTime = time.time()
    
    
        
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            # self.get_logger().info("time between emission and detection: " + str(TimeElapsed))
            distance = (TimeElapsed * 34300) / 2
            # self.get_logger().info("distance recorded: " + str(distance))
            if distance >= 200:
                return -999.0
            return distance
        else:
            return -999.0

    
    def get_average_distance(self, sensor):
        """
        Method for getting the average distance measurement from a specified ultrasonic sensor
        """
        distance_array = []
        while True:
            dist = self.get_distance(sensor)

            if dist > 0 and dist < 200:
                distance_array.append(dist)
                self.get_logger().info(str(dist))
                if len(distance_array) >3:
                    distance_array.pop(0)

            length = len(distance_array)
            if length == 3 and self.check_consistent_distance(distance_array):
                return sum(distance_array)/length

    def check_consistent_distance(self, distance_array):
        """
        AUX method for checking distances in array are consistent
        """
        if abs(distance_array[0] - distance_array[1]) < 2 and abs(distance_array[0] - distance_array[2]) < 2:
            return True
        else:
            return False

    def add_obs_from_ultrasonic(self, dist1, dist2, dist3=None):
        """
        Method for checking for obstacles and adding onto map
        """
        obs_added = False
        obs = [[],[],[]]
        if dist1 is not None and dist1 >= 10 and dist1 <= 200:
            proj_x, proj_y = self.project_coords(0, self.pose, dist1)
            if self.no_overlaps([proj_x, proj_y, self.obs_radius], self.map.obs_circle, 100):
                # self.get_logger().info("Sensor left: Obs added: (" + str(proj_x) + ", " + str(proj_y) + ")")
                self.add_obs(proj_x, proj_y, self.obs_radius)
                obs_added = True
                obs[0] = [proj_x, proj_y, self.obs_radius]

        if dist2 is not None and dist2 >= 10 and dist2 <= 200:
            proj_x, proj_y = self.project_coords(1, self.pose, dist2)
            if self.no_overlaps([proj_x, proj_y, self.obs_radius], self.map.obs_circle, 100):
                # self.get_logger().info("Sensor right: Obs added: (" + str(proj_x) + ", " + str(proj_y) + ")")
                self.add_obs(proj_x, proj_y, self.obs_radius)
                obs_added = True
                obs[1] = [proj_x, proj_y, self.obs_radius]
        
        if dist3 is not None and dist3 >= 10 and dist3 <= 200:
            proj_x, proj_y = self.project_coords(1, self.pose, dist3)
            if self.no_overlaps([proj_x, proj_y, self.obs_radius], self.map.obs_circle, 100):
                # self.get_logger().info("Sensor right: Obs added: (" + str(proj_x) + ", " + str(proj_y) + ")")
                self.add_obs(proj_x, proj_y, self.obs_radius)
                obs_added = True
                obs[2] = [proj_x, proj_y, self.obs_radius]

        return obs, obs_added

    def add_obs(self, center_x, center_y, r_or_l):
        """
        Method for adding a obstacle onto the map given coords
        """
        if self.mode == "A*":
            x = max(center_x//self.scaling, 1)
            y = max(center_y//self.scaling, 1)
            w = max(r_or_l//self.scaling, 1)
            self.map.add_square_obs(x, y, w)
        elif self.mode == "BIT*":
            
            self.map.add_obs_cirlce(center_x, center_y, r_or_l)
    
    def project_coords(self, sensor, pose, dist):
        """
        method for projecting obs coords based on sensor location
        """
        
        if sensor == 0:
            sensor_x = 85
            sensor_y = 140  
            angle = 10
            sensor_angle = np.arctan(sensor_x/sensor_y + angle)*180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] + sensor_angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)
        elif sensor == 1:
            sensor_x = 85
            sensor_y = 140
            angle = -10
            sensor_angle = np.arctan(sensor_x/sensor_y) *180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] - sensor_angle + angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)
        elif sensor == 2:
            sensor_x = 0
            sensor_y = 140
            angle = 0
            sensor_angle = np.arctan(sensor_x/sensor_y) *180/np.pi
            distance_from_robot_center = np.sqrt(sensor_x**2 + sensor_y**2)

            total_angle_rad = (pose[2] - sensor_angle + angle) *np.pi/180
            x = pose[0] + distance_from_robot_center * np.cos(total_angle_rad)
            y = pose[1] + distance_from_robot_center * np.sin(total_angle_rad)


        proj_x = x + dist*np.cos(pose[2]*np.pi/180)
        proj_y = y + dist*np.sin(pose[2]*np.pi/180)
        return proj_x, proj_y
    
    def no_overlaps(self, circle1, circle_list, dist_threshold=100):
        """
        method for checking if any obstacles significantly overlap, e.g. repeated obs
        """
        center_x1, center_y1, radius1 = circle1
        
        # check if outside of the walls/ is the wall
        if center_x1 <= 75 or center_x1 >= 1125 or  center_y1 <= 75 or center_y1 >= 1125:
            return False
        
        for circle2 in circle_list:
            center_x2, center_y2, radius2 = circle2
            center_x2, center_y2, radius2 = center_x2*10, center_y2*10, radius2*10 # convert to mm
            
            # Calculate the distance between the centers of the two circles
            distance = np.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)
            
            # Check if the circles overlap significantly
            if distance < dist_threshold:
                return False
        
        # No significant overlap found
        return True