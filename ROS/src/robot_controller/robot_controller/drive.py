#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO          
import time
from robot_interfaces.msg import Pose
from robot_interfaces.msg import Waypoint
import numpy as np

class Drive(Node):
    def __init__(self):

        ############################################## INITIALISATION #########################
        super().__init__("drive_node")
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


        self.left_wheel_ena = 5
        self.left_wheel_enb = 6
        GPIO.setup(self.left_wheel_ena, GPIO.IN)
        GPIO.setup(self.left_wheel_enb, GPIO.IN)

        self.right_wheel_ena = 16
        self.right_wheel_enb = 26
        GPIO.setup(self.right_wheel_ena, GPIO.IN)
        GPIO.setup(self.right_wheel_enb, GPIO.IN)

        #######################################################################
        self.WHEEL_CIRCUMFERENCE = 169.6
        self.WHEEL_BASELINE = 225
        self.COUNTS_PER_REV = 3600

        self.left_ena_val = -1
        self.left_enb_val = -1
        self.right_ena_val = -1
        self.right_enb_val = -1

        self.pose_timer = self.create_timer(0.01, self.publish_estimated_pose)
        self.pose_publisher = self.create_publisher(Pose, "estimated_pose", 10) # msg type, topic_name to publish to, buffer size

        self.waypoint_subscriber = self.create_subscription(Waypoint, "desired_waypoint", self.waypoint_callback, 10) 

        self.pose = [0, 0, 90]
        # 0 deg pose = pointing in the positive x-direction. pose angle increases when going counter clockwise.
        # 90 deg pose = pointing in the positive y-direction
        # Bottom left of arena = (0,0), moving up towards bin = +y, moving left along loading zone = +x
        # x and y will be in units of mm

    def publish_estimated_pose(self):
        msg = Pose()
        msg.x = float(self.pose[0])
        msg.y = float(self.pose[1])
        msg.theta = float(self.pose[2])
        self.pose_publisher.publish(msg)

    def waypoint_callback(self, msg:Waypoint):
        self.get_logger().info("Recieved command to move to coordinates: (" + str(msg.x) + ", " + str(msg.y) + ")")

        if abs(self.pose[0] - msg.x) > 0.05 or abs(self.pose[1] - msg.y) > 0.05:
            self.drive_to_waypoint(speed = 95, waypoint = [msg.x, msg.y])

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
            raise Exception("Invalid speed")

        if motor == 0:
            if direction == "forward":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(speed)
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif direction == "reverse":
                self.p1.start(0)
                self.p1.ChangeDutyCycle(speed)
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
            else:
                self.get_logger().error("The direction is invalid")
                raise Exception("Invalid direction")
            
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
            raise Exception("Invalid speed")
        
        self._set_speed(1, "forward", speed)
        self._set_speed(0, "forward", speed)

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

        # 170mm per revolution, per 3600 count

        DISTANCE_PER_COUNT = self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV
        total_count = 0
        deg = 0
        count_required = (distance/self.WHEEL_CIRCUMFERENCE)*self.COUNTS_PER_REV

        # self.get_logger().info("To travel the specified distance, encoder needs to count " + str(count_required) + " times.")

        self.drive_forwards(speed)
        while total_count < count_required:
            if GPIO.input(self.left_wheel_ena) != self.left_ena_val or GPIO.input(self.left_wheel_enb) != self.left_enb_val:

                self.pose[0] += DISTANCE_PER_COUNT * np.cos(self.pose[2] * (np.pi/180))
                self.pose[1] += DISTANCE_PER_COUNT * np.sin(self.pose[2] * (np.pi/180))
                self.left_ena_val = GPIO.input(self.left_wheel_ena)
                self.left_enb_val = GPIO.input(self.left_wheel_enb)

                total_count += 1
                deg = total_count/10
                
                distance_travelled = total_count*(self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)
        self.stop()
        # self.get_logger().info("Robot wheel has rotated " + str(deg) + " degrees and travelled a distance of " + str(distance_travelled) + " mm.")

    def rotate_angle(self, speed, angle):
        """
        rotates a specified angle in degrees at a specified speed   
        
        """
        MM_PER_DEG = self.WHEEL_BASELINE*np.pi / 360
        ANGLE_PER_COUNT = (self.WHEEL_CIRCUMFERENCE/self.COUNTS_PER_REV)/MM_PER_DEG

        total_count = 0
        count_required = ((abs(angle) * MM_PER_DEG)/self.WHEEL_CIRCUMFERENCE) * self.COUNTS_PER_REV


        # self.get_logger().info("To rotate the specified angle, encoder needs to count " + str(count_required) + " times.")

        if angle > 0:
            self.rotate("CCW", speed)
        elif angle < 0:
            self.rotate("CW", speed)
        
        deg_rotated = 0
        while total_count < count_required:
            if GPIO.input(self.left_wheel_ena) != self.left_ena_val or GPIO.input(self.left_wheel_enb) != self.left_enb_val:

                self.pose[2] += ANGLE_PER_COUNT* np.sign(angle)
                self.left_ena_val = GPIO.input(self.left_wheel_ena)
                self.left_enb_val = GPIO.input(self.left_wheel_enb)

                total_count += 1
                
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
        
        self.get_logger().info("Recieved command to rotate by " + str(angle_to_rotate) + " degrees")

        # code to rotate
        self.rotate_angle(speed, angle_to_rotate)

        self.get_logger().info("Recieved command to drive forward by " + str(distance_to_travel) + " mm")

        # code to drive
        self.drive_distance(speed, distance_to_travel)

        self.get_logger().info("Final robot pose (world frame): [" + str(self.pose[0]) + ", " + str(self.pose[1])+ ", " + str(self.pose[2]) + "]" )



    def clear_gpio(self): 
        GPIO.cleanup()


def main(args=None):
    try:
        rclpy.init(args=args)

        drive_node = Drive()
        rclpy.spin(drive_node)

    except KeyboardInterrupt:
        drive_node.clear_gpio()
        drive_node.get_logger().info("drive node shutdown")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
