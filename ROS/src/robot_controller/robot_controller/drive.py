#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

import RPi.GPIO as GPIO          
import time
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Waypoint
from robot_interfaces.msg import EncoderInfo
import numpy as np

class Drive(Node):
    def __init__(self):

        ############################################## INITIALISATION #########################
        super().__init__("drive_node")
        time.sleep(1)
        self.get_logger().info('Drive node initialised')

        # Setting up GPIO
        self.in1 = 23
        self.in2 = 24
        self.en = 25

        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.en,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.p1=GPIO.PWM(self.en,1000)



        self.in3 = 7
        self.in4 = 8
        self.en2 = 1

        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.en2,GPIO.OUT)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        self.p2=GPIO.PWM(self.en2,1000)




        #######################################################################
        self.WHEEL_CIRCUMFERENCE = 54*np.pi
        self.WHEEL_BASELINE = 210
        self.COUNTS_PER_REV = 3600


        self.left_encoder_count = 0
        self.right_encoder_count = 0
        self.left_encoder_vel = 0
        self.right_encoder_vel = 0

        self.left_speed = 0
        self.right_speed = 0
        self.speed_corrected = False
        self.prev_error = 0
        self.error_sum = 0

        callback_group_encoder = MutuallyExclusiveCallbackGroup()
        callback_group_drive = ReentrantCallbackGroup()

        self.pose_timer = self.create_timer(0.01, self.publish_estimated_pose)
        self.pose_publisher = self.create_publisher(Pose, "estimated_pose", 10) # msg type, topic_name to publish to, buffer size

        self.target_waypoint = [0, 0]
        self.waypoint_subscriber = self.create_subscription(Waypoint, "desired_waypoint", self.waypoint_callback, 10, callback_group= callback_group_drive)
    
        self.encoder_subscriber = self.create_subscription(EncoderInfo, "encoder_info", self.encoder_callback, 10, callback_group=callback_group_encoder)

        self.pose = [0, 0, 90]
        ########## PARAMS INFO
        # 0 deg pose = pointing in the positive x-direction. pose angle increases when going counter clockwise.
        # 90 deg pose = pointing in the positive y-direction
        # Bottom left of arena = (0,0), moving up towards bin = +y, moving left along loading zone = +x
        # x and y will be in units of mm

        # motor 0 = right motor, motor 1 = left motor

        self.prev_waypoint = [self.pose[0], self.pose[1]]
        self.new_waypoint = False

    def publish_estimated_pose(self):
        msg = Pose()
        msg.x = float(self.pose[0])
        msg.y = float(self.pose[1])
        msg.theta = float(self.pose[2])
        self.pose_publisher.publish(msg)

    def waypoint_callback(self, msg:Waypoint):
        self.get_logger().info("Recieved command to move to coordinates: (" + str(msg.x) + ", " + str(msg.y) + ")")
        try:
            if abs(self.pose[0] - msg.x) > 0.05 or abs(self.pose[1] - msg.y) > 0.05:
                time.sleep(0.5)
                self.target_waypoint[0] = msg.x
                self.target_waypoint[1] = msg.y
                self.drive_to_waypoint(speed = 85, waypoint = [msg.x, msg.y])
                self.get_logger().info("Final Robot pose (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )
                self.get_logger().info("Encoder counts: [" + str(self.left_encoder_count) + ", " + str(self.right_encoder_count) + "]" )
            else:
                self.get_logger().info("Robot not moved (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )
        except:
            return

    def encoder_callback(self, msg:EncoderInfo):
        self.left_encoder_count = msg.left_count
        self.right_encoder_count = msg.right_count
        self.left_encoder_vel = msg.left_vel
        self.right_encoder_vel = msg.right_vel
        # self.get_logger().info("COUNT: (" + str(msg.left_count) + ", " + str(msg.right_count) + ")")

    def _set_speed(self, motor, direction, speed):
        """
        Set speed and direction for selected motor

        :param motor:  Either 0 or 1 to select motor
        :param direction: "forward" or "reverse"
        :param speed: 0-100%
        
        """
        # self.get_logger().info("Motor " + str(motor) + " selected to move "  + str(direction) + " and with speed " + str(speed))
        if speed < 0 or speed > 100:
            self.get_logger().error("The speed is invalid")
            self.stop()
            raise Exception("Invalid speed")

        if motor == 0:

            new_right_speed = speed
            if self.speed_corrected:
                new_right_speed = self.right_speed

            if direction == "forward":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(new_right_speed)
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif direction == "reverse":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(new_right_speed)
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
            else:
                self.get_logger().error("The direction is invalid")
                raise Exception("Invalid direction")
            self.right_speed = new_right_speed
            
        elif motor == 1:
            if direction == "forward":
                self.p2.start(0)
                self.p2.ChangeDutyCycle(speed)
                GPIO.output(self.in3,GPIO.HIGH)
                GPIO.output(self.in4,GPIO.LOW)
            elif direction == "reverse":
                self.p2.start(0)
                self.p2.ChangeDutyCycle(speed)
                GPIO.output(self.in3,GPIO.LOW)
                GPIO.output(self.in4,GPIO.HIGH)
            else:
                self.get_logger().error("The direction is invalid")
                raise Exception("Invalid direction")
            self.left_speed = speed
        else:
            self.get_logger().error("The motor is invalid")
            raise Exception("Invalid motor selected")
        
    def _stop_motor(self, motor):
        if motor == 0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)
            self.p1.stop()
        elif motor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)
            self.p2.stop()
        else:
            self.get_logger().error("The motor is invalid")
            raise Exception("Invalid motor selected")
    
    def rotate(self, direction, speed):
        """
        Rotate at a specified speed in either direction
        :param direction: "CW" or "CCW"
        :param speed: 0-100%
        """
        # self.get_logger().info("Robot rotates " + direction + " with Input speed: " + str(speed))
        if speed < 0 or speed > 100:
            self.get_logger().error("The speed is invalid")
            self.stop()
            raise Exception("Invalid speed")

        if direction == "CCW":
            # self.get_logger().info("Rotating CCW")
            self._set_speed(0, "forward", speed)
            self._set_speed(1, "reverse", speed)
        elif direction == "CW":
            # self.get_logger().info("Rotating CW")
            self._set_speed(0, "reverse", speed)
            self._set_speed(1, "forward", speed)
        else:
            self.get_logger().info("Invalid direction")
            raise Exception("Invalid direction")
        
    def drive_forwards(self, speed, duration=None):
        """
        Drive forwards at a specified speed. If duration is given, stops after a certain time
        
        """
        # self.get_logger().info("Robot drives forward with Input speed: " + str(speed) + " Input duration: " + str(duration))
        if speed < 0 or speed > 100:
            self.get_logger().error("The speed is invalid")
            self.stop()
            raise Exception("Invalid speed")
        
        self._set_speed(0, "forward", speed)
        self._set_speed(1, "forward", speed)

        if (duration is not None):
            if isinstance(duration, int) or isinstance(duration, float):
                time.sleep(duration)
                self.stop()
            else:
                self.get_logger().error("The duration is invalid")
                raise Exception("Invalid duration")
        
    def drive_backwards(self, speed, duration=None):
        # self.get_logger().info("Robot drives backwards with Input speed: " + str(speed) + " Input duration: " + str(duration))
        if speed < 0 or speed > 100:
            self.get_logger().error("The speed is invalid")
            self.stop()
            raise Exception("Invalid speed")
        
        self._set_speed(0, "reverse", speed)
        self._set_speed(1, "reverse", speed)

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

    def drive_distance(self, speed, distance):
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

        count = 0
        self.drive_forwards(speed)
        while total_count < count_required:
            if self.target_waypoint[0] != current_target_waypoint[0] or self.target_waypoint[1] != current_target_waypoint[1]:
                self.stop()
                raise Exception("target waypoint changed")
            
            count +=1
            left_count = self.left_encoder_count - left_encoder_start
            right_count = self.right_encoder_count - right_encoder_start
            total_count = (left_count + right_count)//2
            self.pose[0] = original_pose[0] + DISTANCE_PER_COUNT * np.cos(self.pose[2] * (np.pi/180)) * total_count
            self.pose[1] = original_pose[1] + DISTANCE_PER_COUNT * np.sin(self.pose[2] * (np.pi/180)) * total_count

            ## PID wheel speed control
            if total_count%50 == 0 and total_count !=0 and total_count !=50:
                left_vel = self.left_encoder_vel
                right_vel = self.right_encoder_vel
                error = 100 * (left_vel- right_vel)/left_vel  # calculating %error in speed of right wheel compared to left wheel
                self.get_logger().info("error: " + str(error))
                if abs(error) > 1 :
                    self.correct_speed("forward", error)


        distance_travelled = total_count*(self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)
        self.get_logger().info(str(count))
        self.stop()
        # self.get_logger().info("Robot wheel has rotated " + str(deg) + " degrees and travelled a distance of " + str(distance_travelled) + " mm.")

    def correct_speed(self, direction, error):
        """
        This function will adjust the right wheel speed so that it matches the left speed
        """
        self.speed_corrected = False
        
        KP = 0.4
        KD = 0.1
        KI = 0.05

        new_speed = self.right_speed + (KP*error) + (KD*self.prev_error) + (KI*self.error_sum)
        self._set_speed(0, direction, new_speed)
        self.get_logger().info("right wheel speed adjusted to: " + str(self.right_speed))

        self.prev_error = error
        self.error_sum += error
        self.speed_corrected = True

    def rotate_angle(self, speed, angle):
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
            self.rotate("CCW", speed)
            direction = "forward"
        elif angle < 0:
            self.rotate("CW", speed)
            direction = "reverse"
        
        while total_count < count_required:
            if self.target_waypoint[0] != current_target_waypoint[0] or self.target_waypoint[1] != current_target_waypoint[1]:
                self.stop()
                raise Exception("target waypoint changed")
            left_count = self.left_encoder_count - left_encoder_start
            right_count = self.right_encoder_count - right_encoder_start
            total_count = (left_count + right_count)//2
            self.pose[2] = original_pose[2] + ANGLE_PER_COUNT* np.sign(angle) * total_count

            
            ## PID wheel speed control
            if total_count%50 == 0 and total_count !=0 and total_count !=50:
                left_vel = self.left_encoder_vel
                right_vel = self.right_encoder_vel
                error = 100 * (left_vel- right_vel)/left_vel  # calculating %error in speed of right wheel compared to left wheel
                self.get_logger().info("error: " + str(error))
                if abs(error) > 1:
                    self.correct_speed(direction, error)

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


    def drive_to_waypoint(self, speed, waypoint):
        """
        drives at a specified speed towards a specified waypoint given in world coordinate frame.
        """

        # 0 deg pose = pointing in the positive x-direction. pose angle increases when going counter clockwise.
        # 90 deg pose = pointing in the positive y-direction
        # Bottom left of arena = (0,0), moving up towards bin = +y, moving left along loading zone = +x
        
        angle_to_rotate = self._calculate_rotation(waypoint)
        distance_to_travel = self._calculate_distance(waypoint)
        
        try:
            if abs(distance_to_travel) > 0.05:
                if abs(angle_to_rotate) > 0.05:
                    # code to rotate
                    self.get_logger().info("Recieved command to rotate by " + str(angle_to_rotate) + " degrees")
                    self.rotate_angle(speed, angle_to_rotate)
                # code to drive
                self.get_logger().info("Recieved command to drive forward by " + str(distance_to_travel) + " mm")
                self.drive_distance(speed, distance_to_travel)
        except:
            raise Exception("target waypoint changed")




    def clear_gpio(self): 
        GPIO.cleanup()


def main(args=None):
    try:
        rclpy.init(args=args)
        drive_node = Drive()

        executor = MultiThreadedExecutor()
        executor.add_node(drive_node)
        executor.spin()

    except KeyboardInterrupt:
        drive_node.clear_gpio()
        drive_node.get_logger().info("drive node shutdown")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
