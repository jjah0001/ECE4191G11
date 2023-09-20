import RPi.GPIO as GPIO          
import time
import numpy as np

from encoder import Encoder

class Motor:
    def __init__(self):
        # Setting up GPIO
        self.in1 = 23
        self.in2 = 24

        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)


        self.in3 = 7
        self.in4 = 8

        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

        ############################################# INITIALISATION: ENCODER ###########################
        self.encoders = Encoder()

    def encoder_loop(self):
        self.encoders.detectEncoder()

    def _start_motor(self, motor, direction):
        """
        Set speed and direction for selected motor

        :param motor:  Either 0 or 1 to select motor
        :param direction: "forward" or "reverse"
        :param speed: 0-100%
        
        """

        if motor == 0:
            if direction == "forward":
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif direction == "reverse":
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
            else:
                self.get_logger().error("The direction is invalid")
                raise Exception("Invalid direction")
            
        elif motor == 1:
            if direction == "forward":
                GPIO.output(self.in3,GPIO.HIGH)
                GPIO.output(self.in4,GPIO.LOW)
            elif direction == "reverse":
                GPIO.output(self.in3,GPIO.LOW)
                GPIO.output(self.in4,GPIO.HIGH)
            else:
                self.get_logger().error("The direction is invalid")
                raise Exception("Invalid direction")
        else:
            self.get_logger().error("The motor is invalid")
            raise Exception("Invalid motor selected")
        
    def _stop_motor(self, motor):
        if motor == 0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)
        elif motor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)
        else:
            self.get_logger().error("The motor is invalid")
            raise Exception("Invalid motor selected")
    
    def rotate(self, direction):
        """
        Rotate at a specified speed in either direction
        :param direction: "CW" or "CCW"
        :param speed: 0-100%
        """
        # self.get_logger().info("Robot rotates " + direction + " with Input speed: " + str(speed))

        if direction == "CCW":
            # self.get_logger().info("Rotating CCW")
            self._start_motor(0, "forward")
            self._start_motor(1, "reverse")
        elif direction == "CW":
            # self.get_logger().info("Rotating CW")
            self._start_motor(0, "reverse")
            self._start_motor(1, "forward")
        else:
            self.get_logger().info("Invalid direction")
            raise Exception("Invalid direction")
        
    def drive_forwards(self, duration=None):
        """
        Drive forwards at a specified speed. If duration is given, stops after a certain time
        
        """
        # self.get_logger().info("Robot drives forward with Input speed: " + str(speed) + " Input duration: " + str(duration))
        
        self._start_motor(0, "forward")
        self._start_motor(1, "forward")

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float):
                time.sleep(duration)
                self.stop()
            else:
                self.get_logger().error("The duration is invalid")
                raise Exception("Invalid duration")
        
    def drive_backwards(self, duration=None):
        # self.get_logger().info("Robot drives backwards with Input speed: " + str(speed) + " Input duration: " + str(duration))
        
        self._start_motor(0, "reverse")
        self._start_motor(1, "reverse")

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float):
                time.sleep(duration)
                self._stop_motor(0)
                self._stop_motor(1)
            else:
                self.get_logger().error("The duration is invalid")
                raise Exception("Invalid duration")
    
    def stop(self):
        # self.get_logger().info("Motor stopped")
        self._stop_motor(0)
        self._stop_motor(1)

    def drive_distance(self, distance):
        """
        Drives a distance specified in milimetres at a specified speed   
        
        """

        current_target_waypoint = [0, 0]
        current_target_waypoint[0], current_target_waypoint[1] = self.target_waypoint

        # 170mm per revolution, per 3600 count
        DISTANCE_PER_COUNT = self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV
        original_pose = [0, 0, 0]
        original_pose[0], original_pose[1], original_pose[2] = self.pose #have to do it this way to hard copy arr
        
        left_encoder_start = self.left_encoder_count
        right_encoder_start = self.right_encoder_count


        total_count = 0
        count_required = (distance/self.WHEEL_CIRCUMFERENCE)*self.COUNTS_PER_REV

        # self.get_logger().info("To travel the specified distance, encoder needs to count " + str(count_required) + " times.")

        self.drive_forwards()
        while total_count < count_required:
            if self.obs_detected or self.target_waypoint[0] != current_target_waypoint[0] or self.target_waypoint[1] != current_target_waypoint[1]:
                self.stop()
                raise Exception("target waypoint changed")

            left_count = self.left_encoder_count - left_encoder_start
            right_count = self.right_encoder_count - right_encoder_start
            total_count = (left_count + right_count)//2
            self.pose[0] = original_pose[0] + DISTANCE_PER_COUNT * np.cos(self.pose[2] * (np.pi/180)) * total_count
            self.pose[1] = original_pose[1] + DISTANCE_PER_COUNT * np.sin(self.pose[2] * (np.pi/180)) * total_count
            

        distance_travelled = total_count*(self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)
        self.stop()
        # self.get_logger().info("Robot wheel has rotated " + str(deg) + " degrees and travelled a distance of " + str(distance_travelled) + " mm.")

    def rotate_angle(self, angle):
        """
        rotates a specified angle in degrees at a specified speed   
        
        """

        current_target_waypoint = [0, 0]
        current_target_waypoint[0], current_target_waypoint[1] = self.target_waypoint


        MM_PER_DEG = self.WHEEL_BASELINE*np.pi / 360
        ANGLE_PER_COUNT = (self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)/MM_PER_DEG

        original_pose = [0, 0, 0]
        original_pose[0], original_pose[1], original_pose[2] = self.pose #have to do it this way to hard copy arr

        left_encoder_start = self.left_encoder_count
        right_encoder_start = self.right_encoder_count

        total_count = 0
        count_required = ((abs(angle) * MM_PER_DEG)/self.WHEEL_CIRCUMFERENCE) * self.COUNTS_PER_REV

        # self.get_logger().info("To rotate the specified angle, encoder needs to count " + str(count_required) + " times.")

        if angle > 0:
            self.rotate("CCW")
        elif angle < 0:
            self.rotate("CW")

        
        while total_count < count_required:
            if self.obs_detected or self.target_waypoint[0] != current_target_waypoint[0] or self.target_waypoint[1] != current_target_waypoint[1]:
                self.stop()
                raise Exception("target waypoint changed")
            
            left_count = self.left_encoder_count - left_encoder_start
            right_count = self.right_encoder_count - right_encoder_start
            total_count = (left_count + right_count)//2
            self.pose[2] = original_pose[2] + ANGLE_PER_COUNT* np.sign(angle) * total_count

        deg_rotated = total_count*ANGLE_PER_COUNT
        self.stop()
        # self.get_logger().info("Robot has rotated an angle of " + str(deg_rotated) + " degs.")


    def _calculate_rotation(self, waypoint):
        """
        Calculates rotation needed in degrees to point towards the desired waypoint from the current pose
        """
        current_x, current_y, current_theta = self.pose
        des_x, des_y = waypoint

        dy = des_y - current_y
        dx = des_x - current_x

        desired_theta = np.arctan2(dy,dx)*180/np.pi
        if desired_theta < 0:
            desired_theta += 360


        amount_to_rotate = desired_theta - current_theta
        if amount_to_rotate < -180:
            amount_to_rotate += 360
        elif amount_to_rotate > 180:
            amount_to_rotate -= 360
        
        return amount_to_rotate

    def _calculate_distance(self, waypoint):
        """
        Calculates distance needed to travel forward to reach a waypoint from current pose
        """
        current_x, current_y, current_theta = self.pose
        des_x, des_y = waypoint

        return np.sqrt( (des_x-current_x)**2 + (des_y - current_y)**2 )


    def drive_to_waypoint(self, waypoint):
        """
        drives at a specified speed towards a specified waypoint given in world coordinate frame.
        """

        # 0 deg pose = pointing in the positive x-direction. pose angle increases when going counter clockwise.
        # 90 deg pose = pointing in the positive y-direction
        # Bottom left of arena = (0,0), moving up towards bin = +y, moving left along loading zone = +x
        self.stop()
        angle_to_rotate = self._calculate_rotation(waypoint)
        distance_to_travel = self._calculate_distance(waypoint)
        
        try:
            if abs(distance_to_travel) > 0.05:
                if abs(angle_to_rotate) > 0.05:
                    # code to rotate
                    self.get_logger().info("Recieved command to rotate by " + str(angle_to_rotate) + " degrees")
                    self.rotate_angle(angle_to_rotate)
                
                time.sleep(1.5)
                # code to drive
                self.get_logger().info("Recieved command to drive forward by " + str(distance_to_travel) + " mm")
                self.drive_distance(distance_to_travel)
        except:
            raise Exception("target waypoint changed")
