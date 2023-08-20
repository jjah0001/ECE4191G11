#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO          
import time
from robot_interfaces.msg import Pose

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

        # self.right_wheel_ena = 16
        # self.right_wheel_enb = 26
        # GPIO.setup(self.right_wheel_ena, GPIO.IN)
        # GPIO.setup(self.right_wheel_enb, GPIO.IN)

        #######################################################################
        self.left_ena_val = -1
        self.left_enb_val = -1
        self.right_ena_val = -1
        self.right_enb_val = -1

        self.pose_timer = self.create_timer(0.01, self.publish_estimated_pose)
        self.pose_publisher = self.create_publisher(Pose, "estimated_pose", 10) # msg type, topic_name to publish to, buffer size


    def publish_estimated_pose(self):
        msg = Pose()
        msg.x = 1.0
        msg.y = 2.0
        msg.theta = 3.0
        self.pose_publisher.publish(msg)

    def _set_speed(self, motor, direction, speed):
        """
        Set speed and direction for selected motor

        :param motor:  Either 0 or 1 to select motor
        :param direction: "forward" or "reverse"
        :param speed: 0-100%
        
        """
        self.get_logger().info("Motor " + str(motor) + " selected to move "  + str(direction) + " and with speed " + str(speed))
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
        self.get_logger().info("Robot rotates " + direction + " with Input speed: " + str(speed))
        if speed < 0 or speed > 100:
            self.get_logger().error("The speed is invalid")
            raise Exception("Invalid speed")

        if direction == "CCW":
            self.get_logger().info("Rotating CCW")
            self._set_speed(0, "forward", speed)
            self._set_speed(1, "reverse", speed)
        elif direction == "CW":
            self.get_logger().info("Rotating CW")
            self._set_speed(0, "reverse", speed)
            self._set_speed(1, "forward", speed)
        else:
            self.get_logger().info("Invalid direction")
            raise Exception("Invalid direction")
        
    def drive_forwards(self, speed, duration=None):
        """
        Drive forwards at a specified speed. If duration is given, stops after a certain time
        
        """
        self.get_logger().info("Robot drives forward with Input speed: " + str(speed) + " Input duration: " + str(duration))
        if speed < 0 or speed > 100:
            self.get_logger().error("The speed is invalid")
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
        self.get_logger().info("Robot drives backwards with Input speed: " + str(speed) + " Input duration: " + str(duration))
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
        self.get_logger().info("Motor stopped")
        self._stop_motor(0)
        self._stop_motor(1)

    def drive_distance(self, speed, distance):
        """
        Drives a distance specified in milimetres at a specified speed   
        
        """

        self.drive_forwards(speed)

        # 170mm per revolution, per 3600 count
        WHEEL_CIRCUMFERENCE = 169
        COUNTS_PER_REV = 3600
        total_count = 0
        deg = 0
        count_required = (distance/WHEEL_CIRCUMFERENCE)*COUNTS_PER_REV
        input_a = 0
        input_b = 0

        self.get_logger().info("To travel the specified distance, encoder needs to count " + str(count_required) + " times.")

        while total_count < count_required:
            if GPIO.input(self.left_wheel_ena) != input_a or GPIO.input(self.left_wheel_enb) != input_b:
                input_a = GPIO.input(self.left_wheel_ena)
                input_b = GPIO.input(self.left_wheel_enb)

                total_count += 1
                deg = total_count/10
                
                distance_travelled = total_count*(WHEEL_CIRCUMFERENCE/COUNTS_PER_REV)
                self.get_logger().info("Robot wheel has rotated " + str(deg) + " degrees and travelled a distance of " + str(distance_travelled) + " mm.")
        self.stop()

    def drive_to_waypoint(self, speed, waypoint):
        pass

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
